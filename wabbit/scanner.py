from typing import Dict, List, Tuple, Union
import dataclasses
import enum


class TokenType(enum.Enum):
    # Single-character tokens.
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"

    # One or two character tokens.
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"

    # Two character tokens.
    OR = "OR"
    AND = "AND"

    # Literals.
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    # Keywords.
    PRINT = "PRINT"
    CONST = "CONST"
    VAR = "VAR"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"

    # Types
    BOOL = "BOOL"
    INT = "INT"
    FLOAT = "FLOAT"

    EOF = "EOF"


keywords: Dict[str, TokenType] = {
    "bool": TokenType.BOOL,
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "print": TokenType.PRINT,
    "const": TokenType.CONST,
    "var": TokenType.VAR,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "func": TokenType.FUNCTION,
    "return": TokenType.RETURN,
}


@dataclasses.dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: Union[int, float, None]
    line: int


@dataclasses.dataclass
class Scanner:
    source: str
    tokens: List[Token]
    start: int
    current: int
    line: int


def init_scanner(source: str) -> Scanner:
    tokens: List[Token] = []
    return Scanner(source, tokens, 0, 0, 1)


def scan(scanner: Scanner) -> List[Token]:
    while not is_at_end(scanner):
        scanner.start = scanner.current
        scanner = scan_token(scanner)

    scanner.tokens.append(Token(TokenType.EOF, "", None, scanner.line))

    return scanner.tokens


def scan_token(scanner: Scanner) -> Scanner:
    scanner, character = advance(scanner)

    if character == ";":
        scanner = add_token(scanner, TokenType.SEMICOLON)
    elif character == ",":
        scanner = add_token(scanner, TokenType.COMMA)
    elif character == "+":
        scanner = add_token(scanner, TokenType.PLUS)
    elif character == "-":
        scanner = add_token(scanner, TokenType.MINUS)
    elif character == "*":
        scanner = add_token(scanner, TokenType.STAR)
    elif character == "/":
        scanner = add_token(scanner, TokenType.SLASH)
    elif character == "(":
        scanner = add_token(scanner, TokenType.LEFT_PAREN)
    elif character == ")":
        scanner = add_token(scanner, TokenType.RIGHT_PAREN)
    elif character == "{":
        scanner = add_token(scanner, TokenType.LEFT_BRACE)
    elif character == "}":
        scanner = add_token(scanner, TokenType.RIGHT_BRACE)

    elif character == "=":
        scanner = add_token(
            scanner,
            TokenType.EQUAL_EQUAL if is_match(scanner, "=") else TokenType.EQUAL,
        )
    elif character == "!":
        scanner = add_token(
            scanner, TokenType.BANG_EQUAL if is_match(scanner, "=") else TokenType.BANG
        )
    elif character == "<":
        scanner = add_token(
            scanner,
            TokenType.GREATER_EQUAL if is_match(scanner, "=") else TokenType.GREATER,
        )
    elif character == ">":
        scanner = add_token(
            scanner, TokenType.LESS_EQUAL if is_match(scanner, "=") else TokenType.LESS
        )

    elif character == "&" and is_match(scanner, "&"):
        scanner = add_token(scanner, TokenType.AND)
    elif character == "|" and is_match(scanner, "|"):
        scanner = add_token(scanner, TokenType.OR)

    elif character == "\n":
        scanner.line += 1
    elif character == " ":
        pass

    elif is_digit(character):
        scanner = number(scanner)
    elif is_alpha(character):
        scanner = identifier(scanner)

    else:
        raise Exception(
            f"Error on line {scanner.line}: Unexpected character {character}"
        )

    return scanner


def add_token(
    scanner: Scanner, token_type: TokenType, literal: Union[int, float, None] = None
) -> Scanner:
    scanner.tokens.append(Token(token_type, current(scanner), literal, scanner.line))

    return scanner


def advance(scanner: Scanner) -> Tuple[Scanner, str]:
    character = scanner.source[scanner.current]
    scanner.current += 1

    return scanner, character


def current(scanner: Scanner) -> str:
    return scanner.source[scanner.start : scanner.current]


def peek(scanner: Scanner) -> str:
    if is_at_end(scanner):
        return "\0"

    return scanner.source[scanner.current]


def peek_next(scanner: Scanner) -> str:
    if scanner.current + 1 >= len(scanner.source):
        return "\0"

    return scanner.source[scanner.current + 1]


def is_at_end(scanner: Scanner) -> bool:
    return scanner.current == len(scanner.source)


def is_digit(character: str) -> bool:
    return "0" <= character <= "9"


def is_alpha(character: str) -> bool:
    return "a" <= character <= "z" or "A" <= character <= "Z" or character == "_"


def is_match(scanner: Scanner, expected: str) -> bool:
    if is_at_end(scanner):
        return False

    elif scanner.source[scanner.current] != expected:
        return False

    scanner.current += 1
    return True


def number(scanner: Scanner) -> Scanner:
    is_float = False

    while is_digit(peek(scanner)):
        scanner, _ = advance(scanner)

    if peek(scanner) == "." and is_digit(peek_next(scanner)):
        is_float = True
        scanner, _ = advance(scanner)

        while is_digit(peek(scanner)):
            scanner, _ = advance(scanner)

    literal = float(current(scanner)) if is_float else int(current(scanner))
    return add_token(scanner, TokenType.NUMBER, literal)


def identifier(scanner: Scanner) -> Scanner:
    while is_digit(peek(scanner)) or is_alpha(peek(scanner)):
        scanner, _ = advance(scanner)

    token_type = keywords.get(current(scanner), None)

    if token_type is None:
        token_type = TokenType.IDENTIFIER

    return add_token(scanner, token_type)
