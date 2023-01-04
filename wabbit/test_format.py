from format import format
from model import Literal, Print


def test_format():
    # program 1
    assert format(Print(Literal(42))) == "print 42;\n"
