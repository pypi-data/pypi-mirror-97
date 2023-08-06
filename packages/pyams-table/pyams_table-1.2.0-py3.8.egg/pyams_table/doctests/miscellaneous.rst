Miscellaneous
-------------

Make coverage report happy and test different things.

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> from pyams_table.testing import setup_adapters

    >>> config = setUp(hook_zca=True)
    >>> setup_adapters(config.registry)
    >>> root = {}

Test if the getWeight method returns 0 (zero) on AttributeError:

  >>> from pyams_table.table import get_weight
  >>> get_weight(None)
  0

Create a container:

  >>> from pyams_table.testing import Container
  >>> container = Container()

Try to call a simple table and call renderBatch which should return an empty
string:

  >>> from pyams_table import table
  >>> request = DummyRequest()
  >>> simpleTable = table.Table(container, request)
  >>> simpleTable.render_batch()
  ''

Try to render an empty table adapting an empty mapping:

  >>> simpleTable = table.Table({}, request)
  >>> simpleTable.css_class_sorted_on = None
  >>> simpleTable.render()
  ''

Since we register an adapter for IColumn on None (IOW on an empty mapping).

  >>> from zope.component import provideAdapter
  >>> from pyams_table import column
  >>> from pyams_table import interfaces
  >>> config.registry.registerAdapter(column.NameColumn,
  ...     (None, None, interfaces.ITable), provided=interfaces.IColumn,
  ...      name='secondColumn')

Initializing rows definitions for the empty table initializes the columns
attribute list.

  >>> simpleTable.columns

  >>> simpleTable.init_columns()
  >>> simpleTable.columns
  [<NameColumn 'secondColumn'>]

Rendering the empty table now return the string:

  >>> print(simpleTable.render())
  <table>
    <thead>
      <tr>
        <th>Name</th>
      </tr>
    </thead>
    <tbody>
    </tbody>
  </table>


Let's see if the addColumn raises a ValueError if there is no Column class:

  >>> column.add_column(simpleTable, column.Column, 'dummy')
  <Column 'dummy'>

  >>> column.add_column(simpleTable, None, 'dummy')
  Traceback (most recent call last):
  ...
  ValueError: class_ None must implement IColumn.

Test if we can set additional kws in addColumn:

  >>> simpleColumn = column.add_column(simpleTable, column.Column, 'dummy',
  ...     foo='foo value', bar='something else', counter=99)
  >>> simpleColumn.foo
  'foo value'

  >>> simpleColumn.bar
  'something else'

  >>> simpleColumn.counter
  99

The NoneCell class provides some methods which never get called. But these
are defined in the interface. Let's test the default values
and make coverage report happy.

Let's get an container item first:

  >>> from pyams_table.testing import Content
  >>> firstItem = Content('First', 1)
  >>> noneCellColumn = column.add_column(simpleTable, column.NoneCell, 'none')
  >>> noneCellColumn.render_cell(firstItem)
  ''

  >>> noneCellColumn.get_colspan(firstItem)
  0

  >>> noneCellColumn.render_head_cell()
  ''

  >>> noneCellColumn.render_cell(firstItem)
  ''

The default ``Column`` implementation raises an NotImplementedError if we
do not override the render_cell method:

  >>> defaultColumn = column.add_column(simpleTable, column.Column, 'default')
  >>> defaultColumn.render_cell(firstItem)
  Traceback (most recent call last):
  ...
  NotImplementedError: Subclass must implement render_cell
