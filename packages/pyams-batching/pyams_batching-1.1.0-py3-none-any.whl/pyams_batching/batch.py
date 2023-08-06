#
# Copyright (c) 2008-2015 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_batching.batch module

"""

from zope.interface import implementer
from zope.interface.common.sequence import IFiniteSequence
from zope.schema.fieldproperty import FieldProperty

from pyams_batching.interfaces import IBatch
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'


@factory_config(provided=IBatch)
class Batch:
    """Batch implementation. See IBatch"""

    start = FieldProperty(IBatch['start'])
    size = FieldProperty(IBatch['size'])
    end = FieldProperty(IBatch['end'])

    batches = None

    def __init__(self, sequence, start=0, size=20, batches=None):
        self.sequence = sequence
        length = len(sequence)
        self.update(length, start, size)
        self.update_batches(batches)

    def update(self, length, start, size):
        """Update batch"""
        # See interfaces.IBatch
        self._length = length
        self.start = start
        if length == 0:
            self.start = -1
        elif start >= length:
            raise IndexError('start index key out of range')
        # See interfaces.IBatch
        self.size = size
        self._true_size = size
        if start + size >= length:
            self._true_size = length - start
        # See interfaces.IBatch
        if length == 0:
            self.end = -1
        else:
            self.end = start + self._true_size - 1

    def update_batches(self, batches):
        """Update batches list"""
        if batches is None:
            batches = Batches(self)
        self.batches = batches

    @property
    def index(self):
        """Get current page position"""
        return self.start // self.size

    @property
    def number(self):
        """See interfaces.IBatch"""
        return self.index + 1

    @property
    def total(self):
        """See interfaces.IBatch"""
        total = self._length // self.size
        if self._length % self.size:
            total += 1
        return total

    @property
    def next(self):
        """Get next batch"""
        try:
            return self.batches[self.index + 1]
        except IndexError:
            return None

    @property
    def previous(self):
        """Get previous batch"""
        idx = self.index - 1
        if idx >= 0:
            return self.batches[idx]
        return None

    @property
    def first_element(self):
        """See interfaces.IBatch"""
        return self.sequence[self.start]

    @property
    def last_element(self):
        """See interfaces.IBatch"""
        return self.sequence[self.end]

    def __getitem__(self, key):
        """See zope.interface.common.sequence.IMinimalSequence"""
        if isinstance(key, slice):
            return self.__getslice__(*key.indices(self._true_size))
        if key >= self._true_size:
            raise IndexError('batch index out of range')
        return self.sequence[self.start + key]

    def __iter__(self):
        """See zope.interface.common.sequence.IMinimalSequence"""
        return iter(self.sequence[self.start: self.end + 1])

    def __len__(self):
        """See zope.interface.common.sequence.IFiniteSequence"""
        return self._true_size

    def __contains__(self, item):
        for i in self:
            if item == i:
                return True
        return False

    def __getslice__(self, i, j, k=1):
        if k != 1:
            raise ValueError('extended slicing not supported', k)
        if j > self.end:
            j = self._true_size
        return [self[idx] for idx in range(i, j)]

    def __eq__(self, other):
        return ((self.size, self.start, self.sequence) ==
                (other.size, other.start, other.sequence))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<%s start=%i, size=%i>' % (
            self.__class__.__name__, self.start, self.size)


@implementer(IFiniteSequence)
class Batches:
    """A sequence object representing all the batches.

    Used by a Batch.
    """

    def __init__(self, batch):
        self.size = batch.size
        self.total = batch.total
        self.sequence = batch.sequence
        self._batches = {batch.index: batch}

    def __len__(self):
        return self.total

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__getslice__(*key.indices(self.total))
        if key not in self._batches:
            if key < 0:
                key = self.total + key

            batch = Batch(
                self.sequence, key * self.size, self.size, self)
            self._batches[batch.index] = batch

        try:
            return self._batches[key]
        except KeyError:
            raise IndexError(key)

    def __getslice__(self, i, j, k=1):
        if k != 1:
            raise ValueError('extended slicing not supported')
        j = min(j, self.total)
        return [self[idx] for idx in range(i, j)]


def first_neighbours_last(batches, current_batch_idx, nb_left, nb_right):
    """Build a sublist from a large batch list.

    This is used to display batch links for a large table.

    arguments:
     * :param batches: a large sequence (may be a batches as well)
     * :param current_batch_idx: index of the current batch or item
     * :param nb_left: number of neighbours before the current batch
     * :param nb_right: number of neighbours after the current batch

    The returned list gives:
     * the first batch
     * a None separator if necessary
     * left neighbours of the current batch
     * the current batch
     * right neighbours of the current batch
     * a None separator if necessary
     * the last batch

    Example:

      >>> from pyams_batching.batch import first_neighbours_last as f_n_l
      >>> batches = range(100) # it works with real batches as well

    We try to get subsets at different levels:

      >>> for i in range(0,6):
      ...    f_n_l(batches, i, 2, 2)
      [0, 1, 2, None, 99]
      [0, 1, 2, 3, None, 99]
      [0, 1, 2, 3, 4, None, 99]
      [0, 1, 2, 3, 4, 5, None, 99]
      [0, None, 2, 3, 4, 5, 6, None, 99]
      [0, None, 3, 4, 5, 6, 7, None, 99]

      >>> for i in range(93, 99):
      ...    f_n_l(batches, i, 2, 2)
      [0, None, 91, 92, 93, 94, 95, None, 99]
      [0, None, 92, 93, 94, 95, 96, None, 99]
      [0, None, 93, 94, 95, 96, 97, None, 99]
      [0, None, 94, 95, 96, 97, 98, 99]
      [0, None, 95, 96, 97, 98, 99]
      [0, None, 96, 97, 98, 99]

    Try with no previous and no next batch:

      >>> f_n_l(batches, 0, 0, 0)
      [0, None, 99]
      >>> f_n_l(batches, 1, 0, 0)
      [0, 1, None, 99]
      >>> f_n_l(batches, 2, 0, 0)
      [0, None, 2, None, 99]

    Try with only 1 previous and 1 next batch:

      >>> f_n_l(batches, 0, 1, 1)
      [0, 1, None, 99]
      >>> f_n_l(batches, 1, 1, 1)
      [0, 1, 2, None, 99]
      >>> f_n_l(batches, 2, 1, 1)
      [0, 1, 2, 3, None, 99]
      >>> f_n_l(batches, 3, 1, 1)
      [0, None, 2, 3, 4, None, 99]

    Try with incoherent values:

      >>> f_n_l(batches, 0, -4, -10)
      Traceback (most recent call last):
      ...
      AssertionError
      >>> f_n_l(batches, 2000, 3, 3)
      Traceback (most recent call last):
      ...
      AssertionError
    """
    sublist = []
    # setup some batches and indexes
    first_idx = 0
    last_idx = len(batches) - 1
    assert 0 <= current_batch_idx <= last_idx
    assert nb_left >= 0 and nb_right >= 0
    prev_idx = current_batch_idx - nb_left
    next_idx = current_batch_idx + 1
    first_batch = batches[0]
    last_batch = batches[last_idx]

    # add first batch
    if first_idx < current_batch_idx:
        sublist.append(first_batch)

    # there must probably be space
    if first_idx + 1 < prev_idx:
        # we skip batches between first batch and first previous batch
        sublist.append(None)

    # add previous batches
    for i in range(prev_idx, prev_idx + nb_left):
        if first_idx < i:
            # append previous batches
            sublist.append(batches[i])

    # add current batch
    sublist.append(batches[current_batch_idx])

    # add next batches
    for i in range(next_idx, next_idx + nb_right):
        if i < last_idx:
            # append previous batch
            sublist.append(batches[i])

    # there must probably be space
    if next_idx + nb_right < last_idx:
        # we skip batches between last batch and last next batch
        sublist.append(None)

    # add last batch
    if current_batch_idx < last_idx:
        sublist.append(last_batch)
    return sublist
