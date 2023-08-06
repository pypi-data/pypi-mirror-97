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

"""PyAMS_table.table module

This module provides the main table management class.
"""

from xml.sax.saxutils import quoteattr

from zope.interface import implementer
from zope.location import Location

from pyams_batching.interfaces import IBatch
from pyams_table.column import NoneCell
from pyams_table.interfaces import IBatchProvider, IColumn, INoneCell, ISequenceTable, ITable, \
    IValues
from pyams_utils.factory import get_object_factory


def get_weight(column):
    """Get sorting weight of a table"""
    try:
        return int(column.weight)
    except AttributeError:
        return 0


def get_sort_method(idx):
    """Get sort key of item at given index position"""
    def get_sort_key(item):
        sublist = item[idx]

        def get_column_sort_key(sublist):
            return sublist[1].get_sort_key(sublist[0])

        return get_column_sort_key(sublist)

    return get_sort_key


def name_column(column, name):
    """Give a column a __name__."""
    column.__name__ = name
    return column


@implementer(ITable)
class Table(Location):
    # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """Generic usable table implementation."""

    # customize this part if needed
    prefix = "table"

    # css classes
    css_classes = {}
    # additional (row) css
    css_class_even = ""
    css_class_odd = ""
    css_class_selected = ""
    # css to show sorting, set to None to turn off
    css_class_sorted_on = "sorted-on"

    # sort attributes
    sort_on = 0
    sort_order = "ascending"
    reverse_sort_order_names = ["descending", "reverse", "down"]

    # batch attributes
    batch_provider_name = "batch"
    batch_start = 0
    batch_size = 50
    start_batching_at = 50

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context
        # private variables will be set in update call
        self.batch_provider = None
        self.column_counter = 0
        self.columnindex_by_id = {}
        self.column_by_name = {}
        self.column_by_index = {}
        self.columns = None
        self.rows = []
        self.selected_items = []

    def init_columns(self):
        """Init table columns"""
        # setup columns
        self.columns = self.setup_columns()
        # order columns
        self.order_columns()

    @property
    def values(self):
        """Get table values"""
        registry = self.request.registry
        adapter = registry.getMultiAdapter((self.context, self.request, self), IValues)
        return adapter.values

    # CSS helpers

    def get_css_highlight_class(self, column, item, css_class):
        # pylint: disable=no-self-use,unused-argument
        """Provide a highlight option for any cell"""
        return css_class

    def get_css_sort_class(self, column, css_class):
        """Add CSS class based on current sorting"""
        if self.css_class_sorted_on and self.sort_on is not None:
            try:
                current_sort_id = int(self.sort_on)
            except ValueError:
                current_sort_id = self.sort_on.rsplit("-", 1)[-1]
            sort_id = column.id.rsplit("-", 1)[-1]

            if int(sort_id) == int(current_sort_id):
                klass = self.css_class_sorted_on + " " + self.sort_order
                if css_class:
                    css_class += " " + klass
                else:
                    css_class = klass
        return css_class

    def get_css_class(self, element, css_class=None):
        """Add CSS class based on HTML tag, make a `class=` attribute"""
        klass = self.css_classes.get(element)
        if klass and css_class:
            klass = "%s %s" % (css_class, klass)
        elif css_class:
            klass = css_class
        return " class=%s" % quoteattr(klass) if klass else ""

    # setup

    def setup_columns(self):
        """Setup columns"""
        registry = self.request.registry
        cols = list(registry.getAdapters((self.context, self.request, self), IColumn))
        # use the adapter name as column name
        return [name_column(col, name) for name, col in cols]

    def update_columns(self):
        """Update columns contents"""
        for col in self.columns:
            col.update()

    def order_columns(self):
        """Order columns"""
        self.column_counter = 0
        self.columns = sorted(self.columns, key=get_weight)
        for col in self.columns:
            self.column_by_name[col.__name__] = col
            idx = self.column_counter
            col.id = "%s-%s-%s" % (self.prefix, col.__name__, idx)
            self.columnindex_by_id[col.id] = idx
            self.column_counter += 1

    def setup_row(self, item):
        """Setup row for given item"""
        cols = []
        append = cols.append
        colspan_counter = 0
        countdown = len(self.columns)
        for col in self.columns:
            countdown -= 1
            colspan = 0
            if colspan_counter == 0:
                colspan = colspan_counter = col.get_colspan(item)
                # adjust colspan because we define 0, 2, 3, etc.
                if colspan_counter > 0:
                    colspan_counter -= 1

            if colspan == 0 and colspan_counter > 0:
                # override col if colspan is 0 and colspan coutner not 0
                colspan_counter -= 1
                colspan = 0
                # now we are ready to setup dummy colspan cells
                col = NoneCell(self.context, self.request, self)

            # we reached the end of the table and have still colspan
            if (countdown - colspan) < 0:
                raise ValueError("Colspan for column '%s' is larger than the table." % col)

            append((item, col, colspan))
        return cols

    def setup_rows(self):
        """Setup rows list"""
        return [self.setup_row(item) for item in self.values]

    # sort

    def get_sort_on(self):
        """Returns sort on column id"""
        return self.request.params.get(self.prefix + "-sort-on", self.sort_on)

    def get_sort_order(self):
        """Returns sort order criteria"""
        return self.request.params.get(self.prefix + "-sort-order", self.sort_order)

    def sort_rows(self):
        """Sort table rows"""
        if self.sort_on is not None and self.rows and self.columns:
            sort_on_idx = self.columnindex_by_id.get(self.sort_on, 0)
            sort_key_getter = get_sort_method(sort_on_idx)
            rows = sorted(self.rows, key=sort_key_getter)
            if self.sort_order in self.reverse_sort_order_names:
                rows.reverse()
            self.rows = rows

    # batch

    def get_batch_size(self):
        """Get table batch size"""
        return int(self.request.params.get(self.prefix + "-batch-size", self.batch_size))

    def get_batch_start(self):
        """Get table batch start position"""
        return int(self.request.params.get(self.prefix + "-batch-start", self.batch_start))

    def batch_rows(self):
        """Create batch of rows, if required"""
        if len(self.rows) > self.start_batching_at:
            factory = get_object_factory(IBatch)
            if factory is not None:
                self.rows = factory(self.rows, start=self.batch_start, size=self.batch_size)

    def update_batch(self):
        """Update batch, if required"""
        if IBatch.providedBy(self.rows):
            registry = self.request.registry
            self.batch_provider = registry.getMultiAdapter((self.context, self.request, self),
                                                           IBatchProvider,
                                                           name=self.batch_provider_name)
            self.batch_provider.update()

    def is_selected_row(self, row):
        """Check if row is selected"""
        item, col, colspan = row[0]  # pylint: disable=unused-variable
        if item in self.selected_items:
            return True
        return False

    # render

    def render_batch(self):
        """Render current batch, if any"""
        if self.batch_provider is None:
            return ""
        return self.batch_provider.render()

    def render_table(self):
        """Render the whole table"""
        if self.columns:
            css_class = self.get_css_class("table")
            head = self.render_head()
            body = self.render_body()
            return '<table%s>%s%s\n</table>' % (css_class, head, body)
        return ''

    def render_head(self):
        """Render table head"""
        css_class = self.get_css_class("thead")
        head = self.render_head_row()
        return "\n  <thead%s>%s\n  </thead>" % (css_class, head)

    def render_head_row(self):
        """Render table head row"""
        css_class = self.get_css_class("tr")
        cells = [self.render_head_cell(col) for col in self.columns]
        return "\n    <tr%s>%s\n    </tr>" % (css_class, "".join(cells))

    def render_head_cell(self, column):
        """Render table head cell for given column"""
        css_class = column.css_classes.get("th")
        css_class = self.get_css_sort_class(column, css_class)
        css_class = self.get_css_class("th", css_class)
        return '\n      <th%s>%s</th>' % (css_class, column.render_head_cell())

    def render_body(self):
        """Render table body"""
        css_class = self.get_css_class("tbody")
        body = self.render_rows()
        return '\n  <tbody%s>%s\n  </tbody>' % (css_class, body)

    def render_rows(self):
        """Render table rows"""
        counter = 0
        rows = []
        css_classes = (self.css_class_even, self.css_class_odd)
        append = rows.append
        for row in self.rows:
            append(self.render_row(row, css_classes[counter % 2]))
            counter += 1
        return ''.join(rows)

    def render_row(self, row, css_class=None):
        """Render given row"""
        is_selected = self.is_selected_row(row)
        if is_selected and self.css_class_selected and css_class:
            css_class = "%s %s" % (self.css_class_selected, css_class)
        elif is_selected and self.css_class_selected:
            css_class = self.css_class_selected
        css_class = self.get_css_class("tr", css_class)
        cells = [self.render_cell(item, col, colspan) for item, col, colspan in row]
        return '\n    <tr%s>%s\n    </tr>' % (css_class, ''.join(cells))

    def render_json_row(self, row):
        """Render given row in JSON"""
        return [self.render_json_cell(item, col) for item, col, colspan in row]

    def render_cell(self, item, column, colspan=0):
        """Render cell for item and column"""
        if INoneCell.providedBy(column):
            return ""
        css_class = column.css_classes.get("td")
        css_class = self.get_css_highlight_class(column, item, css_class)
        css_class = self.get_css_sort_class(column, css_class)
        css_class = self.get_css_class("td", css_class)
        colspan_str = ' colspan="%s"' % colspan if colspan else ""
        return '\n      <td%s%s>%s</td>' % (
            css_class,
            colspan_str,
            column.render_cell(item),
        )

    def render_json_cell(self, item, column):
        """Render cell in JSON for item and column"""
        if INoneCell.providedBy(column):
            return None
        return str(column.render_cell(item))

    def update(self):
        """Update table contents"""
        # reset values
        self.column_counter = 0
        self.column_by_index = {}
        self.selected_items = []

        # use batch values from request or the existing ones
        self.batch_size = self.get_batch_size()
        self.batch_start = self.get_batch_start()

        # use sorting values from request or the existing ones
        self.sort_on = self.get_sort_on()
        self.sort_order = self.get_sort_order()

        # initialize columns
        self.init_columns()

        # update columns
        self.update_columns()

        # setup headers based on columns
        self.rows = self.setup_rows()

        # sort items on columns
        self.sort_rows()

        # batch sorted rows
        self.batch_rows()

        self.update_batch()

    def render(self):
        """Render table contents"""
        # allow to use a template for rendering the table, this will allow
        # to position the batch before and after the table
        return self.render_table()

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.__name__)


@implementer(ISequenceTable)
class SequenceTable(Table):
    """Sequence table adapts a sequence as context.

    This table can be used for adapting a z3c.indexer.search.ResultSet or
    pyams_batching.batch.Batch instance as context. Batch which wraps a
    ResultSet sequence.
    """
