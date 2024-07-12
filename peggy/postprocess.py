import re

_OUTPUT_TO_REMOVE = """# Keywords and soft keywords are listed at the end of the parser definition.
class GeneratedParser(Parser):"""


def process_generated_parser(parser_file: str):
    import black

    with open(parser_file, 'r') as file:
        content = file.read()

    assert _OUTPUT_TO_REMOVE in content
    content = content.replace(_OUTPUT_TO_REMOVE, "", 1)
    content = black.format_str(content, mode=black.FileMode())

    content = _add_import(content, "pegen/parser.py")
    content = _add_import(content, "pegen/tokenizer.py")

    with open(parser_file, 'w') as file:
        file.write(content)


def _add_import(content: str, file_path: str):
    with open(file_path, "r") as fh:
        module_path = file_path.partition(".")[0].replace("/", "\\.")
        return fh.read() + "\n" + re.sub(rf'^from {module_path}.*\n?', '', content, flags=re.MULTILINE)
