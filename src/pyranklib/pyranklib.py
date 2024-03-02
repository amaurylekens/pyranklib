#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Package to use lexicographic order of combinatorics. Contains:
    * Combination
    * Permuation
    * Multicombination
    * MultiPermutation
    * IntegerPartition
    * IntegerComposition
"""

from __future__ import annotations

from copy import copy
from math import comb, perm
from functools import lru_cache
from functools import total_ordering
from abc import ABC, abstractmethod
from typing import Set, Any, Optional, Tuple, FrozenSet, Hashable



def ensure_comparable(comparison_function):
    def wrapper(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError()
    
        if self._universal_set != other._universal_set:
            raise NotImplementedError()
        
        if len(self._combinatoric) != len(other._combinatoric):
            raise NotImplementedError()
        
        return comparison_function(self, other)
    
    return wrapper


class Combinatoric(ABC):

    def __init__(self, universal_set: Set[Any], combinatoric: Hashable[Any]) -> None:

        """
        K-sized combination of a universal set.

        :param universal_set: Set of distinct items
        :param combinatoric: A combinatoric from the universal set.

        :raises:
            ValueError: if at least one element of `combination` is not in
                        `universal_set`
        """

        if any(c not in universal_set for c in combinatoric):
            raise ValueError(
                "Each item of a `combinatoric` should be in `universal_set`"
            )
        
        self._universal_set = universal_set
        self._combinatoric = combinatoric


    def successor(self) -> Optional[Combination]:

        """
        Returns successor combination in lexicographic order. If there is no
        successor, a None is returned.

        :return: Successor combination in lexicographic order.
        :rtype: Optional[Combination]
        """

        rank = self.rank()
        successor = unrank_combination(
            set(self._universal_set), len(self._combinatoric), rank+1
        )

        return successor

    @abstractmethod
    def rank(self):

        pass

    @ensure_comparable
    def __eq__(self, _other: Combination) -> bool:

        return self.rank() == _other.rank()
    
    @ensure_comparable
    def __lt__(self, _other: Combination) -> bool:

        return self.rank() < _other.rank()
    
    def __hash__(self) -> int:
        
        return hash(self.rank())
    
    def __str__(self):

        return str(self._combination)



###### Combination ######
# Selection of items:
#  * without repetition
#  * order doesn't matter
#########################


def unrank_combination(
    universal_set: Set[Any], k: int, rank: int
) -> Optional[Combination]:

    """
    Returns a k-sized subset from a set of items based on a given
    lexicographic combinatorial index.

    :param universal_set: Set of distinct items.
    :type universal_set: Set

    :param k: Size of the combination
    :type k: int

    :param rank: Lexicographic combinatorial rank
    :type rank: int

    :return: k-sized combination corresponding to the given index
    :rtype: Set

    :Example:
        >>> universal_set = {'A', 'B', 'C', 'D'}
        >>> unrank_combination(universal_set, 3, 0).combination
        {A', 'B', 'C'}
        >>> unrank_combination(universal_set, 3, 1).combination
        {'A', 'C', 'D'}
    """

    combination = set()

    if rank >= comb(len(universal_set), k):
        return None

    sliced_universal_set = copy(sorted(list(universal_set)))
    for i in range(k):

        index_rank = 0
        for index in range(len(sliced_universal_set)):

            combs = comb(
                len(sliced_universal_set[index+1:]),
                k - (i + 1)
            )

            index_rank += combs

            if index_rank > rank:
                combination.add(sliced_universal_set[index])
                sliced_universal_set = sliced_universal_set[index+1:]
                rank -= (index_rank - combs)
                break

    combination = Combination(universal_set, combination)

    return combination


@lru_cache
def rank_combination(universal_set: FrozenSet[Any], combination: FrozenSet[Any]) -> int:

    """
    Compute a zero-based unique combinatorial index for a specific k-sized
    combination choosen from the n-sized `universal_set` attribute. The
    lexicographic index ranges from 0 to "n choose k" - 1.

    :param universal_set: The universal_set of the combination.
    :type universal_set: Set[Any]
    :param combination: The combination.
    :type combination: Set[Any]
    :return: Lexicograpic index of the given k-sized combination.
    :rtype: int
    """

    universal_set = sorted(list(universal_set))

    rank = 0
    for i, item in enumerate(sorted(list(combination))):

        # index of the current item in the universal set
        index = universal_set.index(item)

        for rank_index in range(index):

            # Compute the contribution to the rank
            rank += comb(
                len(universal_set[rank_index+1:]),
                len(combination) - (i + 1)
            )

        # Remove the items from the universal set for subsequent
        # calculations
        universal_set = universal_set[index+1:]

    return rank


@total_ordering
class Combination(Combinatoric):

    def __init__(self, universal_set: Set[Any], combination: Set[Any]):

        """
        K-sized combination of a universal set.

        :param universal_set: Set of distinct items
        :param combination: A combination from the universal set.
        """

        super().__init__(universal_set, combination)

    @property
    def combination(self):
        return self._combinatoric

    def rank(self) -> int:

        """
        Compute a zero-based unique combinatorial index for a specific k-sized
        combination choosen from the n-sized `universal_set` attribute. The
        lexicographic index ranges from 0 to "n choose k" - 1.

        :return: Lexicograpic index of the given k-sized combination.
        :rtype: int
        """

        return rank_combination(frozenset(self._universal_set), frozenset(self._combinatoric))


class CombinationIterator:

    def __init__(
        self, universal_set: Set[Any], k: int, initial_index: int = 0
    ):

        """
        Lexicographic order combination iterator.

        :param universal_set: Set of distinct items.
        :type universal_set: Set[Any]

        :param k: Size of the combination
        :type k: int

        :param initial_index: initial lexicographic index for the iterator. 0
                              by default.
        :type initial_index: int
        """

        self._combination = unrank_combination(universal_set, k, initial_index)

    def __iter__(self):
        return self

    def __next__(self):

        current = self._combination

        if current:
            successor = self._combination.successor()
            self._combination = successor
            return current

        else:
            raise StopIteration
        


###### Permutation ######
# k-sized tuple of items:
#  * without repetition
#  * order does matter
#########################


def unrank_permutation(
    universal_set: Set[Any], k: int, index: int
) -> Optional[Permutation]:

    """
    Returns a k-sized permutation from a set of items based on a given
    lexicographic combinatorial index.

    :param universal_set: Set of distinct items.
    :type universal_set: Set

    :param k: Size of the permutation
    :type k: int

    :param index: Lexicographic permutation index
    :type index: int

    :return: k-sized combination corresponding to the given index
    :rtype: Set

    :Example:
        >>> universal_set = {'A', 'B', 'C', 'D'}
        >>> unrank_permutation(universal_set, 3, 0)
        {'A', 'B', 'C'}
        >>> unrank_permutation(universal_set, 3, 1)
        {'A', 'C', 'D'}
    """

    sliced_universal_set = sorted(list(universal_set))
    permutation = list()

    if index >= perm(len(universal_set), k):
        return None

    for i in range(k):

        offset = 0
        for j, item in enumerate(sliced_universal_set):

            if offset + perm(len(sliced_universal_set)-1, k-(i+1)) > index:

                index -= offset
                permutation.append(sliced_universal_set[j])
                sliced_universal_set.pop(j)
                break

            else:
                offset += perm(len(sliced_universal_set)-1, k-(i+1))

    permutation = Permutation(universal_set, tuple(permutation))

    return permutation


@lru_cache
def rank_permutation(universal_set: FrozenSet[Any], permutation: Tuple[Any, ...]) -> int:
    
    """
    Compute a zero-based unique permutation rank for a specific k-sized
    permutation choosen from the n-sized `universal_set` attribute. The
    lexicographic rank ranges from 0 to "n perm k" - 1.

    :param universal_set: The universal_set of the permutation.
    :type universal_set: Set[Any]
    :param combination: The permutation.
    :type combination: Tuple[Any]
    :return: Lexicograpic rank of the given k-sized permutation.
    :rtype: int
    """

    rank = 0
    for i, item in enumerate(permutation):
        # index of the current item in the universal set
        index = universal_set.index(item)

        # Calculate the contribution to the rank
        rank += index * perm(
            len(universal_set) - 1,
            len(permutation) - 1 - i
        )

        # Remove the item from the universal set for subsequent calculations
        universal_set.remove(item)

    return rank


@total_ordering
class Permutation(Combinatoric):

    def __init__(self, universal_set: Set[Any], combinatoric: Tuple[Any, ...]):

        """
        K-sized permutation of a universal set.

        :param universal_set: Set of distinct items
        :param combinatoric: A permutation from the universal set.
        """

        super().__init__(universal_set, combinatoric)

    @property
    def permutation(self):
        return self._combinatoric

    def rank(self) -> int:

        """
        Compute a zero-based unique permutation rank for a specific k-sized
        permutation choosen from the n-sized `universal_set` attribute. The
        lexicographic rank ranges from 0 to "n perm k" - 1.

        :return: Lexicograpic rank of the given k-sized permutation.
        :rtype: int
        """

        return rank_combination(tuple(self._universal_set), frozenset(self._combinatoric))


class PermuationIterator:

    def __init__(
        self, universal_set: Set[Any], k: int, initial_index: int = 0
    ):

        """
        Lexicographic order combination iterator.

        :param universal_set: Set of distinct items.
        :type universal_set: Set[Any]

        :param k: Size of the combination
        :type k: int

        :param initial_index: initial lexicographic index for the iterator. 0
                              by default.
        :type initial_index: int
        """

        self._permuation = unrank_permutation(universal_set, k, initial_index)

    def __iter__(self):
        return self

    def __next__(self):

        current = self._permuation

        if current:
            successor = self._permuation.successor()
            self._permuation = successor
            return current

        else:
            raise StopIteration


#### Integer composition ####
# k_sized tuple that sum to n
#   * repetition allowed
#   * order does matter

def unrank_sized_integer_composition(
    n: int, k: int, index: int
) -> Optional[SizedIntegerComposition]:

    """
    Returns a `k`-sized interger composition that sums to `n` based on a given
    lexicographic combinatorial index.

    :param n: Composition sum.
    :type n: int

    :param k: Size of the composition.
    :type k: int

    :param index: Index of the composition
    :type: index: int

    :return: Composition at the index `index`.
    :rtype: int
    """

    if index >= comb(n-1, k-1):
        return None

    composition = list()

    for i in range(k-1):

        offset = 0
        for j in range(1, n-1):

            if offset + comb(n - (sum(composition) + j) - 1, k - i - 2) > index:

                index -= offset
                composition.append(j)
                break

            else:
                offset += comb(n - (sum(composition) + j) - 1, k - i - 2)

    composition.append(n-sum(composition))

    composition = SizedIntegerComposition(tuple(composition))
    return composition


class SizedIntegerComposition:

    def __init__(self, composition: Tuple[int, ...]):

        """
        K-sized integer composition.

        :param composition: A k-sized integer composition.
        """

        self._composition = composition
        self._sum = sum(composition)

    @property
    def composition(self):
        return self._composition

    def __str__(self):

        return str(self._composition)

    def rank(self):

        k = len(self._composition)
        index = 0

        for i in range(k - 1):
            index += sum(
                comb(
                    self._sum - (sum(self._composition[:i]) + j) - 1,
                    k - i - 2
                )
                for j in range(1, self._composition[i])
            )

        return index

    def successor(self) -> Optional[SizedIntegerComposition]:
        """
        Returns successor combination in lexicographic order. If there is no
        successor, a None is returned.

        :return: Successor combination in lexicographic order.
        :rtype: Optional[Combination]
        """

        rank = self.rank()
        successor = unrank_sized_integer_composition(
            self._sum, len(self._composition), rank + 1
        )

        return successor


class SizedIntegerCompositionIterator:

    def __init__(
        self, n: int, k: int, initial_index: int = 0
    ):

        """
        Lexicographic order combination iterator.

        :param n: Composition sum.
        :type n: int

        :param k: Size of the composition
        :type k: int

        :param initial_index: initial lexicographic index for the iterator. 0
                              by default.
        :type initial_index: int
        """

        self._composition = unrank_sized_integer_composition(
            n, k, initial_index
        )

    def __iter__(self):
        return self

    def __next__(self):

        current = self._composition

        if current:
            successor = self._composition.successor()
            self._composition = successor
            return current

        else:
            raise StopIteration


#### Sized Integer partition ####
# k_sized set that sum to n
#   * repetition allowed
#   * order doesn't matter


def part(n, k, l):

    if n < k or k <= 0:
        return 0

    if k == n or k == 1:
        return 1

    return part(n - l, k - 1, l) + part(n - l*k, k, 1)


def unrank_sized_integer_partition(
    n: int, k: int, index: int
) -> Optional[SizedIntegerPartition]:

    """
    Returns a `k`-sized interger partition that sums to `n` based on a given
    lexicographic combinatorial index.

    :param n: Composition sum.
    :type n: int

    :param k: Size of the composition.
    :type k: int

    :param index: Index of the composition
    :type: index: int

    :return: Composition at the index `index`.
    :rtype: int
    """

    if index >= part(n, k, 1):
        return None

    partition = set()

    start_range = 1
    for i in range(k-1):

        for j in range(start_range, n-1):

            part_count = part(n - (sum(partition) + j), k - i - 1, j)
            if index // part_count >= 1:

                index -= part_count

            else:
                partition.add(j)
                start_range = j
                break

    partition.add(n-sum(partition))

    partition = SizedIntegerPartition(partition)
    return partition


class SizedIntegerPartition:

    def __init__(self, partition: Set[int]):

        """
        K-sized integer partition.

        :param partition: A k-sized integer partition.
        """

        self._partition = partition
        self._sum = sum(partition)

    @property
    def partition(self):
        return self._partition

    def __str__(self):

        return str(self._partition)

    def rank(self):

        k = len(self._partition)
        index = 0

        sorted_partition = sorted(list(self._partition))
        start_range = 1
        for i in range(k - 1):
            index += sum(
                part(
                    self._sum - (sum(sorted_partition[:i]) + j),
                    k - i - 1,
                    j
                )
                for j in range(start_range, sorted_partition[i])
            )
            start_range = sorted_partition[i]

        return index

    def successor(self) -> Optional[SizedIntegerComposition]:
        """
        Returns successor combination in lexicographic order. If there is no
        successor, a None is returned.

        :return: Successor combination in lexicographic order.
        :rtype: Optional[Combination]
        """

        rank = self.rank()
        successor = unrank_sized_integer_partition(
            self._sum, len(self._partition), rank + 1
        )

        return successor


###### MultiPermutation ######
# k-sized tuple of items:
#  * with repetition
#  * order does matter
#########################


def unrank_multipermutation(
    universal_set: Set[Any], k: int, index: int
) -> Optional[Multipermutation]:

    """
    Returns a k-sized multi-permutation (permutation with repetition) from a
    set of items based on a given lexicographic multi-permutation rank.

    :param universal_set: Set of distinct items.
    :type universal_set: Set

    :param k: Size of the multi-permutation
    :type k: int

    :param index: Lexicographic multi-permutation rank
    :type index: int

    :return: k-sized multi-combination object corresponding to the given index
    :rtype: Multipermutation

    :Example:
        >>> universal_set = {'A', 'B', 'C', 'D'}
        >>> unrank_multipermutation(universal_set, 3, 0).permutation
        ('A', 'A', 'A')
        >>> unrank_multipermutation(universal_set, 3, 1).permutation
        ('A', 'A', 'B')
    """

    sorted_items = sorted(universal_set)
    permutation = list()

    if index >= pow(len(universal_set), k):
        return None

    for i in range(k):

        offset = 0
        for j, item in enumerate(sorted_items):

            if offset + pow(len(sorted_items), k - (i + 1)) > index:

                index -= offset
                permutation.append(sorted_items[j])
                break

            else:
                offset += pow(len(sorted_items), k - (i + 1))

    permutation = Multipermutation(universal_set, tuple(permutation))

    return permutation


class Multipermutation:

    def __init__(self, universal_set: Set[Any], permutation: Tuple[Any, ...]):

        """
        K-sized multi-permutation of a universal set.

        :param universal_set: Set of distinct items
        :param permutation: A multi-permutation from the universal set.

        :raises:
            ValueError: if at least one element of `permutation` is not in
                        `universal_set`
        """

        self._universal_set = sorted(universal_set)
        self._permutation = permutation

        if any(p not in universal_set for p in permutation):
            raise ValueError(
                "Each item of `permuation` should be in `universal_set`"
            )

    @property
    def permutation(self):
        return self._permutation

    def __str__(self):

        return str(self._permutation)

    def rank(self) -> int:

        """
        Compute a zero-based unique multi-permutation rank for a specific
        k-sized multi-permutation choosen from the n-sized `universal_set`
        attribute. The lexicographic rank ranges from 0 to "n pow k" - 1.

        :return: Lexicograpic rank of the given k-sized multi-combination.
        :rtype: int
        """

        rank = 0
        for i, item in enumerate(self._permutation):
            # index of the current item in the universal set
            index = self._universal_set.index(item)

            # Calculate the contribution to the rank
            rank += index * pow(
                len(self._universal_set),
                len(self._permutation) - (i + 1)
            )

        return rank

    def successor(self) -> Optional[Multipermutation]:

        """
        Returns successor multi-permutation in lexicographic order. If there is
        no successor, a None is returned.

        :return: Successor permutation in lexicographic order.
        :rtype: Optional[Combination]
        """

        rank = self.rank()
        successor = unrank_multipermutation(
            set(self._universal_set), len(self.permutation), rank+1
        )

        return successor


class MultiPermuationIterator:

    def __init__(
        self, universal_set: Set[Any], k: int, initial_index: int = 0
    ):

        """
        Lexicographic order combination iterator.

        :param universal_set: Set of distinct items.
        :type universal_set: Set[Any]

        :param k: Size of the combination
        :type k: int

        :param initial_index: initial lexicographic index for the iterator. 0
                              by default.
        :type initial_index: int
        """

        self._permuation = unrank_permutation(universal_set, k, initial_index)

    def __iter__(self):
        return self

    def __next__(self):

        current = self._permuation

        if current:
            successor = self._permuation.successor()
            self._permuation = successor
            return current

        else:
            raise StopIteration


###### MultiCombination ######
# k-sized tuple of items:
#  * with repetition
#  * order doesn't matter
#########################


def unrank_multicombination(
    universal_set: Set[Any], k: int, rank: int
) -> Optional[MultiCombination]:

    """
    Returns a k-sized subset from a set of items based on a given
    lexicographic combinatorial index.

    :param universal_set: Set of distinct items.
    :type universal_set: Set

    :param k: Size of the multicombination
    :type k: int

    :param rank: Lexicographic combinatorial rank
    :type rank: int

    :return: k-sized multicombination corresponding to the given rank
    :rtype: Set

    :Example:
        >>> universal_set = {'A', 'B', 'C', 'D'}
        >>> unrank_multicombination(universal_set, 3, 0).combination
        (A', 'A', 'A')
        >>> unrank_multicombination(universal_set, 3, 1).combination
        ('A', 'A', 'B')
    """

    multicombination = list()

    if rank > comb(len(universal_set) + k - 1, k):
        return None

    universal_set = sorted(list(universal_set))
    for i in range(k):

        for index in range(len(universal_set)):

            index_rank = index * comb(
                (len(universal_set) + k - 1) - 1,
                k - (i + 1)
            )

            if index_rank > rank:
                multicombination.append(universal_set[index-1])

    multicombination = MultiCombination(
        set(universal_set), tuple(multicombination)
    )

    return multicombination


class MultiCombination:

    def __init__(
        self, universal_set: Set[Any], multicombination: Tuple[Any, ...]
    ):

        """
        K-sized combination of a universal set.

        :param universal_set: Set of distinct items
        :param multicombination: A combination from the universal set.

        :raises:
            ValueError: if at least one element of `multicombination` is not in
                        `universal_set`
        """

        self._universal_set = sorted(universal_set)
        self._multicombination = multicombination

        if any(c not in universal_set for c in multicombination):
            raise ValueError(
                "Each item of `multicombination` should be in `universal_set`"
            )

    @property
    def combination(self) -> Tuple[Any, ...]:
        return self._multicombination

    def __str__(self):

        return str(self._multicombination)

    def rank(self) -> int:

        """
        Compute a zero-based unique combinatorial index for a specific k-sized
        multicombination choosen from the n-sized `universal_set` attribute.
        The lexicographic index ranges from 0 to "(n + k -1) choose k" - 1.

        :return: Lexicograpic index of the given k-sized combination.
        :rtype: int
        """

        # Calculate the combinatorial index for the given k-subset
        rank = 0
        for i, item in enumerate(sorted(list(self._multicombination))):

            # index of the current item in the universal set
            index = self._universal_set.index(item)

            # Compute the contribution to the rank
            rank += index * comb(
                len(self._universal_set) - 1,
                len(self._multicombination) - (i + 1)
            )

        return rank

    def successor(self) -> Optional[Combination]:

        """
        Returns successor combination in lexicographic order. If there is no
        successor, a None is returned.

        :return: Successor combination in lexicographic order.
        :rtype: Optional[Combination]
        """

        rank = self.rank()
        successor = unrank_multicombination(
            set(self._universal_set), len(self._multicombination), rank+1
        )

        return successor


class MultiCombinationIterator:

    def __init__(
        self, universal_set: Set[Any], k: int, initial_index: int = 0
    ):

        """
        Lexicographic order multicombination iterator.

        :param universal_set: Set of distinct items.
        :type universal_set: Set[Any]

        :param k: Size of the multicombination
        :type k: int

        :param initial_index: initial lexicographic index for the iterator. 0
                              by default.
        :type initial_index: int
        """

        self._multicombination = unrank_multicombination(
            universal_set, k, initial_index
        )

    def __iter__(self):
        return self

    def __next__(self):

        current = self._multicombination

        if current:
            successor = self._multicombination.successor()
            self._multicombination = successor
            return current

        else:
            raise StopIteration


if __name__ == '__main__':

    for i in range(130):
        combination = unrank_combination({'A', 'B', 'C', 'D'}, 2, 5)

        print(i, '->', combination.combination, '->', combination.rank())



