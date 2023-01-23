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

    # program 3
    tokens = scan(init_scanner("const pi = 3.14159\n"))
    assert tokens[0].token_type == TokenType.CONST
    assert tokens[1].token_type == TokenType.IDENTIFIER
    assert tokens[2].token_type == TokenType.EQUAL
    assert tokens[3].token_type == TokenType.NUMBER
    assert tokens[4].token_type == TokenType.EOF

    tokens = scan(init_scanner("const tau = 2.0 * pi\n"))
    assert tokens[0].token_type == TokenType.CONST
    assert tokens[1].token_type == TokenType.IDENTIFIER
    assert tokens[2].token_type == TokenType.EQUAL
    assert tokens[3].token_type == TokenType.NUMBER
    assert tokens[4].token_type == TokenType.STAR
    assert tokens[5].token_type == TokenType.IDENTIFIER
    assert tokens[6].token_type == TokenType.EOF

    tokens = scan(init_scanner("var radius = 4.0\n"))
    assert tokens[0].token_type == TokenType.VAR
    assert tokens[1].token_type == TokenType.IDENTIFIER
    assert tokens[2].token_type == TokenType.EQUAL
    assert tokens[3].token_type == TokenType.NUMBER
    assert tokens[4].token_type == TokenType.EOF

    tokens = scan(init_scanner("var perimeter float\n"))
    assert tokens[0].token_type == TokenType.VAR
    assert tokens[1].token_type == TokenType.IDENTIFIER
    assert tokens[2].token_type == TokenType.FLOAT
    assert tokens[3].token_type == TokenType.EOF

    tokens = scan(init_scanner("perimeter = tau * radius\n"))
    assert tokens[0].token_type == TokenType.IDENTIFIER
    assert tokens[1].token_type == TokenType.EQUAL
    assert tokens[2].token_type == TokenType.IDENTIFIER
    assert tokens[3].token_type == TokenType.STAR
    assert tokens[4].token_type == TokenType.IDENTIFIER
    assert tokens[5].token_type == TokenType.EOF

    tokens = scan(init_scanner("print perimeter\n"))
    assert tokens[0].token_type == TokenType.PRINT
    assert tokens[1].token_type == TokenType.IDENTIFIER
    assert tokens[2].token_type == TokenType.EOF

    # program 4
    tokens = scan(init_scanner("print true;\n"))
    assert tokens[1].token_type == TokenType.TRUE
    assert tokens[2].token_type == TokenType.SEMICOLON
    assert tokens[3].token_type == TokenType.EOF

    tokens = scan(init_scanner("print 1 == 1;\n"))
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[2].token_type == TokenType.EQUAL_EQUAL
    assert tokens[3].token_type == TokenType.NUMBER
    assert tokens[4].token_type == TokenType.SEMICOLON
    assert tokens[5].token_type == TokenType.EOF

    tokens = scan(init_scanner("print 0 < 1;\n"))
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[2].token_type == TokenType.GREATER
    assert tokens[3].token_type == TokenType.NUMBER
    assert tokens[4].token_type == TokenType.SEMICOLON
    assert tokens[5].token_type == TokenType.EOF

    tokens = scan(init_scanner("print 1 > 0;\n"))
    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[2].token_type == TokenType.LESS
    assert tokens[3].token_type == TokenType.NUMBER
    assert tokens[4].token_type == TokenType.SEMICOLON
    assert tokens[5].token_type == TokenType.EOF

    tokens = scan(init_scanner("print true && true;\n"))
    assert tokens[1].token_type == TokenType.TRUE
    assert tokens[2].token_type == TokenType.AND
    assert tokens[3].token_type == TokenType.TRUE
    assert tokens[4].token_type == TokenType.SEMICOLON
    assert tokens[5].token_type == TokenType.EOF

    tokens = scan(init_scanner("print false || true;\n"))
    assert tokens[1].token_type == TokenType.FALSE
    assert tokens[2].token_type == TokenType.OR
    assert tokens[3].token_type == TokenType.TRUE
    assert tokens[4].token_type == TokenType.SEMICOLON
    assert tokens[5].token_type == TokenType.EOF

    tokens = scan(init_scanner("print !false;\n"))
    assert tokens[1].token_type == TokenType.BANG
    assert tokens[2].token_type == TokenType.FALSE
    assert tokens[3].token_type == TokenType.SEMICOLON
    assert tokens[4].token_type == TokenType.EOF

    tokens = scan(init_scanner("""\
var a int = 2;
var b int = 3;
var minval int;
if a < b {
   minval = a;
} else {
   minval = b;
}
print minval;
"""))
    assert tokens[0].token_type == TokenType.VAR
    assert tokens[1].token_type == TokenType.IDENTIFIER
    assert tokens[2].token_type == TokenType.INT
    assert tokens[3].token_type == TokenType.EQUAL
    assert tokens[4].token_type == TokenType.NUMBER
    assert tokens[5].token_type == TokenType.SEMICOLON
    assert tokens[6].token_type == TokenType.VAR
    assert tokens[7].token_type == TokenType.IDENTIFIER
    assert tokens[8].token_type == TokenType.INT
    assert tokens[9].token_type == TokenType.EQUAL
    assert tokens[10].token_type == TokenType.NUMBER
    assert tokens[11].token_type == TokenType.SEMICOLON
    assert tokens[12].token_type == TokenType.VAR
    assert tokens[13].token_type == TokenType.IDENTIFIER
    assert tokens[14].token_type == TokenType.INT
    assert tokens[15].token_type == TokenType.SEMICOLON
    assert tokens[16].token_type == TokenType.IF
    assert tokens[17].token_type == TokenType.IDENTIFIER
    assert tokens[18].token_type == TokenType.GREATER
    assert tokens[19].token_type == TokenType.IDENTIFIER
    assert tokens[20].token_type == TokenType.LEFT_BRACE
    assert tokens[21].token_type == TokenType.IDENTIFIER
    assert tokens[22].token_type == TokenType.EQUAL
    assert tokens[23].token_type == TokenType.IDENTIFIER
    assert tokens[24].token_type == TokenType.SEMICOLON
    assert tokens[25].token_type == TokenType.RIGHT_BRACE
    assert tokens[26].token_type == TokenType.IDENTIFIER
    assert tokens[27].token_type == TokenType.LEFT_BRACE
    assert tokens[28].token_type == TokenType.IDENTIFIER
    assert tokens[29].token_type == TokenType.EQUAL
    assert tokens[30].token_type == TokenType.IDENTIFIER
    assert tokens[31].token_type == TokenType.SEMICOLON
    assert tokens[32].token_type == TokenType.RIGHT_BRACE
    assert tokens[33].token_type == TokenType.PRINT
    assert tokens[34].token_type == TokenType.IDENTIFIER
    assert tokens[35].token_type == TokenType.SEMICOLON
    assert tokens[36].token_type == TokenType.EOF
