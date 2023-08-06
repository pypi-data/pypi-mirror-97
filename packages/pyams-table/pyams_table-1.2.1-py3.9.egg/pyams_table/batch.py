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

"""PyAMS_table.batch module

This module provides batch features for tables, using PyAMS_batching package.
"""

from pyramid.encode import urlencode
from pyramid.interfaces import IRequest
from zope.interface import Interface

from pyams_batching.batch import first_neighbours_last
from pyams_table.interfaces import IBatchProvider, ITable
from pyams_utils.adapter import adapter_config
from pyams_utils.url import absolute_url


@adapter_config(name='batch',
                required=(Interface, IRequest, ITable),
                provides=IBatchProvider)
class BatchProvider:
    """Batch content provider

    A batch provider is responsible for rendering the batch HTML and not for
    batching. The batch setup is directly done in the table. A batch provider
    get only used if the table rows is a batch.

    This batch provider offers a batch presentation for a given table. The
    batch provides different configuration options which can be overriden in
    custom implementations:

    The batch acts like this. If we have more batches than
    (prev_batch_size + next_batch_size + 3) then the advanced batch subset is used.
    Otherwise, we will render all batch links.
    Note, the additional factor 3 is the placeholder for the first, current and
    last item.

    Such a batch looks like:

    Renders the link for the first batch, spacers, the amount of links for
    previous batches, the current batch link, spacers, the amount of links for
    previous batches and the link for the last batch.

    Sample for 1000 items with 100 batches with batchSize of 10 and a
    prev_batch_size of 3 and a next_batch_size of 3:

    For the first item:
    [*1*][2][3][4] ... [100]

    In the middle:
    [1] ... [6][7][8][*9*][10][11][12] ... [100]

    At the end:
    [1] ... [97][98][99][*100*]
    """

    batch_items = []

    prev_batch_size = 3
    next_batch_size = 3
    batch_spacer = u"..."

    _request_args = ["%(prefix)s-sort-on", "%(prefix)s-sort-order"]

    def __init__(self, context, request, table):
        self.__parent__ = context
        self.context = context
        self.request = request
        self.table = table
        self.batch = table.rows
        self.batches = table.rows.batches

    def get_query_string_args(self):
        """Collect additional terms from the request to include in links.

        API borrowed from pyams_table.header.ColumnHeader.
        """
        args = {}
        for key in self._request_args:
            key = key % dict(prefix=self.table.prefix)
            value = self.request.params.get(key, None)
            if value:
                args.update({key: value})
        return args

    def render_batch_link(self, batch, css_class=None):
        """Render batch link"""
        args = self.get_query_string_args()
        args[self.table.prefix + "-batch-start"] = batch.start
        args[self.table.prefix + "-batch-size"] = batch.size
        query = urlencode(sorted(args.items()))
        table_url = absolute_url(self.table, self.request)
        idx = batch.index + 1
        css = ' class="%s"' % css_class
        css_class = css if css_class else ''
        return '<a href="%s?%s"%s>%s</a>' % (table_url, query, css_class, idx)

    def update(self):
        """Update batch"""
        # 3 is is the placeholder for the first, current and last item.
        total = self.prev_batch_size + self.next_batch_size + 3
        if self.batch.total <= total:
            # give all batches
            self.batch_items = self.batch.batches
        else:
            # switch to an advanced batch subset
            self.batch_items = first_neighbours_last(self.batches,
                                                     self.batch.index,
                                                     self.prev_batch_size,
                                                     self.next_batch_size)

    def render(self):
        """Render batch"""
        self.update()
        res = []
        append = res.append
        idx = 0
        last_idx = len(self.batch_items)
        for batch in self.batch_items:
            idx += 1
            # build css class
            css_classes = []
            if batch and batch == self.batch:
                css_classes.append("current")
            if idx == 1:
                css_classes.append("first")
            if idx == last_idx:
                css_classes.append("last")

            if css_classes:
                css = " ".join(css_classes)
            else:
                css = None

            # render spaces
            if batch is None:
                append(self.batch_spacer)
            elif idx == 1:
                # render first
                append(self.render_batch_link(batch, css))
            elif batch == self.batch:
                # render current
                append(self.render_batch_link(batch, css))
            elif idx == last_idx:
                # render last
                append(self.render_batch_link(batch, css))
            else:
                append(self.render_batch_link(batch))
        return u"\n".join(res)
