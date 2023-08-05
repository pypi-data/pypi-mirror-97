import dis
import ast
from collections import deque
from opcode import opmap, opname, stack_effect
import types
from collections import defaultdict
from inspect import iscode, getsource

from lambdex.ast_parser import _make_pattern, _shallow_match_ast
from lambdex.utils.ast import pformat
from lambdex.compiler import error
from lambdex.compiler.core import _compile
import linecache

LOAD_GLOBAL = opmap['LOAD_GLOBAL']
LOAD_NAME = opmap['LOAD_NAME']
LOAD_METHOD = opmap['LOAD_METHOD']
LOAD_CLOSURE = opmap['LOAD_CLOSURE']
LOAD_CONST = opmap['LOAD_CONST']

CALL_FUNCTION = opmap['CALL_FUNCTION']
CALL_METHOD = opmap['CALL_METHOD']

MAKE_FUNCTION = opmap['MAKE_FUNCTION']
BUILD_TUPLE = opmap['BUILD_TUPLE']

DUP_TOP = opmap['DUP_TOP']
STORE_DEREF = opmap['STORE_DEREF']

EXTENDED_ARG = opmap['EXTENDED_ARG']


class DefinitionBlock:
    __slots__ = (
        'start_offset',
        'end_offset',
        'make_lambda_start_offset',
        'make_closure_tuple_end_offset',
        'lineno',
        'freevars',
        'keyword',
        'identifier',
        'stack_depth',
        'lambda_code',
        'code_const_id',
        'make_function_mode',
        'compiled_code',
    )

    def __init__(self):
        self.freevars = []
        self.identifier = None
        self.lambda_code = None
        self.make_closure_tuple_end_offset = None
        self.make_function_mode = None

    def __repr__(self):
        return 'Def({})'.format(', '.join('{}={}'.format(name, getattr(self, name, None)) for name in self.__slots__))

    @property
    def key(self):
        return (self.lineno, self.keyword, self.identifier)


def _find_lambdex_definitions(code: types.CodeType):
    linestarts = list(dis.findlinestarts(code))
    idx_linestarts = -1
    n_linestarts = len(linestarts)
    lineno = -1
    defs = []
    stack_depth = 0
    co_names = code.co_names
    co_cellvars = code.co_cellvars
    co_consts = code.co_consts
    last_def = None
    last_op = None
    result = []
    for offset, op, arg in dis._unpack_opargs(code.co_code):
        if n_linestarts - 1 > idx_linestarts and linestarts[idx_linestarts + 1][0] <= offset:
            idx_linestarts += 1
            lineno = linestarts[idx_linestarts][1]

        if op in {LOAD_GLOBAL, LOAD_NAME} and co_names[arg] == 'def_':
            definition = last_def = DefinitionBlock()
            definition.keyword = co_names[arg]
            definition.lineno = lineno
            definition.start_offset = offset
            definition.stack_depth = stack_depth
            definition.make_lambda_start_offset = offset
            defs.append(definition)
            result.append(definition)

        if not defs:
            pass
        elif op == LOAD_METHOD and offset == last_def.start_offset + 2:
            last_def.identifier = co_names[arg]
            last_def.make_lambda_start_offset = offset
        elif op == LOAD_CLOSURE:
            last_def.freevars.append(co_cellvars[arg])

        stack_depth += stack_effect(op, arg)

        if not defs:
            pass
        elif last_def.stack_depth >= stack_depth:
            defs.pop()
            if defs: last_def = defs[-1]
        elif op == LOAD_CONST and iscode(co_consts[arg]):
            last_def.lambda_code = co_consts[arg]
            last_def.code_const_id = arg
        # elif last_def.lambda_code is not None and op == LOAD_CONST and isinstance(co_consts[arg], str):
        #     last_def.qualname_const_id = arg
        elif op == BUILD_TUPLE and last_op == LOAD_CLOSURE:
            last_def.make_closure_tuple_end_offset = offset
        elif op == MAKE_FUNCTION:
            last_def.make_function_mode = arg
        elif op in {CALL_FUNCTION, CALL_METHOD} and last_def.make_function_mode is not None:
            last_def.end_offset = offset
            yield defs.pop()
            if defs: last_def = defs[-1]

        last_op = op

    return result


