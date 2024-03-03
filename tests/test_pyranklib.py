#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest

from pyranklib.pyranklib import (
    CombinationIterator,
    PermutationIterator,
    unrank_combination,
    unrank_permutation,
    rank_combination,
    rank_permutation,
    Combination,
    Permutation,
    part
)



# test unrank_combination

test_values = [
    (set(), 0, 0, set()),
    (set(), 0, 1, None),
    (set(), 1, 0, None),
    (set(), 1, 1, None),
    ({'A'}, 0, 0, set()),
    ({'A'}, 1, 0, {'A'}),
    ({'A'}, 0, 1, None),
    ({'A'}, 1, 1, None),
    ({'A', 'B'}, 0, 0, set()),
    ({'A', 'B'}, 0, 1, None),
    ({'A', 'B'}, 1, 0, {'A'}),
    ({'A', 'B'}, 1, 1, {'B'}),
    ({'A', 'B'}, 2, 0, {'A', 'B'}),
    ({'A', 'B'}, 2, 1, None),
    ({'A', 'B', 'C'}, 0, 0, set()),
    ({'A', 'B', 'C'}, 0, 1, None),
    ({'A', 'B', 'C'}, 1, 0, {'A'}),
    ({'A', 'B', 'C'}, 1, 1, {'B'}),
    ({'A', 'B', 'C'}, 1, 2, {'C'}),
    ({'A', 'B', 'C'}, 1, 3, None),
    ({'A', 'B', 'C'}, 2, 0, {'A', 'B'}),
    ({'A', 'B', 'C'}, 2, 1, {'A', 'C'}),
    ({'A', 'B', 'C'}, 2, 2, {'B', 'C'}),
    ({'A', 'B', 'C'}, 2, 3, None),
    ({'A', 'B', 'C'}, 3, 0, {'A', 'B', 'C'}),
    ({'A', 'B', 'C'}, 3, 1, None),
    ({'A', 'B', 'C', 'D'}, 3, 0, {'A', 'B', 'C'}),
    ({'A', 'B', 'C', 'D'}, 3, 1, {'A', 'B', 'D'}),
    ({'A', 'B', 'C', 'D'}, 3, 2, {'A', 'C', 'D'}),
    ({'A', 'B', 'C', 'D'}, 3, 3, {'B', 'C', 'D'}),
    ({'A', 'B', 'C', 'D'}, 3, 4, None),
    ({'A', 'B', 'C', 'D'}, 4, 0, {'A', 'B', 'C', 'D'}),
    ({'A', 'B', 'C', 'D'}, 4, 1, None),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 0, {'A', 'B'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 1, {'A', 'C'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 2, {'A', 'D'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 3, {'A', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 4, {'B', 'C'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 5, {'B', 'D'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 6, {'B', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 7, {'C', 'D'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 8, {'C', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 9, {'D', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 2, 10, None),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 0, {'A', 'B', 'C'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 1, {'A', 'B', 'D'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 2, {'A', 'B', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 3, {'A', 'C', 'D'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 4, {'A', 'C', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 5, {'A', 'D', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 6, {'B', 'C', 'D'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 7, {'B', 'C', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 8, {'B', 'D', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 9, {'C', 'D', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 3, 10, None),
    ({'A', 'B', 'C', 'D', 'E'}, 4, 0, {'A', 'B', 'C', 'D'}),
    ({'A', 'B', 'C', 'D', 'E'}, 4, 1, {'A', 'B', 'C', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 4, 2, {'A', 'B', 'D', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 4, 3, {'A', 'C', 'D', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 4, 4, {'B', 'C', 'D', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 4, 5, None),
    ({'A', 'B', 'C', 'D', 'E'}, 5, 0, {'A', 'B', 'C', 'D', 'E'}),
    ({'A', 'B', 'C', 'D', 'E'}, 5, 1, None)
]


@pytest.mark.parametrize('universal_set, k, rank, expected', test_values)
def test_unrank_combination(universal_set, k, rank, expected):

    actual = unrank_combination(universal_set, k, rank)
    if actual:
        actual = actual.combinatoric

    assert actual == expected


# test rank_combination
test_values = [
    (frozenset(), frozenset(), 0),
    (frozenset({'A'}), frozenset(), 0),
    (frozenset({'A'}), frozenset({'A'}), 0),
    (frozenset({'A', 'B'}), frozenset(), 0),
    (frozenset({'A', 'B'}), frozenset({'A'}), 0),
    (frozenset({'A', 'B'}), frozenset({'B'}), 1),
    (frozenset({'A', 'B'}), frozenset({'A', 'B'}), 0),
    (frozenset({'A', 'B', 'C'}), frozenset(), 0),
    (frozenset({'A', 'B', 'C'}), frozenset({'A'}), 0),
    (frozenset({'A', 'B', 'C'}), frozenset({'B'}), 1),
    (frozenset({'A', 'B', 'C'}), frozenset({'C'}), 2),
    (frozenset({'A', 'B', 'C'}), frozenset({'A', 'B'}), 0),
    (frozenset({'A', 'B', 'C'}), frozenset({'A', 'C'}), 1),
    (frozenset({'A', 'B', 'C'}), frozenset({'B', 'C'}), 2),
    (frozenset({'A', 'B', 'C'}), frozenset({'A', 'B', 'C'}), 0),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset(), 0),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'A'}), 0),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'B'}), 1),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'C'}), 2),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'D'}), 3),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'A', 'B'}), 0),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'A', 'C'}), 1),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'A', 'D'}), 2),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'B', 'C'}), 3),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'B', 'D'}), 4),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'C', 'D'}), 5),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'A', 'B', 'C'}), 0),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'A', 'B', 'D'}), 1),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'A', 'C', 'D'}), 2),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'B', 'C', 'D'}), 3),
    (frozenset({'A', 'B', 'C', 'D'}), frozenset({'A', 'B', 'C', 'D'}), 0),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'B'}), 0),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'C'}), 1),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'D'}), 2),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'E'}), 3),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'B', 'C'}), 4),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'B', 'D'}), 5),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'B', 'E'}), 6),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'C', 'D'}), 7),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'C', 'E'}), 8),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'D', 'E'}), 9),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'B', 'C'}), 0),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'B', 'D'}), 1),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'B', 'E'}), 2),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'C', 'D'}), 3),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'C', 'E'}), 4),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'D', 'E'}), 5),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'B', 'C', 'D'}), 6),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'B', 'C', 'E'}), 7),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'B', 'D', 'E'}), 8),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'C', 'D', 'E'}), 9),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'B', 'C', 'D'}), 0),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'B', 'C', 'E'}), 1),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'B', 'D', 'E'}), 2),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'C', 'D', 'E'}), 3),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'B', 'C', 'D', 'E'}), 4),
    (frozenset({'A', 'B', 'C', 'D', 'E'}), frozenset({'A', 'B', 'C', 'D', 'E'}), 0),
]


