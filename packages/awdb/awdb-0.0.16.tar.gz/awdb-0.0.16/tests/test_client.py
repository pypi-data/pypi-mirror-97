# -*- coding: utf-8 -*-
import pytest
from awdb.cli.client import parse_break_line


def test_parse_breakline():
    cmd = "break any any any"
    res = parse_break_line(cmd)
    assert res == ['any', 'any', 'any']

    cmd = "break any test.py:1"
    res = parse_break_line(cmd)
    assert res == ['any', 1, 'test.py']

    cmd = "break any test.py 1 x == True"
    res = parse_break_line(cmd)
    assert res == ['any', 1, 'test.py', "x == True"]

    cmd = "break 1 2 3"
    res = parse_break_line(cmd)
    assert res == ['1', 3, '2']

    cmd = "break 1 2 3 x == {'2': 3}"
    res = parse_break_line(cmd)
    assert res == ['1', 3, '2', "x == {'2': 3}"]

    cmd = "break any test.py:1:3"
    res = parse_break_line(cmd)
    assert res == ['any', [1, 3], 'test.py']

    cmd = "break any test.py 1:3"
    res = parse_break_line(cmd)
    assert res == ['any', [1, 3], 'test.py']

    cmd = "break any test.py 1:3 test == {'a': 2}"
    res = parse_break_line(cmd)
    assert res == ['any', [1, 3], 'test.py', "test == {'a': 2}"]
