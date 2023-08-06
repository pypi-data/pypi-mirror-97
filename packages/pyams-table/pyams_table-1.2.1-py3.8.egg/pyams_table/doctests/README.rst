from pyams_table.interfaces import IValues===================
PyAMS_table package
===================

Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

The goal of this package is to offer a modular table rendering library. We use
the content provider pattern and the column are implemented as adapters which
will give us a powerful base concept.


Some important concepts we use
------------------------------

- separate implementation in update render parts, This allows to manipulate
  data after update call and before we render them.

- allow to use page templates if needed. By default all is done in python.

- allow to use the rendered batch outside the existing table HTML part.


No skins
--------

This package does not provide any kind of template or skin support. Most the
time if you need to render a table, you will use your own skin concept. This means
you can render the table or batch within your own templates. This will ensure
that we have as few dependencies as possible in this package and the package
can get reused with any skin concept.


Note
----

As you probably know, batching is only possible after sorting columns. This is
a nightmare if it comes to performance. The reason is, all data need to get
sorted before the batch can start at the given position. And sorting can most
of the time only be done by touching each object. This means you have to be careful
if you are using a large set of data, even if you use batching.


Sample data setup
-----------------

    >>> from pyramid.testing import setUp, tearDown
    >>> from pyams_table.testing import setup_adapters

    >>> config = setUp(hook_zca=True)

    >>> from pyams_table import includeme as include_table
    >>> include_table(config)

    >>> setup_adapters(config.registry)
    >>> root = {}
    
Let's create a sample container which we can use as our iterable context:

    >>> from zope.interface import implementer, Interface
    >>> from zope.component import provideAdapter
    >>> from zope.container.interfaces import IContainer
    >>> from pyramid.interfaces import IRequest
    >>> from pyams_table.interfaces import ISequenceTable, ITable, IValues
    >>> from pyams_table.value import ValuesForContainer, ValuesForSequence

    >>> from zope.container import btree
    >>> class Container(btree.BTreeContainer):
    ...     """Sample container."""
    ...     __name__ = 'container'
    >>> container = Container()

and set a parent for the container:

    >>> root['container'] = container

and create a sample content object which we use as container item:

    >>> class Content(object):
    ...     """Sample content."""
    ...     def __init__(self, title, number):
    ...         self.title = title
    ...         self.number = number

Now setup some items:

    >>> container['first'] = Content('First', 1)
    >>> container['second'] = Content('Second', 2)
    >>> container['third'] = Content('Third', 3)


Table
-----

Create a test request and represent the table:

    >>> from pyramid.testing import DummyRequest
    >>> from pyams_table import table
    
    >>> request = DummyRequest()
    >>> plain_table = table.Table(container, request)
    >>> plain_table.css_class_sorted_on = None

Now we can update and render the table. As you can see with an empty container
we will not get anything that looks like a table. We just get an empty string:

    >>> plain_table.update()
    >>> plain_table.render()
    ''


Column Adapter
--------------

We can create a column for our table:

    >>> from pyams_table import interfaces
    >>> from pyams_table import column

    >>> class TitleColumn(column.Column):
    ...
    ...     weight = 10
    ...     header = u'Title'
    ...
    ...     def render_cell(self, item):
    ...         return u'Title: %s' % item.title

Now we can register the column:

    >>> config.registry.registerAdapter(TitleColumn,
    ...     (None, None, interfaces.ITable), provided=interfaces.IColumn,
    ...     name='first_column')

Now we can render the table again:

    >>> plain_table.update()
    >>> print(plain_table.render())
    <table>
    <thead>
      <tr>
        <th>Title</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Title: First</td>
      </tr>
      <tr>
        <td>Title: Second</td>
      </tr>
      <tr>
        <td>Title: Third</td>
      </tr>
    </tbody>
    </table>

We can also use the predefined name column:

    >>> config.registry.registerAdapter(column.NameColumn,
    ...     (None, None, interfaces.ITable), provided=interfaces.IColumn,
    ...     name='second_column')

Now we will get an additional column:

    >>> plain_table.update()
    >>> print(plain_table.render())
    <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Title</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>first</td>
        <td>Title: First</td>
      </tr>
      <tr>
        <td>second</td>
        <td>Title: Second</td>
      </tr>
      <tr>
        <td>third</td>
        <td>Title: Third</td>
      </tr>
    </tbody>
    </table>


Colspan
-------

