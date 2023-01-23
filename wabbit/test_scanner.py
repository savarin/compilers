from scanner import TokenType, init_scanner, scan


def test_format():
    # program 1
    tokens = scan(init_scanner("print 42;"))
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[2].token_type == TokenType.SEMICOLON
    assert tokens[3].token_type == TokenType.EOF

    # program 2
    tokens = scan(init_scanner("print 2 + 3;\n"))
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[2].token_type == TokenType.PLUS
    assert tokens[3].token_type == TokenType.NUMBER
    assert tokens[4].token_type == TokenType.SEMICOLON
    assert tokens[5].token_type == TokenType.EOF

    tokens = scan(init_scanner("print -2 + 3;\n"))
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.MINUS
    assert tokens[2].token_type == TokenType.NUMBER
    assert tokens[3].token_type == TokenType.PLUS
    assert tokens[4].token_type == TokenType.NUMBER
    assert tokens[5].token_type == TokenType.SEMICOLON
    assert tokens[6].token_type == TokenType.EOF

    tokens = scan(init_scanner("print 2 + 3 * -4;\n"))
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[2].token_type == TokenType.PLUS
    assert tokens[3].token_type == TokenType.NUMBER
    assert tokens[4].token_type == TokenType.STAR
    assert tokens[5].token_type == TokenType.MINUS
    assert tokens[6].token_type == TokenType.NUMBER
    assert tokens[7].token_type == TokenType.SEMICOLON
    assert tokens[8].token_type == TokenType.EOF

    tokens = scan(init_scanner("print (2 + 3) * 4;\n"))
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.LEFT_PAREN
    assert tokens[2].token_type == TokenType.NUMBER
    assert tokens[3].token_type == TokenType.PLUS
    assert tokens[4].token_type == TokenType.NUMBER
    assert tokens[5].token_type == TokenType.RIGHT_PAREN
    assert tokens[6].token_type == TokenType.STAR
    assert tokens[7].token_type == TokenType.NUMBER
    assert tokens[8].token_type == TokenType.SEMICOLON
    assert tokens[9].token_type == TokenType.EOF

    tokens = scan(init_scanner("print 2.0 - 3.0 / 4.0;\n"))
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[2].token_type == TokenType.MINUS
    assert tokens[3].token_type == TokenType.NUMBER
    assert tokens[4].token_type == TokenType.SLASH
    assert tokens[5].token_type == TokenType.NUMBER
    assert tokens[6].token_type == TokenType.SEMICOLON
    assert tokens[7].token_type == TokenType.EOF
