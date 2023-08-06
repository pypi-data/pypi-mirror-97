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

"""PyAMS_table.interfaces module

This module provides all package interfaces.
"""

from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, Interface
from zope.schema import BytesLine, Int, List, TextLine


__docformat__ = 'restructuredtext'


class IValues(Interface):
    """Table value adapter."""

    values = Attribute("Iterable table row data sequence.")


class ITable(IContentProvider):
    # pylint: disable=too-many-public-methods
    """Table provider"""

    column_counter = Int(title="Column counter",
                         description="Column counter",
                         default=0)

    column_index_by_id = Attribute("Dict of column index number by id")

    column_by_name = Attribute("Dict of columns by name")

    columns = Attribute("Sequence of columns")

    rows = Attribute("Sequence of rows")

    selected_items = Attribute("Sequence of selected items")

    # customize this part if needed
    prefix = BytesLine(title="Prefix",
                       description="The prefix of the table used to uniquely identify it.",
                       default=b"table")

    # css classes
    css_classes = Attribute("Dict of element name and CSS classes")

    # additional (row) css
    css_class_even = TextLine(title="Even css row class",
                              description="CSS class for even rows.",
                              default=u"even",
                              required=False)

    css_class_odd = TextLine(title="Odd css row class",
                             description="CSS class for odd rows.",
                             default=u"odd",
                             required=False)

    css_class_selected = TextLine(title="Selected css row class",
                                  description="CSS class for selected rows.",
                                  default=u"selected",
                                  required=False)

    # sort attributes
    sort_on = Int(title="Sort on table index",
                  description="Sort on table index",
                  default=0)

    sort_order = TextLine(title="Sort order",
                          description="Row sort order",
                          default="ascending")

    reverse_sort_order_names = List(title="Selected css row class",
                                    description="CSS class for selected rows.",
                                    value_type=TextLine(title="Reverse sort order name",
                                                        description="Reverse sort order name"),
                                    default=["descending", "reverse", "down"],
                                    required=False)

    # batch attributes
    batch_start = Int(title="Batch start index",
                      description="Index the batch starts with",
                      default=0)

    batch_size = Int(title="Batch size",
                     description="The batch size",
                     default=50)

    start_batching_at = Int(title="Batch start size",
                            description="The minimal size the batch starts to get used",
                            default=50)

    values = Attribute("Iterable table row data sequence.")

    def get_css_class(self, element, css_class=None):
        """Return the css class if any or an empty string."""

    def setup_columns(self):
        """Setup table column renderer."""

    def update_columns(self):
        """Update columns."""

    def init_columns(self):
        """Initialize columns definitions used by the table"""

    def order_columns(self):
        """Order columns."""

    def setup_row(self, item):
        """Setup table row."""

    def setup_rows(self):
        """Setup table rows."""

    def get_sort_on(self):
        """Return sort on column id."""

    def get_sort_order(self):
        """Return sort order criteria."""

    def sort_rows(self):
        """Sort rows."""

    def get_batch_size(self):
        """Return the batch size."""

    def get_batch_start(self):
        """Return the batch start index."""

    def batch_rows(self):
        """Batch rows."""

    def is_selected_row(self, row):
        """Return `True for selected row."""

    def render_table(self):
        """Render the table."""

    def render_head(self):
        """Render the thead."""

    def render_head_row(self):
        """Render the table header rows."""

    def render_head_cell(self, column):
        """Setup the table header rows."""

    def render_body(self):
        """Render the table body."""

    def render_rows(self):
        """Render the table body rows."""

    def render_row(self, row, css_class=None):
        """Render a single table row."""

    def render_json_row(self, row):
        """Render a single table row content in JSON"""

    def render_cell(self, item, column, colspan=0):
        """Render a single table body cell."""

    def render_json_cell(self, item, column):
        """Render a single table body cell content in JSON"""

    def render(self):  # pylint:disable=arguments-differ
        """Plain render method without keyword arguments."""


class ISequenceTable(ITable):
    """Sequence table adapts a sequence as context.

    This table can be used for adapting a pyams_batching.batch.Batch instance as
    context. Batch which wraps a ResultSet sequence.
    """


class IColumn(Interface):
    """Column provider"""

    # pylint: disable=invalid-name
    id = TextLine(title="Id",
                  description="The column id",
                  default=None)

    # customize this part if needed
    colspan = Int(title="Colspan",
                  description="The colspan value",
                  default=0)

    weight = Int(title="Weight",
                 description="The column weight",
                 default=0)

    header = TextLine(title="Header name",
                      description="The header name",
                      default="")

    css_classes = Attribute("Dict of element name and CSS classes")

    def get_colspan(self, item):
        """Colspan value based on the given item."""

    def render_head_cell(self):
        """Render the column header label."""

    def render_cell(self, item):
        """Render the column content."""


class INoneCell(IColumn):
    """None cell used for colspan."""


class IBatchProvider(IContentProvider):
    """Batch content provider"""

    def render_batch_link(self, batch, css_class=None):
        """Render batch links."""

    def render(self):  # pylint: disable=arguments-differ
        """Plain render method without keyword arguments."""


class IColumnHeader(Interface):
    """Multi-adapter for header rendering."""

    def update(self):
        """Override this method in subclasses if required"""

    def render(self):
        """Return the HTML output for the header

        Make sure HTML special chars are escaped.
        Override this method in subclasses"""

    def get_query_string_args(self):
        """
        Because the header will most often be used to add links for sorting the
        columns it may also be necessary to collect other query arguments from
        the request.

        The initial use case here is to maintain a search term.
        """
