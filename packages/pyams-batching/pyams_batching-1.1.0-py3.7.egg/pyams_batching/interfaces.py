#
# Copyright (c) 2008-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_batching.interfaces module

This module defines all package interfaces.
"""

from zope.interface import Attribute
from zope.interface.common.sequence import IFiniteSequence
from zope.schema import Field, Int


__docformat__ = 'restructuredtext'


class IBatch(IFiniteSequence):
    """A Batch represents a sub-list of the full sequence.

    The Batch constructor takes a list (or any list-like object) of elements,
    a starting index and the size of the batch. From this information all
    other values are calculated.
    """

    sequence = Attribute('Sequence')

    batches = Attribute('Batches')

    start = Int(title='Start Index',
                description='The index of the sequence at which the batch starts. '
                            'If the full sequence is empty, the value is -1.',
                min=-1,
                default=0,
                required=True)

    size = Int(title='Batch Size',
               description='The maximum size of the batch.',
               min=1,
               default=20,
               required=True)

    end = Int(title='End Index',
              description='The index of the sequence at which the batch ends.',
              min=-1,
              default=0,
              readonly=True,
              required=True)

    index = Int(title='Current Batch Index',
                description='The index of the batch in relation to all batches.',
                min=0,
                readonly=True,
                required=True)

    number = Int(title='Current Batch Number',
                 description='The number of the batch in relation to all batches.',
                 min=1,
                 readonly=True,
                 required=True)

    total = Int(title='Total Number of Batches',
                description='The total number of batches available.',
                min=1,
                readonly=True,
                required=True)

    next = Field(title='Next Batch',
                 description='The next batch of the sequence; ``None`` if last.',
                 readonly=True,
                 required=True)

    previous = Field(title='Previous Batch',
                     description='The previous batch of the sequence; ``None`` if first.',
                     readonly=True,
                     required=True)

    first_element = Field(title='First Element',
                          description='The first element of the batch.',
                          readonly=True,
                          required=True)

    total_elements = Int(title='Total Number of Elements',
                         description='Return the length of the full sequence.',
                         min=1,
                         readonly=True,
                         required=True)

    def __iter__(self):
        """Creates an iterator for the contents of the batch."""

    def __contains__(self, item):
        """ `x.__contains__(item)` <==> `item in x` """

    def __eq__(self, other):
        """`x.__eq__(other)` <==> `x == other`"""

    def __ne__(self, other):
        """`x.__ne__(other)` <==> `x != other`"""