def _find_definitions_in_ast(code):
    ast_node = ast.parse(''.join(linecache.getlines(code.co_filename)))
    mapping = {}
    iterator = _shallow_match_ast(ast_node, _make_pattern(None, None), yield_node_only=False)
    for lambdex_node, (keyword, identifier) in iterator:
        key = (lambdex_node.lineno, keyword, identifier)
        if key in mapping:
            decl = keyword if not identifier else keyword + '.' + identifier
            error.assert_(
                False,
                'ambiguious declaration {!r}'.format(decl),
                lambdex_node,
                code.co_filename,
            )

        mapping[key] = lambdex_node

    return mapping


class _Instruction:
    __slots__ = ('op', 'arg', 'offset', 'jump_target', 'is_jabs', 'is_jrel', 'length', 'is_jump', 'lineno')

    def __init__(self, op, arg, offset=-1):
        self.op = op
        self.arg = arg
        self._calc_length()
        self.offset = offset + 2 - self.length

        self.is_jrel = op in dis.hasjrel
        self.is_jabs = op in dis.hasjabs
        self.is_jump = self.is_jrel or self.is_jabs

        self._calc_jump_target()

        self.lineno = None

    def _calc_jump_target(self):
        if self.is_jrel:
            target = self.offset + self.arg + 2
        elif self.is_jabs:
            target = self.arg
        else:
            target = None

        self.jump_target = target

    def _calc_length(self):
        arg = self.arg
        if not arg: self.length = 2
        else:
            cnt = 0
            while arg:
                arg >>= 8
                cnt += 1
            self.length = cnt * 2

    def bytecodes(self):
        arg = self.arg or 0
        length = self.length // 2
        for i, byte in enumerate(arg.to_bytes(length, 'little')):
            yield EXTENDED_ARG if i < length - 1 else self.op
            yield byte

    def renew_arg(self, jump_table, offset):
        changed = offset != self.offset
        self.offset = offset
        if self.is_jabs:
            new_arg = jump_table[self].offset
        elif self.is_jrel:
            new_arg = jump_table[self].offset - self.offset - 2
        else:
            self._calc_length()
            return changed

        changed = changed or self.arg != new_arg
        self.arg = new_arg
        self._calc_length()
        self._calc_jump_target()
        return changed

    def target_is_wrong(self, jump_table):
        # if self.is_jump:
        #     print(self.jump_target, jump_table[self].offset)
        return self.is_jump and self.jump_target != jump_table[self].offset

    def __repr__(self):
        return '{}{}{}'.format(str(self.offset).rjust(20), opname[self.op].rjust(20), str(self.arg).rjust(20))


def _recalculate_offsets(instructions, jump_table):
    changed = True
    while changed:
        offset = 0
        changed = False
        for instruction in instructions:
            changed = changed or instruction.renew_arg(jump_table, offset)
            offset += instruction.length

        if not changed and any(item.target_is_wrong(jump_table) for item in instructions):
            print('changed')
            changed = True


class _JumpTable:
    def __init__(self, instructions):
        self._mapping = {}
        self._reversed_mapping = defaultdict(set)
        self.init(instructions)

    def init(self, instructions):
        offset2instruction = {}
        pairs = []
        for instruction in instructions:
            offset2instruction[instruction.offset] = instruction
            if instruction.jump_target is not None:
                pairs.append((instruction.offset, instruction.jump_target))

        for source_offset, target_offset in pairs:
            source = offset2instruction[source_offset]
            target = offset2instruction[target_offset]
            self._mapping[source] = target
            self._reversed_mapping[target].add(source)

        return self

    def replace(self, old, new):
        if old is new: return
        m, rm = self._mapping, self._reversed_mapping
        popped = m.pop(old, None)
        if popped is not None:
            m[new] = popped
            rm[popped].remove(old)
            rm[popped].add(new)

        popped = rm.pop(old, None)
        if popped is not None:
            rm[new] = popped
            for item in popped:
                m[item] = new

    def __getitem__(self, item):
        return self._mapping[item]


