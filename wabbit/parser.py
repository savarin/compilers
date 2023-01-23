from typing import List, Tuple
import dataclasses

import scanner
from statement import Statem, Break


@dataclasses.dataclass
class Parser:
    tokens: List[scanner.Token]
    current: int


def init_parser(tokens: List[scanner.Token]) -> Parser:
    return Parser(tokens, 0)


def parse(parser: Parser) -> List[Statem]:
    statements: List[Statem] = []

    while not is_at_end(parser):
        parser, individual_statement = break_statement(parser)
        statements.append(individual_statement)

    return statements


def break_statement(parser: Parser) -> Tuple[Parser, Statem]:
    return advance(parser), Break()


def advance(parser: Parser) -> Parser:
    if not is_at_end(parser):
        parser.current += 1

    return parser


def is_at_end(parser: Parser) -> bool:
    return parser.tokens[parser.current].token_type == scanner.TokenType.EOF
