from typing import List, Tuple
import dataclasses

import scanner
from statement import Statem, Break, Continue


class ParseError(Exception):
    ...


@dataclasses.dataclass
class Parser:
    tokens: List[scanner.Token]
    current: int


def init_parser(tokens: List[scanner.Token]) -> Parser:
    return Parser(tokens, 0)


def parse(parser: Parser) -> List[Statem]:
    statements: List[Statem] = []

    while not is_at_end(parser):
        parser, individual_statement = statement(parser)
        statements.append(individual_statement)

    return statements


def statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, is_break = match(parser, [scanner.TokenType.BREAK])

    if is_break:
        return break_statement(parser)

    parser, is_continue = match(parser, [scanner.TokenType.CONTINUE])

    if is_continue:
        return continue_statement(parser)

    raise ParseError()


def break_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser = consume(
        parser, scanner.TokenType.SEMICOLON, "Expect ';' after break statement."
    )

    return parser, Break()


def continue_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser = consume(
        parser, scanner.TokenType.SEMICOLON, "Expect ';' after continue statement."
    )

    return parser, Continue()


def match(parser: Parser, token_types: List[scanner.TokenType]) -> Tuple[Parser, bool]:
    for token_type in token_types:
        if expect(parser, token_type):
            parser = advance(parser)
            return parser, True

    return parser, False


def consume(
    parser: Parser, token_type: scanner.TokenType, message: str
) -> Tuple[Parser, scanner.Token]:
    if expect(parser, token_type):
        return advance(parser)

    raise ParseError()


def advance(parser: Parser) -> Parser:
    if not is_at_end(parser):
        parser.current += 1

    return parser


def expect(parser: Parser, token_type: scanner.TokenType) -> bool:
    if is_at_end(parser):
        return False

    return peek(parser).token_type == token_type


def peek(parser: Parser) -> scanner.Token:
    return parser.tokens[parser.current]


def is_at_end(parser: Parser) -> bool:
    return peek(parser).token_type == scanner.TokenType.EOF