@pytest.mark.parametrize('universal_set, combination, expected', test_values)
def test_rank_combination(universal_set, combination, expected):

    actual = rank_combination(universal_set, combination)

    assert actual == expected


# test Combination 

# test Combination.combinatoric

test_values = [
    (Combination(set(), set()), set()),
    (Combination({'A'}, set()), set()),
    (Combination({'A'}, set('A')), set('A')),
]


@pytest.mark.parametrize('combination, expected', test_values)
def test_combination_combinatoric(combination, expected):

    actual = combination.combinatoric

    assert actual == expected
    

# test Combination.rank

test_values = [
    (Combination({'A', 'B', 'C'}, {}), 0),
    (Combination({'A', 'B', 'C', 'D'}, {'C'}), 2),
    (Combination({'A', 'B', 'C', 'D'}, {'D'}), 3),
    (Combination({'A', 'B', 'C', 'D'}, {'A', 'B', 'C', 'D'}), 0),
    (Combination({'A', 'B', 'C', 'D', 'E'}, {'C', 'D'}), 7),
    (Combination({'A', 'B', 'C', 'D', 'E'}, {'A', 'D', 'E'}), 5),
    (Combination({'A', 'B', 'C', 'D', 'E'}, {'A', 'B', 'C', 'D'}), 0),
    (Combination({'A', 'B', 'C', 'D', 'E'}, {'B', 'C', 'D', 'E'}), 4),
    (Combination({'A', 'B', 'C', 'D', 'E'}, {'A', 'B', 'C', 'D', 'E'}), 0),
]


@pytest.mark.parametrize('combination, expected', test_values)
def test_combination_rank(combination, expected):

    actual = combination.rank()

    assert actual == expected


# test Combination.successor()
test_values = [
    (Combination(set(), set()), None),
    (Combination({'A'}, set()), None),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B'}, {'B'})),
    (Combination({'A', 'B', 'C', 'D'}, {'A', 'D'}), Combination({'A', 'B', 'C', 'D'}, {'B', 'C'})),
    (Combination({'A', 'B', 'C', 'D', 'E'}, {'A', 'D', 'E'}), Combination({'A', 'B', 'C', 'D', 'E'}, {'B', 'C', 'D'})),
    (Combination({'A', 'B', 'C', 'D', 'E'}, {'A', 'C', 'D', 'E'}), Combination({'A', 'B', 'C', 'D', 'E'}, {'B', 'C', 'D', 'E'}))
]


@pytest.mark.parametrize('combination, expected', test_values)
def test_combination_successor(combination, expected):

    actual = combination.successor()

    assert actual == expected
    

