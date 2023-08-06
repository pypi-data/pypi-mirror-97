Sorting Table
-------------

Another table feature is the support for sorting data given from columns. Since
sorting table data is an important feature, we offer this by default. But it
only gets used if there is a ``sort-on`` value set. You can set this value at
class level by adding a ``defaultSortOn`` value or set it as a request value.
We show you how to do this later. We also need a columns which allows us to do
a better sort sample. Our new sorting column will use the content items number
value for sorting:

  >>> from pyramid.testing import setUp, tearDown, DummyRequest
  >>> from pyams_table.testing import setup_adapters

  >>> config = setUp(hook_zca=True)
  >>> setup_adapters(config.registry)
  >>> root = {}

  >>> from pyams_table import column, table
  >>> class NumberColumn(column.Column):
  ...
  ...     header = 'Number'
  ...     weight = 20
  ...
  ...     def get_sort_key(self, item):
  ...         return item.number
  ...
  ...     def render_cell(self, item):
  ...         return 'number: %s' % item.number


Now let's set up a table:

  >>> from pyams_table.testing import TitleColumn
  >>> class SortingTable(table.Table):
  ...
  ...     def setup_columns(self):
  ...         firstColumn = TitleColumn(self.context, self.request, self)
  ...         firstColumn.__name__ = 'title'
  ...         firstColumn.__parent__ = self
  ...         secondColumn = NumberColumn(self.context, self.request, self)
  ...         secondColumn.__name__ = 'number'
  ...         secondColumn.__parent__ = self
  ...         return [firstColumn, secondColumn]

Create a container:

  >>> from pyams_table.testing import OrderedContainer
  >>> container = OrderedContainer()

We also need some container items that we can use for sorting:

  >>> from pyams_table.testing import Content
  >>> container['first'] = Content('First', 1)
  >>> container['second'] = Content('Second', 2)
  >>> container['third'] = Content('Third', 3)
  >>> container['fourth'] = Content('Fourth', 4)
  >>> container['zero'] = Content('Zero', 0)

And render them without set a ``sort-on`` value:

  >>> request = DummyRequest()
  >>> sortingTable = SortingTable(container, request)
  >>> sortingTable.update()
  >>> print(sortingTable.render())
  <table>
    <thead>
      <tr>
        <th class="sorted-on ascending">Title</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="sorted-on ascending">Title: First</td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td class="sorted-on ascending">Title: Fourth</td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td class="sorted-on ascending">Title: Second</td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td class="sorted-on ascending">Title: Third</td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td class="sorted-on ascending">Title: Zero</td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>

Ooops, well, by default the table is sorted on the first column, ascending.

  >>> sortingTable.sort_on
  0

Now switch off sorting, now we get the original order:

  >>> sortingTable.sort_on = None
  >>> sortingTable.update()
  >>> print(sortingTable.render())
  <table>
    <thead>
      <tr>
        <th>Title</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Title: First</td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td>Title: Second</td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td>Title: Third</td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td>Title: Fourth</td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td>Title: Zero</td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>


As you can see this table doesn't provide any explicit order. Let's find out
the index of our column that we like to sort on:

  >>> sortOnId = sortingTable.rows[0][1][1].id
  >>> sortOnId
  'table-number-1'

And let's use this id as ``sort-on`` value:

  >>> sortingTable.sort_on = sortOnId

An important thing is to update the table after set an ``sort-on`` value:

  >>> sortingTable.update()
  >>> print(sortingTable.render())
  <table>
    <thead>
      <tr>
        <th>Title</th>
        <th class="sorted-on ascending">Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Title: Zero</td>
        <td class="sorted-on ascending">number: 0</td>
      </tr>
      <tr>
        <td>Title: First</td>
        <td class="sorted-on ascending">number: 1</td>
      </tr>
      <tr>
        <td>Title: Second</td>
        <td class="sorted-on ascending">number: 2</td>
      </tr>
      <tr>
        <td>Title: Third</td>
        <td class="sorted-on ascending">number: 3</td>
      </tr>
      <tr>
        <td>Title: Fourth</td>
        <td class="sorted-on ascending">number: 4</td>
      </tr>
    </tbody>
  </table>

We can also reverse the sorting order:

  >>> sortingTable.sort_order = 'reverse'
  >>> sortingTable.update()
  >>> print(sortingTable.render())
  <table>
    <thead>
      <tr>
        <th>Title</th>
        <th class="sorted-on reverse">Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Title: Fourth</td>
        <td class="sorted-on reverse">number: 4</td>
      </tr>
      <tr>
        <td>Title: Third</td>
        <td class="sorted-on reverse">number: 3</td>
      </tr>
      <tr>
        <td>Title: Second</td>
        <td class="sorted-on reverse">number: 2</td>
      </tr>
      <tr>
        <td>Title: First</td>
        <td class="sorted-on reverse">number: 1</td>
      </tr>
      <tr>
        <td>Title: Zero</td>
        <td class="sorted-on reverse">number: 0</td>
      </tr>
    </tbody>
  </table>

