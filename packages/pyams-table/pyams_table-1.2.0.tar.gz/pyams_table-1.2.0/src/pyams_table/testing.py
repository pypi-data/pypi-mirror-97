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

"""PyAMS_table.testing module

This module provides testing helpers.
"""

from datetime import datetime

from pyramid.interfaces import IRequest
from zope.container.btree import BTreeContainer
from zope.container.contained import Contained
from zope.container.interfaces import IContainer
from zope.container.ordered import OrderedContainer as BaseOrderedContainer
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface, implementer

from pyams_table.column import Column, add_column
from pyams_table.interfaces import ISequenceTable, ITable, IValues
from pyams_table.table import Table
from pyams_table.value import ValuesForContainer, ValuesForSequence


__docformat__ = "reStructuredText"


class TitleColumn(Column):
    """Title column"""

    weight = 10
    header = "Title"

    def render_cell(self, item):
        """Render cell"""
        return u"Title: %s" % item.title


class NumberColumn(Column):
    """Number column"""

    header = "Number"
    weight = 20

    def get_sort_key(self, item):
        """Get item sort key"""
        return item.number

    def render_cell(self, item):
        """Render column cell"""
        return "number: %s" % item.number


class Container(BTreeContainer):
    """Sample container"""

    __name__ = "container"


class OrderedContainer(BaseOrderedContainer):
    """Sample container."""

    __name__ = "container"


class Content(Contained):
    """Sample content"""

    def __init__(self, title, number):
        self.title = title
        self.number = number


class SimpleTable(Table):
    """Simple testing table"""

    def setup_columns(self):
        return [
            add_column(self, TitleColumn, "title",
                       cell_renderer=cell_renderer,
                       head_cell_renderer=head_cell_renderer,
                       weight=1),
            add_column(self, NumberColumn, name="number", weight=2, header="Number"),
        ]


def head_cell_renderer():
    """Head cell renderer"""
    return "My items"


def cell_renderer(item):
    """Simple cell renderer"""
    return "%s item" % item.title


@implementer(IZopeDublinCore)
class DublinCoreAdapterStub:
    """Dublin core adapter stub."""

    def __init__(self, context):
        pass

    title = "faux title"
    size = 1024
    created = datetime(2001, 1, 1, 1, 1, 1)
    modified = datetime(2002, 2, 2, 2, 2, 2)


def setup_adapters(registry):
    """Adapters registry"""
    registry.registerAdapter(ValuesForContainer,
                             (IContainer, IRequest, ITable),
                             provided=IValues)
    registry.registerAdapter(ValuesForSequence,
                             (Interface, IRequest, ISequenceTable),
                             provided=IValues)
    registry.registerAdapter(DublinCoreAdapterStub,
                             (Interface,),
                             provided=IZopeDublinCore)