# test Combination.__eq__()
test_values = [
    (Combination(set(), set()), Combination(set(), set()), True),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B'}, {'B'}), False),
    (Combination({'A', 'B', 'C', 'D'}, {'A', 'D'}), Combination({'A', 'B', 'C', 'D'}, {'A', 'D'}), True),
    (Combination({'A', 'B'}, {'A'}), {'A', 'B'}, NotImplementedError()),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B', 'C', 'D'}, {'A'}), NotImplementedError()),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B'}, {'A', 'B'}), NotImplementedError())
]


@pytest.mark.parametrize('combination_a, combination_b, expected', test_values)
def test_combination_eq(combination_a, combination_b, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            combination_a == combination_b
    
    else:
        
        actual = combination_a == combination_b

        assert actual == expected


# test Combination.__lt__()
test_values = [
    (Combination(set(), set()), Combination(set(), set()), False),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B'}, {'B'}), True),
    (Combination({'A', 'B', 'C', 'D'}, {'A', 'D'}), Combination({'A', 'B', 'C', 'D'}, {'A', 'B'}), False),
    (Combination({'A', 'B'}, {'A'}), {'A', 'B'}, NotImplementedError()),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B', 'C', 'D'}, {'A'}), NotImplementedError()),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B'}, {'A', 'B'}), NotImplementedError())
]


