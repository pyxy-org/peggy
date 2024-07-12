"""This file contains patches for pegen. This file should be as minimal as possible."""

def patch_pegen():
    import pegen.python_generator
    pegen.python_generator.PythonCallMakerVisitor.visit_NameLeaf = _visit_NameLeaf
    pegen.python_generator.MODULE_PREFIX = _MODULE_PREFIX
    pegen.python_generator.MODULE_SUFFIX = _MODULE_SUFFIX

_unlowered_names = ("NAME", "NUMBER", "STRING", "OP", "TYPE_COMMENT", "SOFT_KEYWORD")
"""These were converted to lowercase originally, but that conflicts with the grammar!"""

def _visit_NameLeaf(self, node):
    """Patched to not convert the names to lowercase"""
    name = node.value
    if name in _unlowered_names:
        return name, f"self.{name}()"
    if name in ("NEWLINE", "DEDENT", "INDENT", "ENDMARKER"):
        return name, f"self.expect({name!r})"
    return name, f"self.{name}()"

_MODULE_SUFFIX = """

if __name__ == '__main__':
    simple_parser_main({class_name})
"""

_MODULE_PREFIX = f"""#!/usr/bin/env python

import token as _token
import tokenize

from typing import Any, Optional

from pegen.parser import memoize, memoize_left_rec, logger, Parser
_memoize = memoize
_memoize_left_rec = memoize_left_rec
_logger = logger

def tag_result(method_name: str, value: Any):
    if method_name.startswith("_"):
        return value
    if not isinstance(value, list):
        return value
    if isinstance(value[0], str):
        return value
    return [method_name] + value

def memoize(method):
    wrapped = _memoize(method)
    def wrapper(*args, **kwargs) -> Any:
        return tag_result(method.__name__, wrapped(*args, **kwargs))
    return wrapper

def memoize_left_rec(method):
    wrapped = _memoize_left_rec(method)
    def wrapper(*args, **kwargs) -> Any:
        return tag_result(method.__name__, wrapped(*args, **kwargs))
    return wrapper

def logger(method):
    wrapped = _logger(method)
    def wrapper(*args, **kwargs) -> Any:
        return tag_result(method.__name__, wrapped(*args, **kwargs))
    return wrapper

# noinspection PyUnboundLocalVariable,SpellCheckingInspection,PyArgumentList,PyShadowingBuiltins,PyUnusedLocal
class GeneratedParser(Parser):
    # The FSTRING_* functions are here because they were never added to pegen... that should be fixed!
    @memoize
    def FSTRING_START(self) -> Optional[tokenize.TokenInfo]:
        tok = self._tokenizer.peek()
        if tok.type == _token.FSTRING_START:
            return self._tokenizer.getnext()
        return None

    @memoize
    def FSTRING_MIDDLE(self) -> Optional[tokenize.TokenInfo]:
        tok = self._tokenizer.peek()
        if tok.type == _token.FSTRING_MIDDLE:
            return self._tokenizer.getnext()
        return None

    @memoize
    def FSTRING_END(self) -> Optional[tokenize.TokenInfo]:
        tok = self._tokenizer.peek()
        if tok.type == _token.FSTRING_END:
            return self._tokenizer.getnext()
        return None

{"\n".join(f"    def {name}(self): return super().{name.lower()}()" for name in _unlowered_names)}

"""