def _disassemble(code: types.CodeType):
    ret = []
    linestarts = dict(dis.findlinestarts(code))
    for offset, op, arg in dis._unpack_opargs(code.co_code):
        if op == EXTENDED_ARG:
            continue
        instr = _Instruction(op, arg, offset)
        instr.lineno = linestarts.get(instr.offset)
        ret.append(instr)

    table = _JumpTable(ret)
    return ret, table


def _rewrite_code(code: types.CodeType, ast_defs):
    # old_bytecodes = memoryview(code.co_code)
    # new_bytecodes = bytearray()
    old_instructions, jump_table = _disassemble(code)
    old_instructions = iter(old_instructions)
    new_instructions = []
    handling_bc_defs = []
    remaining_bc_defs = deque(sorted(_find_lambdex_definitions(code), key=lambda x: x.start_offset))
    for x in remaining_bc_defs:
        print(x)

    consts = list(code.co_consts)
    cellvars = list(code.co_cellvars or [])
    extra_cellvar_idx = len(cellvars)
    extra_const_idx = len(consts)

    shifts = []

    current_bc_def = None
    discarded = []
    skipped_const_idxs = []
    while remaining_bc_defs or handling_bc_defs:
        current_instruction = next(old_instructions)
        old_offset = current_instruction.offset
        if remaining_bc_defs and old_offset >= remaining_bc_defs[0].start_offset:
            current_bc_def = remaining_bc_defs.popleft()
            handling_bc_defs.append(current_bc_def)

            ast_def = ast_defs[current_bc_def.key]
            lambdex_code, _ = _compile(ast_def, code.co_filename, current_bc_def.freevars)
            consts[current_bc_def.code_const_id] = lambdex_code
            skipped_const_idxs.append(current_bc_def.code_const_id)
            # consts[current_bc_def.qualname_const_id] = lambdex_code.co_name
            current_bc_def.compiled_code = lambdex_code
        if current_bc_def is not None and old_offset > current_bc_def.end_offset:
            handling_bc_defs.pop()
            current_bc_def = handling_bc_defs[-1] if handling_bc_defs else None
            # continue?

        first_added = None
        if current_bc_def is None:
            new_instructions.append(current_instruction)
            first_added = current_instruction
            # new_bytecodes.extend(old_bytecodes[old_offset:old_offset + 2])
        elif old_offset <= current_bc_def.make_lambda_start_offset:
            pass
            # shifts.append([old_offset, -2])
        elif current_bc_def.make_function_mode & 0x08 and current_bc_def.make_closure_tuple_end_offset == old_offset:
            build_tuple_arg = old_bytecodes[old_offset + 1]
            if build_tuple_arg == 0xff:
                raise RuntimeError
            new_instructions.append(_Instruction(LOAD_CLOSURE, extra_cellvar_idx, old_offset))
            first_added = new_instructions[-1]
            new_instructions.append(_Instruction(BUILD_TUPLE, build_tuple_arg + 1, old_offset))
            # new_bytecodes.extend([LOAD_CLOSURE, extra_cellvar_idx, BUILD_TUPLE, build_tuple_arg + 1])
            # shifts.append([old_offset, +2])
        elif old_offset == current_bc_def.end_offset - 6 and current_bc_def.make_closure_tuple_end_offset is None:
            new_instructions.append(_Instruction(LOAD_CLOSURE, extra_cellvar_idx, old_offset))
            first_added = new_instructions[-1]
            new_instructions.append(_Instruction(BUILD_TUPLE, 1, old_offset))
            new_instructions.append(current_instruction)

            # new_bytecodes.extend([LOAD_CLOSURE, extra_cellvar_idx, BUILD_TUPLE, 1])
            # new_bytecodes.extend(old_bytecodes[old_offset:old_offset + 2])
            # shifts.append([old_offset, +4])
        elif old_offset == current_bc_def.end_offset - 4:
            if extra_const_idx == 0xff:
                raise RuntimeError
            current_instruction.arg = extra_const_idx
            new_instructions.append(current_instruction)
            first_added = current_instruction
            # new_bytecodes.extend([old_bytecodes[old_offset], extra_const_idx])
            consts.append(current_bc_def.compiled_code.co_name)
            extra_const_idx += 1
        elif old_offset == current_bc_def.end_offset - 2:
            current_instruction.arg |= 0x08
            new_instructions.append(current_instruction)
            first_added = new_instructions[-1]
            # new_bytecodes.extend([old_bytecodes[old_offset], old_bytecodes[old_offset + 1] | 0x08])
        elif old_offset == current_bc_def.end_offset:
            new_instructions.append(_Instruction(DUP_TOP, 0x00, old_offset))
            first_added = new_instructions[-1]
            new_instructions.append(_Instruction(STORE_DEREF, extra_cellvar_idx, old_offset))
            # new_bytecodes.extend([DUP_TOP, 0x00, STORE_DEREF, extra_cellvar_idx])
            extra_cellvar_idx += 1
            cellvars.append('?')
            # shifts.append([offset, +2])
        else:
            new_instructions.append(current_instruction)
            first_added = current_instruction
            # new_bytecodes.extend(old_bytecodes[old_offset:old_offset + 2])

        # old_offset += 2
        if first_added is None:
            discarded.append(current_instruction)
        else:
            for item in discarded:
                jump_table.replace(item, first_added)
                if not first_added.lineno: first_added.lineno = item.lineno
            discarded.clear()
    new_instructions.extend(old_instructions)
    _recalculate_offsets(new_instructions, jump_table)
    return _instructions_to_bytes(
        new_instructions
    ), consts, cellvars, bytes(make_lnotab(new_instructions, code.co_firstlineno)), skipped_const_idxs