@pytest.mark.parametrize('combination_a, combination_b, expected', test_values)
def test_combination_lt(combination_a, combination_b, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            combination_a < combination_b
    
    else:
        
        actual = combination_a < combination_b

        assert actual == expected

# test Combination.__gt__()
test_values = [
    (Combination(set(), set()), Combination(set(), set()), False),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B'}, {'B'}), False),
    (Combination({'A', 'B', 'C', 'D'}, {'A', 'D'}), Combination({'A', 'B', 'C', 'D'}, {'A', 'B'}), True),
    (Combination({'A', 'B'}, {'A'}), {'A', 'B'}, NotImplementedError()),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B', 'C', 'D'}, {'A'}), NotImplementedError()),
    (Combination({'A', 'B'}, {'A'}), Combination({'A', 'B'}, {'A', 'B'}), NotImplementedError())
]


@pytest.mark.parametrize('combination_a, combination_b, expected', test_values)
def test_combination_gt(combination_a, combination_b, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            combination_a > combination_b
    
    else:
        
        actual = combination_a > combination_b

        assert actual == expected


# test CombinationIterator
test_values = [
    (CombinationIterator(set(), 0, 0), [Combination(set(), set())]),
    (CombinationIterator({'A'}, 0, 0), [Combination({'A'}, set())]),
    (CombinationIterator({'A'}, 1, 0), [Combination({'A'}, {'A'})]),
    (
        CombinationIterator({'A', 'B'}, 1, 0), 
        [
            Combination({'A', 'B'}, {'A'}), 
            Combination({'A', 'B'}, {'B'})
        ]
    ),
    (
        CombinationIterator({'A', 'B'}, 1, 1), 
        [Combination({'A', 'B'}, {'B'})]
    ),
    (
        CombinationIterator({'A', 'B'}, 2, 0), 
        [Combination({'A', 'B'}, {'A', 'B'})]
    ),
    (
        CombinationIterator({'A', 'B', 'C'}, 1, 0), 
        [
            Combination({'A', 'B', 'C'}, {'A'}), 
            Combination({'A', 'B', 'C'}, {'B'}),
            Combination({'A', 'B', 'C'}, {'C'})
        ]       
    ),
    (
        CombinationIterator({'A', 'B', 'C'}, 2, 2), 
        [
            Combination({'A', 'B', 'C'}, {'B', 'C'})
        ]       
    )
]


@pytest.mark.parametrize('combination_iterator, expected', test_values)
def test_combination_iterator(combination_iterator, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            combinations = list(combination_iterator)
    
    else:
        
        actual = list(combination_iterator)

        assert actual == expected


# test unrank_permutation

test_values = [
    (set(), 0, 0, Permutation(set(), tuple())),
    (set(), 0, 1, None),
    (set(), 1, 0, None),
    (set(), 1, 1, None),
    ({'A'}, 0, 0, Permutation({'A'}, tuple())),
    ({'A'}, 1, 0, Permutation({'A'}, ('A',))),
    ({'A'}, 0, 1, None),
    ({'A'}, 1, 1, None),
    ({'A', 'B'}, 0, 0, Permutation({'A', 'B'}, tuple())),
    ({'A', 'B'}, 0, 1, None),
    ({'A', 'B'}, 1, 0, Permutation({'A', 'B'}, ('A', ))),
    ({'A', 'B'}, 1, 1, Permutation({'A', 'B'}, ('B', ))),
    ({'A', 'B'}, 2, 0, Permutation({'A', 'B'}, ('A', 'B'))),
    ({'A', 'B'}, 2, 1, Permutation({'A', 'B'}, ('B', 'A'))),
    ({'A', 'B'}, 2, 2, None),
    ({'A', 'B', 'C'}, 0, 0, Permutation({'A', 'B', 'C'}, tuple())),
    ({'A', 'B', 'C'}, 0, 1, None),
    ({'A', 'B', 'C'}, 1, 0, Permutation({'A', 'B', 'C'}, ('A',))),
    ({'A', 'B', 'C'}, 1, 1, Permutation({'A', 'B', 'C'}, ('B',))),
    ({'A', 'B', 'C'}, 1, 2, Permutation({'A', 'B', 'C'}, ('C',))),
    ({'A', 'B', 'C'}, 2, 0, Permutation({'A', 'B', 'C'}, ('A', 'B'))),
    ({'A', 'B', 'C'}, 2, 1, Permutation({'A', 'B', 'C'}, ('A', 'C'))),
    ({'A', 'B', 'C'}, 2, 2, Permutation({'A', 'B', 'C'}, ('B', 'A'))),
    ({'A', 'B', 'C'}, 2, 3, Permutation({'A', 'B', 'C'}, ('B', 'C'))),
    ({'A', 'B', 'C'}, 2, 4, Permutation({'A', 'B', 'C'}, ('C', 'A'))),
    ({'A', 'B', 'C'}, 2, 5, Permutation({'A', 'B', 'C'}, ('C', 'B'))),
    ({'A', 'B', 'C'}, 2, 6, None),
    ({'A', 'B', 'C'}, 3, 0, Permutation({'A', 'B', 'C'}, ('A', 'B', 'C'))),
    ({'A', 'B', 'C'}, 3, 1, Permutation({'A', 'B', 'C'}, ('A', 'C', 'B'))),
    ({'A', 'B', 'C'}, 3, 2, Permutation({'A', 'B', 'C'}, ('B', 'A', 'C'))),
    ({'A', 'B', 'C'}, 3, 3, Permutation({'A', 'B', 'C'}, ('B', 'C', 'A'))),
    ({'A', 'B', 'C'}, 3, 4, Permutation({'A', 'B', 'C'}, ('C', 'A', 'B'))),
    ({'A', 'B', 'C'}, 3, 5, Permutation({'A', 'B', 'C'}, ('C', 'B', 'A'))),
    ({'A', 'B', 'C'}, 3, 6, None),
    ({'A', 'B', 'C', 'D'}, 0, 0, Permutation({'A', 'B', 'C', 'D'}, tuple())),
    ({'A', 'B', 'C', 'D'}, 0, 1, None),
    ({'A', 'B', 'C', 'D'}, 1, 0, Permutation({'A', 'B', 'C', 'D'}, ('A',))),
    ({'A', 'B', 'C', 'D'}, 1, 1, Permutation({'A', 'B', 'C', 'D'}, ('B',))),
    ({'A', 'B', 'C', 'D'}, 1, 2, Permutation({'A', 'B', 'C', 'D'}, ('C',))),
    ({'A', 'B', 'C', 'D'}, 1, 3, Permutation({'A', 'B', 'C', 'D'}, ('D',))),
    ({'A', 'B', 'C', 'D'}, 2, 0, Permutation({'A', 'B', 'C', 'D'}, ('A', 'B'))),
    ({'A', 'B', 'C', 'D'}, 2, 1, Permutation({'A', 'B', 'C', 'D'}, ('A', 'C'))),
    ({'A', 'B', 'C', 'D'}, 2, 2, Permutation({'A', 'B', 'C', 'D'}, ('A', 'D'))),
    ({'A', 'B', 'C', 'D'}, 2, 3, Permutation({'A', 'B', 'C', 'D'}, ('B', 'A'))),
    ({'A', 'B', 'C', 'D'}, 2, 4, Permutation({'A', 'B', 'C', 'D'}, ('B', 'C'))),
    ({'A', 'B', 'C', 'D'}, 2, 5, Permutation({'A', 'B', 'C', 'D'}, ('B', 'D'))),
    ({'A', 'B', 'C', 'D'}, 2, 6, Permutation({'A', 'B', 'C', 'D'}, ('C', 'A'))),
    ({'A', 'B', 'C', 'D'}, 2, 7, Permutation({'A', 'B', 'C', 'D'}, ('C', 'B'))),
    ({'A', 'B', 'C', 'D'}, 2, 8, Permutation({'A', 'B', 'C', 'D'}, ('C', 'D'))),
    ({'A', 'B', 'C', 'D'}, 2, 9, Permutation({'A', 'B', 'C', 'D'}, ('D', 'A'))),
    ({'A', 'B', 'C', 'D'}, 2, 10, Permutation({'A', 'B', 'C', 'D'}, ('D', 'B'))),
    ({'A', 'B', 'C', 'D'}, 2, 11, Permutation({'A', 'B', 'C', 'D'}, ('D', 'C'))),
    ({'A', 'B', 'C', 'D'}, 2, 12, None),
    ({'A', 'B', 'C', 'D'}, 3, 0, Permutation({'A', 'B', 'C', 'D'}, ('A', 'B', 'C'))),
    ({'A', 'B', 'C', 'D'}, 3, 1, Permutation({'A', 'B', 'C', 'D'}, ('A', 'B', 'D'))),
    ({'A', 'B', 'C', 'D'}, 3, 2, Permutation({'A', 'B', 'C', 'D'}, ('A', 'C', 'B'))),
    ({'A', 'B', 'C', 'D'}, 3, 3, Permutation({'A', 'B', 'C', 'D'}, ('A', 'C', 'D'))),
    ({'A', 'B', 'C', 'D'}, 3, 4, Permutation({'A', 'B', 'C', 'D'}, ('A', 'D', 'B'))),
    ({'A', 'B', 'C', 'D'}, 3, 5, Permutation({'A', 'B', 'C', 'D'}, ('A', 'D', 'C'))),
    ({'A', 'B', 'C', 'D'}, 3, 6, Permutation({'A', 'B', 'C', 'D'}, ('B', 'A', 'C'))),
    ({'A', 'B', 'C', 'D'}, 3, 7, Permutation({'A', 'B', 'C', 'D'}, ('B', 'A', 'D'))),
    ({'A', 'B', 'C', 'D'}, 3, 8, Permutation({'A', 'B', 'C', 'D'}, ('B', 'C', 'A'))),
    ({'A', 'B', 'C', 'D'}, 3, 9, Permutation({'A', 'B', 'C', 'D'}, ('B', 'C', 'D'))),
    ({'A', 'B', 'C', 'D'}, 3, 10, Permutation({'A', 'B', 'C', 'D'}, ('B', 'D', 'A'))),
    ({'A', 'B', 'C', 'D'}, 3, 11, Permutation({'A', 'B', 'C', 'D'}, ('B', 'D', 'C'))),
    ({'A', 'B', 'C', 'D'}, 3, 12, Permutation({'A', 'B', 'C', 'D'}, ('C', 'A', 'B'))),
    ({'A', 'B', 'C', 'D'}, 3, 13, Permutation({'A', 'B', 'C', 'D'}, ('C', 'A', 'D'))),
    ({'A', 'B', 'C', 'D'}, 3, 14, Permutation({'A', 'B', 'C', 'D'}, ('C', 'B', 'A'))),
    ({'A', 'B', 'C', 'D'}, 3, 15, Permutation({'A', 'B', 'C', 'D'}, ('C', 'B', 'D'))),
    ({'A', 'B', 'C', 'D'}, 3, 16, Permutation({'A', 'B', 'C', 'D'}, ('C', 'D', 'A'))),
    ({'A', 'B', 'C', 'D'}, 3, 17, Permutation({'A', 'B', 'C', 'D'}, ('C', 'D', 'B'))),
    ({'A', 'B', 'C', 'D'}, 3, 18, Permutation({'A', 'B', 'C', 'D'}, ('D', 'A', 'B'))),
    ({'A', 'B', 'C', 'D'}, 3, 19, Permutation({'A', 'B', 'C', 'D'}, ('D', 'A', 'C'))),
    ({'A', 'B', 'C', 'D'}, 3, 20, Permutation({'A', 'B', 'C', 'D'}, ('D', 'B', 'A'))),
    ({'A', 'B', 'C', 'D'}, 3, 21, Permutation({'A', 'B', 'C', 'D'}, ('D', 'B', 'C'))),
    ({'A', 'B', 'C', 'D'}, 3, 22, Permutation({'A', 'B', 'C', 'D'}, ('D', 'C', 'A'))),
    ({'A', 'B', 'C', 'D'}, 3, 23, Permutation({'A', 'B', 'C', 'D'}, ('D', 'C', 'B'))),
    ({'A', 'B', 'C', 'D'}, 3, 24, None),
    ({'A', 'B', 'C', 'D'}, 4, 0, Permutation({'A', 'B', 'C', 'D'}, ('A', 'B', 'C', 'D'))),
    ({'A', 'B', 'C', 'D'}, 4, 1, Permutation({'A', 'B', 'C', 'D'}, ('A', 'B', 'D', 'C'))),
    ({'A', 'B', 'C', 'D'}, 4, 2, Permutation({'A', 'B', 'C', 'D'}, ('A', 'C', 'B', 'D'))),
    ({'A', 'B', 'C', 'D'}, 4, 3, Permutation({'A', 'B', 'C', 'D'}, ('A', 'C', 'D', 'B'))),
    ({'A', 'B', 'C', 'D'}, 4, 4, Permutation({'A', 'B', 'C', 'D'}, ('A', 'D', 'B', 'C'))),
    ({'A', 'B', 'C', 'D'}, 4, 5, Permutation({'A', 'B', 'C', 'D'}, ('A', 'D', 'C', 'B'))),
    ({'A', 'B', 'C', 'D'}, 4, 6, Permutation({'A', 'B', 'C', 'D'}, ('B', 'A', 'C', 'D'))),
    ({'A', 'B', 'C', 'D'}, 4, 7, Permutation({'A', 'B', 'C', 'D'}, ('B', 'A', 'D', 'C'))),
    ({'A', 'B', 'C', 'D'}, 4, 8, Permutation({'A', 'B', 'C', 'D'}, ('B', 'C', 'A', 'D'))),
    ({'A', 'B', 'C', 'D'}, 4, 9, Permutation({'A', 'B', 'C', 'D'}, ('B', 'C', 'D', 'A'))),
    ({'A', 'B', 'C', 'D'}, 4, 10, Permutation({'A', 'B', 'C', 'D'}, ('B', 'D', 'A', 'C'))),
    ({'A', 'B', 'C', 'D'}, 4, 11, Permutation({'A', 'B', 'C', 'D'}, ('B', 'D', 'C', 'A'))),
    ({'A', 'B', 'C', 'D'}, 4, 12, Permutation({'A', 'B', 'C', 'D'}, ('C', 'A', 'B', 'D'))),
    ({'A', 'B', 'C', 'D'}, 4, 13, Permutation({'A', 'B', 'C', 'D'}, ('C', 'A', 'D', 'B'))),
    ({'A', 'B', 'C', 'D'}, 4, 14, Permutation({'A', 'B', 'C', 'D'}, ('C', 'B', 'A', 'D'))),
    ({'A', 'B', 'C', 'D'}, 4, 15, Permutation({'A', 'B', 'C', 'D'}, ('C', 'B', 'D', 'A'))),
    ({'A', 'B', 'C', 'D'}, 4, 16, Permutation({'A', 'B', 'C', 'D'}, ('C', 'D', 'A', 'B'))),
    ({'A', 'B', 'C', 'D'}, 4, 17, Permutation({'A', 'B', 'C', 'D'}, ('C', 'D', 'B', 'A'))),
    ({'A', 'B', 'C', 'D'}, 4, 18, Permutation({'A', 'B', 'C', 'D'}, ('D', 'A', 'B', 'C'))),
    ({'A', 'B', 'C', 'D'}, 4, 19, Permutation({'A', 'B', 'C', 'D'}, ('D', 'A', 'C', 'B'))),
    ({'A', 'B', 'C', 'D'}, 4, 20, Permutation({'A', 'B', 'C', 'D'}, ('D', 'B', 'A', 'C'))),
    ({'A', 'B', 'C', 'D'}, 4, 21, Permutation({'A', 'B', 'C', 'D'}, ('D', 'B', 'C', 'A'))),
    ({'A', 'B', 'C', 'D'}, 4, 22, Permutation({'A', 'B', 'C', 'D'}, ('D', 'C', 'A', 'B'))),
    ({'A', 'B', 'C', 'D'}, 4, 23, Permutation({'A', 'B', 'C', 'D'}, ('D', 'C', 'B', 'A'))),
    ({'A', 'B', 'C', 'D'}, 4, 24, None),
]


@pytest.mark.parametrize('universal_set, k, rank, expected', test_values)
def test_unrank_permutation(universal_set, k, rank, expected):

    actual = unrank_permutation(universal_set, k, rank)

    if actual is not None:
        assert actual._combinatoric == expected._combinatoric
        assert actual._universal_set == expected._universal_set
    else:
        assert actual == expected

# test rank_permutation
test_values = [
    (frozenset(), tuple(), 0),
    (frozenset({'A'}), tuple(), 0),
    (frozenset({'A'}), ('A', ), 0),
    (frozenset({'A', 'B'}), tuple(), 0),
    (frozenset({'A', 'B'}), ('A', ), 0),
    (frozenset({'A', 'B'}), ('B',), 1),
    (frozenset({'A', 'B'}), ('A', 'B'), 0),
    (frozenset({'A', 'B'}), ('B', 'A'), 1),
    (frozenset({'A', 'B', 'C'}), tuple(), 0),
    (frozenset({'A', 'B', 'C'}), ('A', ), 0),
    (frozenset({'A', 'B', 'C'}), ('B', ), 1),
    (frozenset({'A', 'B', 'C'}), ('C', ), 2),
    (frozenset({'A', 'B', 'C'}), ('A', 'B'), 0),
    (frozenset({'A', 'B', 'C'}), ('A', 'C'), 1),
    (frozenset({'A', 'B', 'C'}), ('B', 'A'), 2),
    (frozenset({'A', 'B', 'C'}), ('B', 'C'), 3),
    (frozenset({'A', 'B', 'C'}), ('C', 'A'), 4),
    (frozenset({'A', 'B', 'C'}), ('C', 'B'), 5),
    (frozenset({'A', 'B', 'C'}), ('A', 'B', 'C'), 0),
    (frozenset({'A', 'B', 'C'}), ('A', 'C', 'B'), 1),
    (frozenset({'A', 'B', 'C'}), ('B', 'A', 'C'), 2),
    (frozenset({'A', 'B', 'C'}), ('B', 'C', 'A'), 3),
    (frozenset({'A', 'B', 'C'}), ('C', 'A', 'B'), 4),
    (frozenset({'A', 'B', 'C'}), ('C', 'B', 'A'), 5),
    (frozenset({'A', 'B', 'C', 'D'}), tuple(), 0),
    (frozenset({'A', 'B', 'C', 'D'}), ('A', ), 0),
    (frozenset({'A', 'B', 'C', 'D'}), ('B', ), 1),
    (frozenset({'A', 'B', 'C', 'D'}), ('C', ), 2),
    (frozenset({'A', 'B', 'C', 'D'}), ('D', ), 3),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'B'), 0),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'C'), 1),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'D'), 2),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'A'), 3),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'C'), 4),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'D'), 5),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'A'), 6),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'B'), 7),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'D'), 8),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'A'), 9),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'B'), 10),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'C'), 11),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'B', 'C'), 0),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'B', 'D'), 1),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'C', 'B'), 2),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'C', 'D'), 3),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'D', 'B'), 4),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'D', 'C'), 5),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'A', 'C'), 6),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'A', 'D'), 7),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'C', 'A'), 8),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'C', 'D'), 9),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'D', 'A'), 10),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'D', 'C'), 11),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'A', 'B'), 12),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'A', 'D'), 13),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'B', 'A'), 14),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'B', 'D'), 15),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'D', 'A'), 16),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'D', 'B'), 17),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'A', 'B'), 18),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'A', 'C'), 19),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'B', 'A'), 20),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'B', 'C'), 21),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'B', 'C', 'D'), 0),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'B', 'D', 'C'), 1),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'C', 'B', 'D'), 2),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'C', 'D', 'B'), 3),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'D', 'B', 'C'), 4),
    (frozenset({'A', 'B', 'C', 'D'}), ('A',  'D', 'C', 'B'), 5),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'A', 'C', 'D'), 6),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'A', 'D', 'C'), 7),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'C', 'A', 'D'), 8),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'C', 'D', 'A'), 9),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'D', 'A', 'C'), 10),
    (frozenset({'A', 'B', 'C', 'D'}), ('B',  'D', 'C', 'A'), 11),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'A', 'B', 'D'), 12),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'A', 'D', 'B'), 13),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'B', 'A', 'D'), 14),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'B', 'D', 'A'), 15),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'D', 'A', 'B'), 16),
    (frozenset({'A', 'B', 'C', 'D'}), ('C',  'D', 'B', 'A'), 17),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'A', 'B', 'C'), 18),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'A', 'C', 'B'), 19),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'B', 'A', 'C'), 20),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'B', 'C', 'A'), 21),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'C', 'A', 'B'), 22),
    (frozenset({'A', 'B', 'C', 'D'}), ('D',  'C', 'B', 'A'), 23)
]


