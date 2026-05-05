import pytest
from extras import normalize_string

def test_manual_1():
    s = '\"321321\"'
    expected = "321321"
    assert normalize_string(s) == expected