def _instructions_to_bytes(instructions):
    def _iter():
        for item in instructions:
            yield from item.bytecodes()

    return bytes(_iter())


def make_lnotab(instructions, firstlineno):
    prev_offset = 0
    prev_lineno = firstlineno or 0
    for instr in instructions:
        if instr.lineno is None: continue
        offset = instr.offset
        lineno = instr.lineno

        sdelta = offset - prev_offset
        ldelta = lineno - prev_lineno
        print(sdelta, ldelta)
        while sdelta > 0xff:
            yield 0xff
            yield 0x00
            sdelta -= 0xff
        yield sdelta
        if -128 <= ldelta <= -1:
            yield ldelta + 0x100
        elif 0 <= ldelta <= 127:
            yield ldelta
        elif ldelta < -128:
            yield 0x80
            ldelta += 128
            while ldelta < -128:
                yield 0x00
                yield 0x80
                ldelta += 128
            yield 0x00
            yield ldelta + 0x100
        else:
            yield 0x7f
            ldelta -= 127
            while ldelta > 127:
                yield 0x00
                yield 0x7f
                ldelta -= 127
            yield 0x00
            yield ldelta

        prev_offset = offset
        prev_lineno = lineno


def transpile(code: types.CodeType, ast_defs=None) -> types.CodeType:

    if ast_defs is None:
        ast_defs = _find_definitions_in_ast(code)

    new_bc, new_consts, new_cellvars, new_lnotab, skipped_const_idxs = _rewrite_code(code, ast_defs)
    # print(new_bc, new_consts, new_cellvars)
    # code = code.replace(co_code=new_bc, co_consts=tuple(new_consts), co_cellvars=tuple(new_cellvars))
    # print(code.co_freevars, code.co_cellvars)
    # print(dis.disassemble(code))
    # exec(code)

    # skipped_codes = set()
    # for definition in _find_lambdex_definitions(code):
    #     print(definition)
    #     skipped_codes.add(definition.lambda_code)

    for idx, const in enumerate(new_consts):
        if idx in skipped_const_idxs: continue
        if iscode(const):
            new_consts[idx] = transpile(const, ast_defs)

    return code.replace(
        co_code=new_bc,
        co_consts=tuple(new_consts),
        co_cellvars=tuple(new_cellvars),
        co_lnotab=new_lnotab,
    )


if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as fd:
        content = fd.read()
    code = compile(content, sys.argv[1], 'exec')
    # print(code.co_freevars, code.co_cellvars)
    dis.dis(code)
    new_code = transpile(code)
    dis.dis(new_code)
    exec(new_code)
    print(new_code.co_lnotab.hex().upper())