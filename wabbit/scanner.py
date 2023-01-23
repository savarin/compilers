from typing import Dict, List, Optional, Tuple
import dataclasses
import enum


class TokenType(enum.Enum):
    # Single-character tokens.
    SEMICOLON = "SEMICOLON"

    # Literals.
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    # Keywords.
    PRINT = "PRINT"

    EOF = "EOF"


keywords: Dict[str, TokenType] = {
    "print": TokenType.PRINT,
}


@dataclasses.dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: Optional[int]
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
    scanner: Scanner, token_type: TokenType, literal: Optional[int] = None
) -> Scanner:
    scanner.tokens.append(Token(token_type, current(scanner), literal, scanner.line))

    return scanner


def current(scanner: Scanner) -> str:
    return scanner.source[scanner.start : scanner.current]


def advance(scanner) -> Tuple[Scanner, str]:
    character = scanner.source[scanner.current]
    scanner.current += 1

    return scanner, character


def peek(scanner: Scanner) -> str:
    if is_at_end(scanner):
        return "\0"

    return scanner.source[scanner.current]


def is_at_end(scanner: Scanner) -> bool:
    return scanner.current == len(scanner.source)


def is_digit(character: str) -> bool:
    return "0" <= character <= "9"


def is_alpha(character: str) -> bool:
    return "a" <= character <= "z" or "A" <= character <= "Z" or character == "_"


def number(scanner: Scanner) -> Scanner:
    while is_digit(peek(scanner)):
        scanner, _ = advance(scanner)

    return add_token(scanner, TokenType.NUMBER, int(current(scanner)))


def identifier(scanner: Scanner) -> Scanner:
    while is_digit(peek(scanner)) or is_alpha(peek(scanner)):
        scanner, _ = advance(scanner)

    token_type = keywords.get(current(scanner), None)

    if token_type is None:
        token_type = TokenType.IDENTIFIER

    return add_token(scanner, token_type)
