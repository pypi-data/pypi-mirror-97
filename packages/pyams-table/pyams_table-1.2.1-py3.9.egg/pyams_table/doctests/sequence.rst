SequenceTable
-------------

A sequence table can be used if we need to provide a table for a sequence
of items instead of a mapping. Define the same sequence of items we used before
we added the other 1000 items:


  >>> from pyramid.testing import setUp, tearDown, DummyRequest
  >>> from pyams_table.testing import setup_adapters

  >>> config = setUp(hook_zca=True)
  >>> setup_adapters(config.registry)
  >>> root = {}

  >>> from pyams_table.testing import Content
  >>> dataSequence = []
  >>> dataSequence.append(Content('Zero', 0))
  >>> dataSequence.append(Content('First', 1))
  >>> dataSequence.append(Content('Second', 2))
  >>> dataSequence.append(Content('Third', 3))
  >>> dataSequence.append(Content('Fourth', 4))
  >>> dataSequence.append(Content('Fifth', 5))
  >>> dataSequence.append(Content('Sixth', 6))
  >>> dataSequence.append(Content('Seventh', 7))
  >>> dataSequence.append(Content('Eighth', 8))
  >>> dataSequence.append(Content('Ninth', 9))
  >>> dataSequence.append(Content('Tenth', 10))
  >>> dataSequence.append(Content('Eleventh', 11))
  >>> dataSequence.append(Content('Twelfth', 12))
  >>> dataSequence.append(Content('Thirteenth', 13))
  >>> dataSequence.append(Content('Fourteenth', 14))
  >>> dataSequence.append(Content('Fifteenth', 15))
  >>> dataSequence.append(Content('Sixteenth', 16))
  >>> dataSequence.append(Content('Seventeenth', 17))
  >>> dataSequence.append(Content('Eighteenth', 18))
  >>> dataSequence.append(Content('Nineteenth', 19))
  >>> dataSequence.append(Content('Twentieth', 20))

Now let's define a new SequenceTable:

  >>> from pyams_table import table, column
  >>> from pyams_table.testing import (TitleColumn, NumberColumn, cell_renderer,
  ...                                  head_cell_renderer)
  >>> class SequenceTable(table.SequenceTable):
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, TitleColumn, 'title',
  ...                              cell_renderer=cell_renderer,
  ...                              head_cell_renderer=head_cell_renderer,
  ...                              weight=1),
  ...             column.add_column(self, NumberColumn, name='number',
  ...                              weight=2, header='Number')
  ...             ]

Now we can create our table adapting our sequence:

  >>> sequenceRequest = DummyRequest(params={'table-batch-start': '0',
  ...                                        'table-sort-on': 'table-number-1'})
  >>> sequenceTable = SequenceTable(dataSequence, sequenceRequest)
  >>> sequenceTable.css_class_sorted_on = None

We also need to give the table a location and a name like we normally setup
in traversing:

  >>> from pyams_table.testing import Container
  >>> container = Container()
  >>> root['container-1'] = container
  >>> sequenceTable.__parent__ = container
  >>> sequenceTable.__name__ = 'sequenceTable.html'

We need to configure our batch provider for the next step first. See the
section ``BatchProvider`` below for more infos about batch rendering:

  >>> from zope.interface import Interface
  >>> from pyramid.interfaces import IRequest
  >>> from pyams_batching.interfaces import IBatch
  >>> from pyams_batching.batch import Batch
  >>> from pyams_table.interfaces import IBatchProvider, ITable
  >>> from pyams_table.batch import BatchProvider
  >>> from pyams_utils.factory import register_factory
  >>> register_factory(IBatch, Batch)
  >>> config.registry.registerAdapter(BatchProvider,
  ...       (Interface, IRequest, ITable),
  ...       provided=IBatchProvider,
  ...       name='batch')

And update and render the sequence table:

  >>> sequenceTable.update()
  >>> print(sequenceTable.render())
  <table>
    <thead>
      <tr>
        <th>My items</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Zero item</td>
        <td>number: 0</td>
      </tr>
      <tr>
        <td>First item</td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td>Second item</td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td>Third item</td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td>Fourth item</td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td>Fifth item</td>
        <td>number: 5</td>
      </tr>
      <tr>
        <td>Sixth item</td>
        <td>number: 6</td>
      </tr>
      <tr>
        <td>Seventh item</td>
        <td>number: 7</td>
      </tr>
      <tr>
        <td>Eighth item</td>
        <td>number: 8</td>
      </tr>
      <tr>
        <td>Ninth item</td>
        <td>number: 9</td>
      </tr>
      <tr>
        <td>Tenth item</td>
        <td>number: 10</td>
      </tr>
      <tr>
        <td>Eleventh item</td>
        <td>number: 11</td>
      </tr>
      <tr>
        <td>Twelfth item</td>
        <td>number: 12</td>
      </tr>
      <tr>
        <td>Thirteenth item</td>
        <td>number: 13</td>
      </tr>
      <tr>
        <td>Fourteenth item</td>
        <td>number: 14</td>
      </tr>
      <tr>
        <td>Fifteenth item</td>
        <td>number: 15</td>
      </tr>
      <tr>
        <td>Sixteenth item</td>
        <td>number: 16</td>
      </tr>
      <tr>
        <td>Seventeenth item</td>
        <td>number: 17</td>
      </tr>
      <tr>
        <td>Eighteenth item</td>
        <td>number: 18</td>
      </tr>
      <tr>
        <td>Nineteenth item</td>
        <td>number: 19</td>
      </tr>
      <tr>
        <td>Twentieth item</td>
        <td>number: 20</td>
      </tr>
    </tbody>
  </table>

As you can see, the items get rendered based on a data sequence. Now we set
the ``start batch at`` size to ``5``:

  >>> sequenceTable.start_batching_at = 5

And the ``batch_size`` to ``5``:

  >>> sequenceTable.batch_size = 5

Now we can update and render the table again. But you will see that we only get
a table size of 5 rows:

  >>> sequenceTable.update()
  >>> print(sequenceTable.render())
  <table>
    <thead>
      <tr>
        <th>My items</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Zero item</td>
        <td>number: 0</td>
      </tr>
      <tr>
        <td>First item</td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td>Second item</td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td>Third item</td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td>Fourth item</td>
        <td>number: 4</td>
      </tr>
    </tbody>
  </table>

And we set the sort order to ``reverse`` even if we use batching:

  >>> sequenceTable.sort_order = 'reverse'
  >>> sequenceTable.update()
  >>> print(sequenceTable.render())
  <table>
    <thead>
      <tr>
        <th>My items</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Twentieth item</td>
        <td>number: 20</td>
      </tr>
      <tr>
        <td>Nineteenth item</td>
        <td>number: 19</td>
      </tr>
      <tr>
        <td>Eighteenth item</td>
        <td>number: 18</td>
      </tr>
      <tr>
        <td>Seventeenth item</td>
        <td>number: 17</td>
      </tr>
      <tr>
        <td>Sixteenth item</td>
        <td>number: 16</td>
      </tr>
    </tbody>
  </table>
