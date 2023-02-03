from typing import List

from parser import init_parser, parse
from scanner import init_scanner, scan
from expression import Integer
from statement import Statem, Break, Continue, Print


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

    # program 3
    statements = source_to_statements("print 1;")
    assert isinstance(statements[0], Print)
    assert isinstance(statements[0].expression, Integer)
    assert statements[0].expression.value == "1"
