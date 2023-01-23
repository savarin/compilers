from typing import List, Tuple
import dataclasses

import scanner
from expression import TypeEnum, Expr, Integer, Name, Type
from statement import DeclarationEnum, Statem, Break, Continue, Print, Declaration


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
        parser, individual_statement = declaration(parser)
        statements.append(individual_statement)

    return statements


def declaration(parser: Parser) -> Tuple[Parser, Statem]:
    parser, is_variable = match(
        parser, [scanner.TokenType.CONST, scanner.TokenType.VAR]
    )

    if is_variable:
        return variable_declaration(parser)

    return statement(parser)


def variable_declaration(parser: Parser) -> Tuple[Parser, Statem]:
    declaration_enum = DeclarationEnum(previous(parser).token_type.value)

    parser, name = consume(
        parser, scanner.TokenType.IDENTIFIER, "Expect variable name."
    )

    var_type = None
    parser, is_var_type = match(
        parser, [scanner.TokenType.BOOL, scanner.TokenType.INT, scanner.TokenType.FLOAT]
    )

    if is_var_type:
        var_type = Type(TypeEnum(previous(parser).token_type.value))

    initializer = None
    parser, is_equal = match(parser, [scanner.TokenType.EQUAL])

    if is_equal:
        parser, initializer = expression(parser)

    parser, _ = consume(
        parser, scanner.TokenType.SEMICOLON, "Expect ';' after variable declaration."
    )

    return parser, Declaration(
        Name(name.lexeme), declaration_enum, var_type, initializer
    )


def statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, is_break = match(parser, [scanner.TokenType.BREAK])

    if is_break:
        return break_statement(parser)

    parser, is_continue = match(parser, [scanner.TokenType.CONTINUE])

    if is_continue:
        return continue_statement(parser)

    parser, is_print = match(parser, [scanner.TokenType.PRINT])

    if is_print:
        return print_statement(parser)

    raise ParseError()


def break_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, _ = consume(
        parser, scanner.TokenType.SEMICOLON, "Expect ';' after break statement."
    )

    return parser, Break()


def continue_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, _ = consume(
        parser, scanner.TokenType.SEMICOLON, "Expect ';' after continue statement."
    )

    return parser, Continue()


def print_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, individual_expression = expression(parser)
    parser, _ = consume(
        parser, scanner.TokenType.SEMICOLON, "Expect ';' after continue statement."
    )

    return parser, Print(individual_expression)


def expression(parser: Parser) -> Tuple[Parser, Expr]:
    parser, token = advance(parser)

    return parser, Integer(token.lexeme)


def match(parser: Parser, token_types: List[scanner.TokenType]) -> Tuple[Parser, bool]:
    for token_type in token_types:
        if expect(parser, token_type):
            parser, _ = advance(parser)
            return parser, True

    return parser, False


def consume(
    parser: Parser, token_type: scanner.TokenType, message: str
) -> Tuple[Parser, scanner.Token]:
    if expect(parser, token_type):
        return advance(parser)

    raise ParseError()


def advance(parser: Parser) -> Tuple[Parser, scanner.Token]:
    if not is_at_end(parser):
        parser.current += 1

    return parser, previous(parser)


def expect(parser: Parser, token_type: scanner.TokenType) -> bool:
    if is_at_end(parser):
        return False

    return peek(parser).token_type == token_type


def peek(parser: Parser) -> scanner.Token:
    return parser.tokens[parser.current]


def previous(parser: Parser) -> scanner.Token:
    return parser.tokens[parser.current - 1]


def is_at_end(parser: Parser) -> bool:
    return peek(parser).token_type == scanner.TokenType.EOF
