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


def find_lambdex(code: types.CodeType):
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
