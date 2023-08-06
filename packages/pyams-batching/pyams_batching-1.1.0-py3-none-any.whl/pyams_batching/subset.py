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

"""PyAMS_batching.subset module

Batching implementation for subsets.

Sometimes subsets can have pre-batched values.
"""

from pyams_batching.batch import Batch, Batches


__docformat__ = 'restructuredtext'


EMPTY_BATCH_ERROR = "EmptyBatch holds no item"


class EmptyBatch(Batch):
    """Empty batch"""

    def __init__(self, length, start, size, batches):
        # pylint: disable=super-init-not-called
        self.update(length, start, size)
        self.batches = batches

    def __eq__(self, other):
        return ((self.size, self.start, self._length) ==
                (other.size, other.start, other._length))

    @property
    def first_element(self):
        raise ValueError(EMPTY_BATCH_ERROR)

    @property
    def last_element(self):
        raise ValueError(EMPTY_BATCH_ERROR)

    def __getitem__(self, key):
        raise ValueError(EMPTY_BATCH_ERROR)

    def __iter__(self):
        raise ValueError(EMPTY_BATCH_ERROR)


class SubsetBatches(Batches):
    """Subset batches"""

    def __init__(self, batch):
        super(SubsetBatches, self).__init__(batch)
        self.length = batch._length

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__getslice__(*key.indices(self.total))
        if key not in self._batches:
            if key < 0:
                key = self.total + key

            batch = EmptyBatch(
                self.length, key * self.size, self.size, self)
            self._batches[batch.index] = batch

        try:
            return self._batches[key]
        except KeyError:
            raise IndexError(key)


class SubsetBatch(Batch):
    """Subset batch"""

    def __init__(self, sequence, length, start=0, size=20, batches=None):
        # pylint: disable=super-init-not-called,too-many-arguments
        self.sequence = sequence
        self.update(length, start, size)
        self.update_batches(batches)

    def update_batches(self, batches):
        if batches is None:
            batches = SubsetBatches(self)

        self.batches = batches

    @property
    def first_element(self):
        """See interfaces.IBatch"""
        return self.sequence[0]

    @property
    def last_element(self):
        """See interfaces.IBatch"""
        return self.sequence[-1]

    def __getitem__(self, key):
        """See zope.interface.common.sequence.IMinimalSequence"""
        if isinstance(key, slice):
            return self.__getslice__(*key.indices(self._true_size))
        if key >= self._true_size:
            raise IndexError('batch index out of range')
        return self.sequence[key]

    def __iter__(self):
        """See zope.interface.common.sequence.IMinimalSequence"""
        return iter(self.sequence)

    def __eq__(self, other):
        return ((self.size, self.start, self._length) ==
                (other.size, other.start, other._length))
