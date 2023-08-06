import bashlex
from typing import List


class ParseError(RuntimeError):
    def __init__(self, cause):
        self.__cause__ = cause

    def __str__(self):
        return "cannot parse your shell script"

    def __repr__(self):
        return f"ParseError(cause={self.__cause__!r})"


def get_command(command):
    for part in command.parts:
        if part.kind == "word":
            return part.word
    return None


def get_command_as_args_list(command) -> List[str]:
    return list(map(lambda node: node.word, filter(lambda node: node.kind == "word", command.parts)))


def get_simple_commands(ast_commands, command: str) -> List:
    return list(filter(lambda cmd: get_command(cmd) == command, ast_commands))


def parse_script(script_path: str):
    with open(script_path, "r") as f:
        lines = filter(lambda x: x.strip() != "" and x[0] != "#", f.readlines())
    try:
        lines = map(lambda x: x.strip(), lines)
        lines = map(lambda x: (x[:-1] + " ") if x[-1] == "\\" else (x + "\n"), lines)
        text = "".join(lines)
        return bashlex.parse(text)
    except Exception as e:
        raise ParseError(e)