Now let's show how we can define a colspan condition of 2 for a column:

    >>> class ColspanColumn(column.NameColumn):
    ...
    ...     weight = 999
    ...
    ...     def get_colspan(self, item):
    ...         # colspan condition
    ...         if item.__name__ == 'first':
    ...             return 2
    ...         else:
    ...             return 0
    ...
    ...     def render_head_cell(self):
    ...         return 'Colspan'
    ...
    ...     def render_cell(self, item):
    ...         return 'colspan: %s' % item.title

Now we register this column adapter as colspanColumn:

    >>> config.registry.registerAdapter(ColspanColumn,
    ...     (None, None, interfaces.ITable), provided=interfaces.IColumn,
    ...      name='colspan_column')

Now you can see that the colspan of the ColspanAdapter is larger than the table.
This will raise a ValueError:

    >>> plain_table.update()
    Traceback (most recent call last):
    ...
    ValueError: Colspan for column '<ColspanColumn 'colspan_column'>' is larger than the table.

But if we set the column as first row, it will render the colspan correctly:

    >>> class CorrectColspanColumn(ColspanColumn):
    ...     """Colspan with correct weight."""
    ...
    ...     weight = -1  # NameColumn is 0

Register and render the table again:

    >>> config.registry.registerAdapter(CorrectColspanColumn,
    ...     (None, None, interfaces.ITable), provided=interfaces.IColumn,
    ...      name='colspan_column')

    >>> plain_table.update()
    >>> print(plain_table.render())
    <table>
    <thead>
      <tr>
        <th>Colspan</th>
        <th>Name</th>
        <th>Title</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td colspan="2">colspan: First</td>
        <td>Title: First</td>
      </tr>
      <tr>
        <td>colspan: Second</td>
        <td>second</td>
        <td>Title: Second</td>
      </tr>
      <tr>
        <td>colspan: Third</td>
        <td>third</td>
        <td>Title: Third</td>
      </tr>
    </tbody>
    </table>


Setup columns
-------------

The existing implementation allows us to define a table in a class without
using the modular adapter pattern for columns.

First we need to define a column which can render a value for our items:

    >>> class SimpleColumn(column.Column):
    ...
    ...     weight = 0
    ...
    ...     def render_cell(self, item):
    ...         return item.title

Let's define our table which defines the columns explicitly. you can also see
that we do not return the columns in the correct order:

    >>> class PrivateTable(table.Table):
    ...     css_class_sorted_on = None
    ...
    ...     def setup_columns(self):
    ...         first_column = TitleColumn(self.context, self.request, self)
    ...         first_column.__name__ = 'title'
    ...         first_column.weight = 1
    ...         second_column = SimpleColumn(self.context, self.request, self)
    ...         second_column.__name__ = 'simple'
    ...         second_column.weight = 2
    ...         second_column.header = 'The second column'
    ...         return [second_column, first_column]

Now we can create, update and render the table and see that this renders a nice
table too:

    >>> private_table = PrivateTable(container, request)
    >>> private_table.update()
    >>> print(private_table.render())
    <table>
    <thead>
      <tr>
        <th>Title</th>
        <th>The second column</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Title: First</td>
        <td>First</td>
      </tr>
      <tr>
        <td>Title: Second</td>
        <td>Second</td>
      </tr>
      <tr>
        <td>Title: Third</td>
        <td>Third</td>
      </tr>
    </tbody>
    </table>

We can render a single row in JSON; this can be useful in AJAX applications to be able to
update a single table row:

    >>> row = private_table.setup_row(container['first'])
    >>> private_table.render_json_row(row)
    ['Title: First', 'First']


Cascading Style Sheet
---------------------

Our table and column implementation supports CSS class assignment. Let's define
a table and columns with some css class values:

    >>> class CSSTable(table.Table):
    ...
    ...     css_classes = {'table': 'table',
    ...                    'thead': 'thead',
    ...                    'tbody': 'tbody',
    ...                    'th': 'th',
    ...                    'tr': 'tr',
    ...                    'td': 'td'}
    ...     css_class_sorted_on = None
    ...
    ...     def setup_columns(self):
    ...         first_column = TitleColumn(self.context, self.request, self)
    ...         first_column.__name__ = 'title'
    ...         first_column.__parent__ = self
    ...         first_column.weight = 1
    ...         first_column.css_classes = {'th':'thCol', 'td':'tdCol'}
    ...         second_column = SimpleColumn(self.context, self.request, self)
    ...         second_column.__name__ = 'simple'
    ...         second_column.__parent__ = self
    ...         second_column.weight = 2
    ...         second_column.header = 'The second column'
    ...         return [second_column, first_column]

