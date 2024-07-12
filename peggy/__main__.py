from pathlib import Path

import arguably

from peggy.generator import generate_parser
from peggy.patches import patch_pegen
from peggy.postprocess import process_generated_parser
from peggy.preprocess import process_grammar, append_grammar_file, add_rule_alternative


@arguably.command
def __root__(grammar_file: str, parser_file: str, extra_grammar_file: str | None = None, *, rule_alt: list[str] | None = None):
    patch_pegen()

    with open(grammar_file, "r") as fh:
        grammar = fh.read()

    grammar = process_grammar(grammar)
    if extra_grammar_file is not None:
        grammar = append_grammar_file(grammar, extra_grammar_file)
    for alt_item in rule_alt:
        name, _, value = alt_item.partition("=")
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        grammar = add_rule_alternative(grammar, name, value)

    print(grammar)
    generate_parser(grammar, parser_file)
    process_generated_parser(parser_file)


if __name__ == "__main__":
    arguably.run()