@pytest.mark.parametrize('universal_set, permutation, expected', test_values)
def test_rank_permutationt(universal_set, permutation, expected):

    actual = rank_permutation(universal_set, permutation)

    assert actual == expected


# test Permutation 

# test Permutation.combinatoric

test_values = [
    (Permutation(set(), tuple()), tuple()),
    (Permutation({'A'}, tuple()), tuple()),
    (Permutation({'A'}, ('A', )), ('A', )),
]


@pytest.mark.parametrize('permutation, expected', test_values)
def test_permutation_combinatoric(permutation, expected):

    actual = permutation.combinatoric

    assert actual == expected


# test Permutation.rank()
    
test_values = [
    (Permutation({'A', 'B'}, tuple()), 0),
    (Permutation({'A', 'B', 'C', 'D'}, ('A',  'C', 'D')), 3),
    (Permutation({'A', 'B', 'C', 'D'}, ('D',  'B', 'C')), 21),
    (Permutation({'A', 'B', 'C', 'D'}, ('C',  'A', 'D', 'B')), 13),
    (Permutation({'A', 'B', 'C', 'D'}, ('D',  'C', 'A', 'B')), 22),
]


@pytest.mark.parametrize('permutation, expected', test_values)
def test_permutation_rank(permutation, expected):

    actual = permutation.rank()

    assert actual == expected