Now let's see if we got the css class assigned which we defined in the table and
column. Note that the ``th`` and ``td`` got CSS declarations from the table and
from the column:

    >>> css_table = CSSTable(container, request)
    >>> css_table.update()
    >>> print(css_table.render())
    <table class="table">
    <thead class="thead">
      <tr class="tr">
        <th class="thCol th">Title</th>
        <th class="th">The second column</th>
      </tr>
    </thead>
    <tbody class="tbody">
      <tr class="tr">
        <td class="tdCol td">Title: First</td>
        <td class="td">First</td>
      </tr>
      <tr class="tr">
        <td class="tdCol td">Title: Second</td>
        <td class="td">Second</td>
      </tr>
      <tr class="tr">
        <td class="tdCol td">Title: Third</td>
        <td class="td">Third</td>
      </tr>
    </tbody>
    </table>


Alternating table
-----------------

We offer built in support for alternating table rows based on even and odd CSS
classes. Let's define a table including other CSS classes. For even/odd support,
we only need to define the ``css_class_even`` and ``css_class_odd`` CSS classes:

    >>> class AlternatingTable(table.Table):
    ...
    ...     css_classes = {'table': 'table',
    ...                    'thead': 'thead',
    ...                    'tbody': 'tbody',
    ...                    'th': 'th',
    ...                    'tr': 'tr',
    ...                    'td': 'td'}
    ...
    ...     css_class_even = 'even'
    ...     css_class_odd = 'odd'
    ...     css_class_sorted_on = None
    ...
    ...     def setup_columns(self):
    ...         first_column = TitleColumn(self.context, self.request, self)
    ...         first_column.__name__ = 'title'
    ...         first_column.__parent__ = self
    ...         first_column.weight = 1
    ...         first_column.css_classes = {'th':'thCol', 'td':'tdCol'}
    ...         second_column = SimpleColumn(self.context, self.request, self)
    ...         second_column.__name__ = 'simple'
    ...         second_column.__parent__ = self
    ...         second_column.weight = 2
    ...         second_column.header = 'The second column'
    ...         return [second_column, first_column]

Now update and render the new table. As you can see the given ``tr`` class is
added to the even and odd classes:

    >>> alternating_table = AlternatingTable(container, request)
    >>> alternating_table.update()
    >>> print(alternating_table.render())
    <table class="table">
    <thead class="thead">
      <tr class="tr">
        <th class="thCol th">Title</th>
        <th class="th">The second column</th>
      </tr>
    </thead>
    <tbody class="tbody">
      <tr class="even tr">
        <td class="tdCol td">Title: First</td>
        <td class="td">First</td>
      </tr>
      <tr class="odd tr">
        <td class="tdCol td">Title: Second</td>
        <td class="td">Second</td>
      </tr>
      <tr class="even tr">
        <td class="tdCol td">Title: Third</td>
        <td class="td">Third</td>
      </tr>
    </tbody>
    </table>


Class based Table setup
-----------------------

There is a more elegant way to define table rows at class level. We offer
a method which you can use if you need to define some columns called
``addColumn``. Before we define the table. let's define some cell renderer:

    >>> def head_cell_renderer():
    ...     return 'My items'

    >>> def cell_renderer(item):
    ...     return '%s item' % item.title

Now we can define our table and use the custom cell renderer:

    >>> class AddColumnTable(table.Table):
    ...
    ...     css_classes = {'table': 'table',
    ...                    'thead': 'thead',
    ...                    'tbody': 'tbody',
    ...                    'th': 'th',
    ...                    'tr': 'tr',
    ...                    'td': 'td'}
    ...
    ...     css_class_even = 'even'
    ...     css_class_odd = 'odd'
    ...     css_class_sorted_on = None
    ...
    ...     def setup_columns(self):
    ...         return [
    ...             column.add_column(self, TitleColumn, 'title',
    ...                               cell_renderer=cell_renderer,
    ...                               head_cell_renderer=head_cell_renderer,
    ...                               weight=1, colspan=0),
    ...             column.add_column(self, SimpleColumn, name='simple',
    ...                              weight=2, header='The second column',
    ...                              css_classes = {'th':'thCol', 'td':'tdCol'})
    ...             ]

