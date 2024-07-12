import io
import tokenize

import pegen.python_generator


def generate_parser(grammar: str, output_path: str):
    grammar, parser, tokenizer = _build_parser_str(grammar)

    with open(output_path, "w") as out_file:
        gen = pegen.python_generator.PythonParserGenerator(grammar, out_file)
        gen.generate("")
    return gen


def _build_parser_str(grammar_str: str, verbose_tokenizer: bool = False, verbose_parser: bool = False):
    from pegen.grammar_parser import GeneratedParser as GrammarParser
    from pegen.tokenizer import Tokenizer
    tokenizer = Tokenizer(tokenize.generate_tokens(io.StringIO(grammar_str).readline), verbose=verbose_tokenizer)
    parser = GrammarParser(tokenizer, verbose=verbose_parser)
    grammar = parser.start()

    if not grammar:
        raise parser.make_syntax_error("Error in grammar")

    return grammar, parser, tokenizer
