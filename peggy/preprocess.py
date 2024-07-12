import re
from pathlib import Path

GRAMMAR_SECTION_HEADER = "# ========================= START OF THE GRAMMAR ========================="

OUTPUT_TO_REMOVE = """# Keywords and soft keywords are listed at the end of the parser definition.
class GeneratedParser(Parser):"""

def process_grammar(text):
    # Remove anything before the grammar section
    match = re.search(GRAMMAR_SECTION_HEADER, text, re.MULTILINE)
    if not match:
        raise Exception("Cannot find grammar section")
    text = text[match.start():]

    # Remove anything inside braces
    text = re.sub(r"[^']{(?:[^{}']|'[^']*'|{(?:[^{}']|'[^']*')*})*[^']}", "", text)

    # Remove types
    text = re.sub(r"^[^\n ]+(\[[a-zA-Z_*]+])", lambda m: m.group(0).replace(m.group(1), ""), text, flags=re.MULTILINE)
    text = re.sub(r"\[[a-zA-Z_*]+]=", "=", text, flags=re.MULTILINE)

    # Append start
    text += "\nstart: file\n"

    return text


def append_grammar_file(grammar: str, extra_grammar_path: str) -> str:
    with open(extra_grammar_path, "r") as fh:
        return grammar + "\n" + fh.read()


def add_rule_alternative(grammar: str, rule: str, contents: str) -> str:
    assert re.search(rf"^({rule}:(( *\n(?:\s+\|.*\n)+)|( .*)))", grammar, flags=re.MULTILINE)
    return re.sub(rf"^({rule}:(( *\n(?:\s+\|.*\n)+)|( .*)))", rf"\1\n    | {contents}", grammar, flags=re.MULTILINE)
