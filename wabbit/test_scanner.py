from scanner import TokenType, init_scanner, scan


def test_format():
    # program 1
    tokens = scan(init_scanner("print 42;"))

    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[2].token_type == TokenType.SEMICOLON
    assert tokens[3].token_type == TokenType.EOF
