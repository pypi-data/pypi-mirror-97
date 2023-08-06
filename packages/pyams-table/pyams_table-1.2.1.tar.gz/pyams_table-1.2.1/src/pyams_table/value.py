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

"""PyAMS_table.value module

This module provides several default values adapters.
"""

from pyramid.interfaces import IRequest
from zope.container.interfaces import IContainer
from zope.interface import Interface, implementer

from pyams_table.interfaces import ISequenceTable, ITable, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config


__docformat__ = "reStructuredText"


@implementer(IValues)
class ValuesMixin(ContextRequestViewAdapter):
    """Mixin for different value adapters"""


@adapter_config(required=(IContainer, IRequest, ITable), provides=IValues)
class ValuesForContainer(ValuesMixin):
    """Values adapter from a simple IContainer"""

    @property
    def values(self):
        """Get container values"""
        return self.context.values()


@adapter_config(required=(Interface, IRequest, ISequenceTable), provides=IValues)
class ValuesForSequence(ValuesMixin):
    """Values adapter from a simple sequence table"""

    @property
    def values(self):
        """Get sequence values"""
        return self.context