# test Permutation.successor()
test_values = [
    (Permutation(set(), tuple()), None),
    (Permutation({'A'}, tuple()), None),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B'}, ('B', ))),
    (Permutation({'A', 'B', 'C', 'D'}, ('A', 'D')), Permutation({'A', 'B', 'C', 'D'}, ('B', 'A'))),
    (Permutation({'A', 'B', 'C', 'D', 'E'}, ('A', 'D', 'E')), Permutation({'A', 'B', 'C', 'D', 'E'}, ('A', 'E', 'B'))),
    (Permutation({'A', 'B', 'C', 'D', 'E'}, ('A', 'C', 'D', 'E')), Permutation({'A', 'B', 'C', 'D', 'E'}, ('A', 'C', 'E', 'B')))
]


@pytest.mark.parametrize('permutation, expected', test_values)
def test_permutation_successor(permutation, expected):

    actual = permutation.successor()

    assert actual == expected


# test Permutation.__eq__()
test_values = [
    (Permutation(set(), tuple()), Permutation(set(), tuple()), True),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B'},('B', )), False),
    (Permutation({'A', 'B', 'C', 'D'}, ('A', 'D')), Permutation({'A', 'B', 'C', 'D'}, ('A', 'D')), True),
    (Permutation({'A', 'B'}, ('A', )), ('A', ), NotImplementedError()),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B', 'C', 'D'}, ('A', )), NotImplementedError()),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B'}, ('A', 'B')), NotImplementedError())
]