The table implementation is also able to get the sorting criteria given from a
request. Let's setup such a request:

  >>> sorterRequest = DummyRequest(params={'table-sort-on': 'table-number-1',
  ...                                      'table-sort-order':'descending'})

and another time, update and render. As you can see the new table gets sorted
by the second column and ordered in reverse order:

  >>> requestSortedTable = SortingTable(container, sorterRequest)
  >>> requestSortedTable.update()
  >>> print(requestSortedTable.render())
  <table>
    <thead>
      <tr>
        <th>Title</th>
        <th class="sorted-on descending">Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Title: Fourth</td>
        <td class="sorted-on descending">number: 4</td>
      </tr>
      <tr>
        <td>Title: Third</td>
        <td class="sorted-on descending">number: 3</td>
      </tr>
      <tr>
        <td>Title: Second</td>
        <td class="sorted-on descending">number: 2</td>
      </tr>
      <tr>
        <td>Title: First</td>
        <td class="sorted-on descending">number: 1</td>
      </tr>
      <tr>
        <td>Title: Zero</td>
        <td class="sorted-on descending">number: 0</td>
      </tr>
    </tbody>
  </table>

There's a header renderer, which provides a handy link rendering for sorting:

  >>> from pyams_table import interfaces
  >>> from pyams_table.header import SortingColumnHeader
  >>> config.registry.registerAdapter(SortingColumnHeader,
  ...     (None, None, interfaces.ITable, interfaces.IColumn),
  ...     provided=interfaces.IColumnHeader)

Let's see now various sortings:

  >>> request = DummyRequest()
  >>> sortingTable = SortingTable(container, request)
  >>> sortingTable.update()
  >>> sortingTable.sort_on
  0
  >>> sortingTable.sort_order
  'ascending'
  >>> print(sortingTable.render())
  <table>
    <thead>
      <tr>
        <th class="sorted-on ascending"><a href="?table-sort-on=table-title-0&table-sort-order=descending" title="Sort">Title</a></th>
        <th><a href="?table-sort-on=table-number-1&table-sort-order=ascending" title="Sort">Number</a></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="sorted-on ascending">Title: First</td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td class="sorted-on ascending">Title: Fourth</td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td class="sorted-on ascending">Title: Second</td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td class="sorted-on ascending">Title: Third</td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td class="sorted-on ascending">Title: Zero</td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>

Let's see the `number` column:

  >>> sortingTable.sort_on = 'table-number-1'

  >>> sortingTable.update()
  >>> print(sortingTable.render())
  <table>
    <thead>
      <tr>
        <th><a href="?table-sort-on=table-title-0&table-sort-order=ascending" title="Sort">Title</a></th>
        <th class="sorted-on ascending"><a href="?table-sort-on=table-number-1&table-sort-order=descending" title="Sort">Number</a></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Title: Zero</td>
        <td class="sorted-on ascending">number: 0</td>
      </tr>
      <tr>
        <td>Title: First</td>
        <td class="sorted-on ascending">number: 1</td>
      </tr>
      <tr>
        <td>Title: Second</td>
        <td class="sorted-on ascending">number: 2</td>
      </tr>
      <tr>
        <td>Title: Third</td>
        <td class="sorted-on ascending">number: 3</td>
      </tr>
      <tr>
        <td>Title: Fourth</td>
        <td class="sorted-on ascending">number: 4</td>
      </tr>
    </tbody>
  </table>

Let's see the `title` column but descending:

  >>> sortingTable.sort_on = 'table-title-0'
  >>> sortingTable.sort_order = 'descending'

  >>> sortingTable.update()
  >>> print(sortingTable.render())
  <table>
    <thead>
      <tr>
        <th class="sorted-on descending"><a href="?table-sort-on=table-title-0&table-sort-order=ascending" title="Sort">Title</a></th>
        <th><a href="?table-sort-on=table-number-1&table-sort-order=descending" title="Sort">Number</a></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="sorted-on descending">Title: Zero</td>
        <td>number: 0</td>
      </tr>
      <tr>
        <td class="sorted-on descending">Title: Third</td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td class="sorted-on descending">Title: Second</td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td class="sorted-on descending">Title: Fourth</td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td class="sorted-on descending">Title: First</td>
        <td>number: 1</td>
      </tr>
    </tbody>
  </table>

  >>> tearDown()
