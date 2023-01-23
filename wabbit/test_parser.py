from typing import List

from parser import init_parser, parse
from scanner import init_scanner, scan
from statement import Statem, Break, Continue


def source_to_statements(source: str) -> List[Statem]:
    tokens = scan(init_scanner(source))
    return parse(init_parser(tokens))


def test_parse():
    # program 1
    statements = source_to_statements("break;")
    assert isinstance(statements[0], Break)

    # program 2
    statements = source_to_statements("continue;")
    assert isinstance(statements[0], Continue)