@pytest.mark.parametrize('permutation_a, permutation_b, expected', test_values)
def test_permutation_eq(permutation_a, permutation_b, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            permutation_a == permutation_b
    
    else:
        
        actual = permutation_a == permutation_b

        assert actual == expected


# test Permutation.__lt__()
test_values = [
    (Permutation(set(), tuple()), Permutation(set(), tuple()), False),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B'},('B', )), True),
    (Permutation({'A', 'B', 'C', 'D'}, ('A', 'D')), Permutation({'A', 'B', 'C', 'D'}, ('A', 'D')), False),
    (Permutation({'A', 'B'}, ('A', )), ('A', ), NotImplementedError()),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B', 'C', 'D'}, ('A', )), NotImplementedError()),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B'}, ('A', 'B')), NotImplementedError())
]


@pytest.mark.parametrize('permutation_a, permutation_b, expected', test_values)
def test_permutation_lt(permutation_a, permutation_b, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            permutation_a < permutation_b
    
    else:
        
        actual = permutation_a < permutation_b

        assert actual == expected


# test Permutation.__gt__()
test_values = [
    (Permutation(set(), tuple()), Permutation(set(), tuple()), False),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B'},('B', )), False),
    (Permutation({'A', 'B', 'C', 'D'}, ('B', 'D')), Permutation({'A', 'B', 'C', 'D'}, ('A', 'D')), True),
    (Permutation({'A', 'B'}, ('A', )), ('A', ), NotImplementedError()),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B', 'C', 'D'}, ('A', )), NotImplementedError()),
    (Permutation({'A', 'B'}, ('A', )), Permutation({'A', 'B'}, ('A', 'B')), NotImplementedError())
]


@pytest.mark.parametrize('permutation_a, permutation_b, expected', test_values)
def test_permutation_gt(permutation_a, permutation_b, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            permutation_a > permutation_b
    
    else:
        
        actual = permutation_a > permutation_b

        assert actual == expected


# test PermutationIterator
test_values = [
    (PermutationIterator(set(), 0, 0), [Permutation(set(), tuple())]),
    (PermutationIterator({'A'}, 0, 0), [Permutation({'A'}, tuple())]),
    (PermutationIterator({'A'}, 1, 0), [Permutation({'A'}, ('A', ))]),
    (
        PermutationIterator({'A', 'B'}, 1, 0), 
        [
            Permutation({'A', 'B'}, ('A', )), 
            Permutation({'A', 'B'}, ('B', ))
        ]
    ),
    (
        PermutationIterator({'A', 'B'}, 1, 1), 
        [Permutation({'A', 'B'}, ('B', ))]
    ),
    (
        PermutationIterator({'A', 'B'}, 2, 0), 
        [
            Permutation({'A', 'B'}, ('A', 'B')),
            Permutation({'A', 'B'}, ('B', 'A'))
        ]
    ),
    (
        PermutationIterator({'A', 'B', 'C'}, 1, 0), 
        [
            Permutation({'A', 'B', 'C'}, ('A', )), 
            Permutation({'A', 'B', 'C'}, ('B', )),
            Permutation({'A', 'B', 'C'}, ('C', ))
        ]       
    ),
    (
        PermutationIterator({'A', 'B', 'C'}, 2, 2), 
        [
            Permutation({'A', 'B', 'C'}, ('B', 'A')),
            Permutation({'A', 'B', 'C'}, ('B', 'C')),
            Permutation({'A', 'B', 'C'}, ('C', 'A')),
            Permutation({'A', 'B', 'C'}, ('C', 'B'))
        ]       
    )
]


@pytest.mark.parametrize('permutation_iterator, expected', test_values)
def test_permutation_iterator(permutation_iterator, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            permutations = list(permutation_iterator)
    
    else:
        
        actual = list(permutation_iterator)

        assert actual == expected



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
