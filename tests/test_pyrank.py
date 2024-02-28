#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest

from src.pyranklib.pyranklib import part


# test part
test_values = [
    (8, 2, 2, 3),
    (8, 3, 2, 2),
    (9, 4, 2, 1),
    (10, 2, 3, 3),
    (30, 3, 10, 1),
    (30, 3, 5, 27)
]


@pytest.mark.parametrize('n, k, l, expected', test_values)
def test_part(n, k, l, expected):

    actual = part(n, k, l)

    assert actual == expected