Add some more content:

    >>> container[u'fourth'] = Content('Fourth', 4)
    >>> container[u'zero'] = Content('Zero', 0)

    >>> add_column_table = AddColumnTable(container, request)
    >>> add_column_table.update()
    >>> print(add_column_table.render())
    <table class="table">
    <thead class="thead">
      <tr class="tr">
        <th class="th">My items</th>
        <th class="thCol th">The second column</th>
      </tr>
    </thead>
    <tbody class="tbody">
      <tr class="even tr">
        <td class="td">First item</td>
        <td class="tdCol td">First</td>
      </tr>
      <tr class="odd tr">
        <td class="td">Fourth item</td>
        <td class="tdCol td">Fourth</td>
      </tr>
      <tr class="even tr">
        <td class="td">Second item</td>
        <td class="tdCol td">Second</td>
      </tr>
      <tr class="odd tr">
        <td class="td">Third item</td>
        <td class="tdCol td">Third</td>
      </tr>
      <tr class="even tr">
        <td class="td">Zero item</td>
        <td class="tdCol td">Zero</td>
      </tr>
    </tbody>
    </table>

As you can see the table columns provide all attributes we set in the addColumn
method:

    >>> title_column = add_column_table.rows[0][0][1]
    >>> title_column
    <TitleColumn 'title'>

    >>> title_column.__name__
    'title'

    >>> title_column.__parent__
    <AddColumnTable None>

    >>> title_column.colspan
    0

    >>> title_column.weight
    1

    >>> title_column.header
    'Title'

    >>> title_column.css_classes
    {}

and the second column:

    >>> simple_column = add_column_table.rows[0][1][1]
    >>> simple_column
    <SimpleColumn 'simple'>

    >>> simple_column.__name__
    'simple'

    >>> simple_column.__parent__
    <AddColumnTable None>

    >>> simple_column.colspan
    0

    >>> simple_column.weight
    2

    >>> simple_column.header
    'The second column'

    >>> sorted(simple_column.css_classes.items())
    [('td', 'tdCol'), ('th', 'thCol')]


Headers
-------

We can change the rendering of the header of, e.g, the Title column by
registering a IHeaderColumn adapter. This may be useful for adding links to
column headers for an existing table implementation.

We'll use a fresh almost empty container.:

    >>> container = Container()
    >>> root['container-1'] = container
    >>> container['first'] = Content('First', 1)
    >>> container['second'] = Content('Second', 2)
    >>> container['third'] = Content('Third', 3)

    >>> class myTableClass(table.Table):
    ...     css_class_sorted_on = None

    >>> my_table = myTableClass(container, request)

    >>> class TitleColumn(column.Column):
    ...
    ...     header = u'Title'
    ...     weight = -2
    ...
    ...     def render_cell(self, item):
    ...         return item.title

Now we can register a column adapter directly to our table class:

    >>> config.registry.registerAdapter(TitleColumn,
    ...     (None, None, myTableClass), provided=interfaces.IColumn,
    ...      name='title_column')

And add a registration for a column header - we'll use here the provided generic
sorting header implementation:

    >>> from pyams_table.header import SortingColumnHeader
    >>> config.registry.registerAdapter(SortingColumnHeader,
    ...     (None, None, interfaces.ITable, interfaces.IColumn),
    ...     provided=interfaces.IColumnHeader)

Now we can render the table and we shall see a link in the header. Note that it
is set to switch to descending as the table initially will display the first
column as ascending:

    >>> my_table.update()
    >>> print(my_table.render())
    <table>
    <thead>
    <tr>
     <th><a
      href="?table-sort-on=table-title_column-0&table-sort-order=descending"
      title="Sort">Title</a></th>
    ...
    </table>

If the table is initially set to descending, the link should allow to switch to
ascending again:

    >>> my_table.sort_order = 'descending'
    >>> print(my_table.render())
    <table>
    <thead>
    <tr>
     <th><a
      href="?table-sort-on=table-title_column-0&table-sort-order=ascending"
      title="Sort">Title</a></th>
    ...
    </table>

If the table is ascending but the request was descending,
the link should allow to switch again to ascending:

    >>> descending_request = DummyRequest(params={'table-sort-on': 'table-title_column-0',
    ...                                           'table-sort-order':'descending'})
    >>> my_table = myTableClass(container, descending_request)
    >>> my_table.sortOrder = 'ascending'
    >>> my_table.update()
    >>> print(my_table.render())
    <table>
    <thead>
    <tr>
     <th><a
      href="?table-sort-on=table-title_column-0&table-sort-order=ascending"
      title="Sort">Title</a></th>
    ...
    </table>


Tests cleanup:

    >>> tearDown()
