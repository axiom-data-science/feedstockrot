import re


def escape_regex_format_str(input: str) -> str:
    return re.escape(input).replace('\\{\\}\\', '{}')
