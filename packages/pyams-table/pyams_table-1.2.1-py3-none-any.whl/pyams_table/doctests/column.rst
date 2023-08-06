=============
Table Columns
=============

Let's show the different columns we offer by default. But first take a look at
the README.txt which explains the Table and Column concepts.


Sample data setup
-----------------

  >>> from pyramid.testing import setUp, tearDown
  >>> from pyams_table.testing import setup_adapters

  >>> config = setUp(hook_zca=True)
  >>> setup_adapters(config.registry)
  >>> root = {}

Let's create a sample container that we can use as our iterable context:

  >>> from zope.container import btree
  >>> class Container(btree.BTreeContainer):
  ...     """Sample container."""
  >>> container = Container()
  >>> root['container'] = container

and create a sample content object that we use as container item:

  >>> class Content(object):
  ...     """Sample content."""
  ...     def __init__(self, title, number, email):
  ...         self.title = title
  ...         self.number = number
  ...         self.email = email

Now setup some items:

  >>> container['zero'] = Content('Zero', 0, 'zero@example.com')
  >>> container['first'] = Content('First', 1, 'first@example.com')
  >>> container['second'] = Content('Second', 2, 'second@example.com')
  >>> container['third'] = Content('Third', 3, 'third@example.com')
  >>> container['fourth'] = Content('Fourth', 4, None)

Let's also create a simple number sortable column:

  >>> from pyams_table import column
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


NameColumn
----------

Let's define a table using the NameColumn:

  >>> from pyams_table import table
  >>> class NameTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.NameColumn, 'name',
  ...                               weight=1),
  ...             column.add_column(self, NumberColumn, name='number',
  ...                               weight=2, header='Number')
  ...         ]

Now create, update and render our table and you can see that the NameColumn
renders the name of the item using the zope.traversing.api.getName() concept:

  >>> from pyramid.testing import DummyRequest
  >>> request = DummyRequest()
  >>> nameTable = NameTable(container, request)
  >>> nameTable.update()
  >>> print(nameTable.render())
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>first</td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td>fourth</td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td>second</td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td>third</td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td>zero</td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>


RadioColumn
-----------

Let's define a table using the RadioColumn:

  >>> class RadioTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.RadioColumn, 'radioColumn',
  ...                               weight=1),
  ...             column.add_column(self, NumberColumn, name='number',
  ...                               weight=2, header='Number')
  ...             ]

Now create, update and render our table:

  >>> request = DummyRequest()
  >>> radioTable = RadioTable(container, request)
  >>> radioTable.update()
  >>> print(radioTable.render())
  <table>
    <thead>
      <tr>
        <th>X</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="first"  /></td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="fourth"  /></td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="second"  /></td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="third"  /></td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="zero"  /></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>

As you can see, we can force to render the radio input field as selected with a
given request value:

  >>> radioRequest = DummyRequest(params={'table-radioColumn-0-selected-item': 'third'})
  >>> radioTable = RadioTable(container, radioRequest)
  >>> radioTable.update()
  >>> print(radioTable.render())
  <table>
    <thead>
      <tr>
        <th>X</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="first"  /></td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="fourth"  /></td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="second"  /></td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="third" checked="checked" /></td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td><input type="radio" class="radio-widget" name="table-radioColumn-0-selected-item" value="zero"  /></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>


CheckBoxColumn
--------------

Let's define a table using the RadioColumn:

  >>> class CheckBoxTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.CheckBoxColumn, 'checkBoxColumn',
  ...                               weight=1),
  ...             column.add_column(self, NumberColumn, name='number',
  ...                               weight=2, header='Number')
  ...             ]

Now create, update and render our table:


  >>> request = DummyRequest()
  >>> checkBoxTable = CheckBoxTable(container, request)
  >>> checkBoxTable.update()
  >>> print(checkBoxTable.render())
  <table>
    <thead>
      <tr>
        <th>X</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="first"  /></td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="fourth"  /></td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="second"  /></td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="third"  /></td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="zero"  /></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>

And again you can set force to render the checkbox input field as selected with
a given request value:

  >>> checkBoxRequest = DummyRequest(params={'table-checkBoxColumn-0-selected-items':
  ...                                        ['first', 'third']})
  >>> checkBoxTable = CheckBoxTable(container, checkBoxRequest)
  >>> checkBoxTable.update()
  >>> print(checkBoxTable.render())
  <table>
    <thead>
      <tr>
        <th>X</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="first" checked="checked" /></td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="fourth"  /></td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="second"  /></td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="third" checked="checked" /></td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="zero"  /></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>

If you select a row, you can also give them an additional CSS style. This could
be used in combination with alternating ``even`` and ``odd`` styles:

  >>> checkBoxRequest = DummyRequest(params={'table-checkBoxColumn-0-selected-items':
  ...                                        ['first', 'third']})
  >>> checkBoxTable = CheckBoxTable(container, checkBoxRequest)
  >>> checkBoxTable.css_classes = {'tr': 'tr'}
  >>> checkBoxTable.css_class_selected = 'selected'
  >>> checkBoxTable.css_class_even = 'even'
  >>> checkBoxTable.css_class_odd = 'odd'
  >>> checkBoxTable.update()
  >>> print(checkBoxTable.render())
  <table>
    <thead>
      <tr class="tr">
        <th>X</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr class="selected even tr">
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="first" checked="checked" /></td>
        <td>number: 1</td>
      </tr>
      <tr class="odd tr">
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="fourth"  /></td>
        <td>number: 4</td>
      </tr>
      <tr class="even tr">
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="second"  /></td>
        <td>number: 2</td>
      </tr>
      <tr class="selected odd tr">
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="third" checked="checked" /></td>
        <td>number: 3</td>
      </tr>
      <tr class="even tr">
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="zero"  /></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>

Let's test the ``css_class_selected`` without any other css class:

  >>> checkBoxRequest = DummyRequest(params={'table-checkBoxColumn-0-selected-items':
  ...                                        ['first', 'third']})
  >>> checkBoxTable = CheckBoxTable(container, checkBoxRequest)
  >>> checkBoxTable.css_class_selected = u'selected'
  >>> checkBoxTable.update()
  >>> print(checkBoxTable.render())
  <table>
    <thead>
      <tr>
        <th>X</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr class="selected">
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="first" checked="checked" /></td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="fourth"  /></td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="second"  /></td>
        <td>number: 2</td>
      </tr>
      <tr class="selected">
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="third" checked="checked" /></td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td><input type="checkbox" class="checkbox-widget" name="table-checkBoxColumn-0-selected-items" value="zero"  /></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>


CreatedColumn
-------------

Let's define a table using the CreatedColumn:

  >>> class CreatedColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.CreatedColumn, u'createdColumn',
  ...                               weight=1),
  ...         ]

Now create, update and render our table. Note, we use a Dublin Core stub
adapter which only returns ``01/01/01 01:01`` as created date:

  >>> request = DummyRequest()
  >>> createdColumnTable = CreatedColumnTable(container, request)
  >>> createdColumnTable.update()
  >>> print(createdColumnTable.render())
  <table>
    <thead>
      <tr>
        <th>Created</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
    </tbody>
  </table>


ModifiedColumn
--------------

Let's define a table using the ModifiedColumn and a custom format string:

  >>> from pyams_utils.date import SH_DATETIME_FORMAT
  >>> class ModifiedColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.ModifiedColumn,
  ...                               'modifiedColumn', weight=1,
  ...                               format_string=SH_DATETIME_FORMAT),
  ...         ]

Now create, update and render our table. Note, we use a Dublin Core stub
adapter which only returns ``02/02/02 02:02`` as modified date:

  >>> request = DummyRequest()
  >>> modifiedColumnTable = ModifiedColumnTable(container, request)
  >>> modifiedColumnTable.update()
  >>> print(modifiedColumnTable.render())
  <table>
    <thead>
      <tr>
        <th>Modified</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>02/02/2002 - 02:02</td>
      </tr>
      <tr>
        <td>02/02/2002 - 02:02</td>
      </tr>
      <tr>
        <td>02/02/2002 - 02:02</td>
      </tr>
      <tr>
        <td>02/02/2002 - 02:02</td>
      </tr>
      <tr>
        <td>02/02/2002 - 02:02</td>
      </tr>
    </tbody>
  </table>


GetAttrColumn
-------------

The ``GetAttrColumn`` column is a handy column that retrieves the value from
the item by attribute access.
It also provides a ``default_value`` in case an exception happens.

  >>> class GetTitleColumn(column.GetAttrColumn):
  ...
  ...     attr_name = 'title'
  ...     default_value = 'missing'

  >>> class GetAttrColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, GetTitleColumn, 'title'),
  ...         ]

Render and update the table:

  >>> request = DummyRequest()
  >>> getAttrColumnTable = GetAttrColumnTable(container, request)
  >>> getAttrColumnTable.update()
  >>> print(getAttrColumnTable.render())
  <table>
    <thead>
      <tr>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>First</td>
      </tr>
      <tr>
        <td>Fourth</td>
      </tr>
      <tr>
        <td>Second</td>
      </tr>
      <tr>
        <td>Third</td>
      </tr>
      <tr>
        <td>Zero</td>
      </tr>
    </tbody>
  </table>

If we use a non-existing Attribute, we do not raise an AttributeError, we will
get the default value:

  >>> class UndefinedAttributeColumn(column.GetAttrColumn):
  ...
  ...     attr_name = 'undefined'
  ...     default_value = 'missing'

  >>> class GetAttrColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, UndefinedAttributeColumn, 'missing'),
  ...         ]

Render and update the table:

  >>> request = DummyRequest()
  >>> getAttrColumnTable = GetAttrColumnTable(container, request)
  >>> getAttrColumnTable.update()
  >>> print(getAttrColumnTable.render())
  <table>
    <thead>
      <tr>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>missing</td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
    </tbody>
  </table>

A missing ``attr_name`` in ``GetAttrColumn`` would also end in return the
``default_value``:

  >>> class BadAttributeColumn(column.GetAttrColumn):
  ...
  ...     default_value = u'missing'

  >>> firstItem = container[u'first']
  >>> simpleTable = table.Table(container, request)
  >>> badColumn = column.add_column(simpleTable, BadAttributeColumn, u'bad')
  >>> badColumn.render_cell(firstItem)
  'missing'

If we try to access a protected attribute the object raises an ``Unauthorized``.
In this case we also return the default_value. Let's setup an object which
raises such an error if we access the title:

  >>> from zope.security.interfaces import Unauthorized
  >>> class ProtectedItem(object):
  ...
  ...     @property
  ...     def forbidden(self):
  ...         raise Unauthorized('forbidden')

Setup and test the item:

  >>> protectedItem = ProtectedItem()
  >>> protectedItem.forbidden
  Traceback (most recent call last):
  ...
  zope.security.interfaces.Unauthorized: forbidden

Now define a column:

  >>> class ForbiddenAttributeColumn(column.GetAttrColumn):
  ...
  ...     attr_name = 'forbidden'
  ...     default_value = u'missing'

And test the attribute access:

  >>> simpleTable = table.Table(container, request)
  >>> badColumn = column.add_column(simpleTable, ForbiddenAttributeColumn, u'x')
  >>> badColumn.render_cell(protectedItem)
  'missing'


I18nGetAttrColumn
-----------------

The ``I18nGetAttrColumn`` column can be used to get a translated value of the item:

    >>> from pyams_table import _
    >>> class I18nGetAttrColumn(column.I18nGetAttrColumn):
    ...     def get_value(self, obj):
    ...         return _("I18n value")

    >>> i18nTable = table.Table(container, request)
    >>> i18nColumn = column.add_column(i18nTable, I18nGetAttrColumn, 'i18n')
    >>> i18nColumn.render_cell(protectedItem)
    'I18n value'


GetItemColumn
-------------

The ``GetItemColumn`` column is a handy column that retrieves the value from
the item by index or key access. That means the item can be a tuple, list, dict
or anything that implements that.
It also provides a ``default_value`` in case an exception happens.

Dict-ish
........

  >>> sampleDictData = [
  ...     dict(name='foo', value=1),
  ...     dict(name='bar', value=7),
  ...     dict(name='moo', value=42),]

  >>> class GetDictColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.GetItemColumn, 'name',
  ...                               header='Name',
  ...                               idx='name', default_value='missing'),
  ...             column.add_column(self, column.GetItemColumn, 'value',
  ...                               header='Value',
  ...                               idx='value', default_value='missing'),
  ...             ]
  ...     @property
  ...     def values(self):
  ...         return sampleDictData

Render and update the table:

  >>> request = DummyRequest()
  >>> getDictColumnTable = GetDictColumnTable(sampleDictData, request)
  >>> getDictColumnTable.update()
  >>> print(getDictColumnTable.render())
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>bar</td>
        <td>7</td>
      </tr>
      <tr>
        <td>foo</td>
        <td>1</td>
      </tr>
      <tr>
        <td>moo</td>
        <td>42</td>
      </tr>
    </tbody>
  </table>

If we use a non-existing index/key, we do not raise an exception, we will
get the default value:

  >>> class GetDictColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.GetItemColumn, 'name',
  ...                               idx='not-existing', default_value='missing'),
  ...             ]
  ...     @property
  ...     def values(self):
  ...         return sampleDictData

Render and update the table:

  >>> request = DummyRequest()
  >>> getDictColumnTable = GetDictColumnTable(container, request)
  >>> getDictColumnTable.update()
  >>> print(getDictColumnTable.render())
  <table>
    <thead>
      <tr>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>missing</td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
    </tbody>
  </table>

A missing ``idx`` in ``GetItemColumn`` would also end in return the
``default_value``:

  >>> class BadIdxColumn(column.GetItemColumn):
  ...
  ...     default_value = 'missing'

  >>> firstItem = sampleDictData[0]
  >>> simpleTable = table.Table(sampleDictData, request)
  >>> badColumn = column.add_column(simpleTable, BadIdxColumn, u'bad')
  >>> badColumn.render_cell(firstItem)
  'missing'

Tuple/List-ish
...............

  >>> sampleTupleData = [
  ...     (50, 'bar'),
  ...     (42, 'cent'),
  ...     (7, 'bild'),]

  >>> class GetTupleColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.GetItemColumn, u'name',
  ...                              header='Name',
  ...                              idx=1, default_value='missing'),
  ...             column.add_column(self, column.GetItemColumn, 'value',
  ...                              header=u'Value',
  ...                              idx=0, default_value='missing'),
  ...             ]
  ...     @property
  ...     def values(self):
  ...         return sampleTupleData

Render and update the table:

  >>> request = DummyRequest()
  >>> getTupleColumnTable = GetTupleColumnTable(sampleTupleData, request)
  >>> getTupleColumnTable.update()
  >>> print(getTupleColumnTable.render())
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>bar</td>
        <td>50</td>
      </tr>
      <tr>
        <td>bild</td>
        <td>7</td>
      </tr>
      <tr>
        <td>cent</td>
        <td>42</td>
      </tr>
    </tbody>
  </table>

If we use a non-existing index/key, we do not raise an exception, we will
get the default value:

  >>> class GetTupleColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.GetItemColumn, 'name',
  ...                               idx=42, default_value='missing'),
  ...             ]
  ...     @property
  ...     def values(self):
  ...         return sampleTupleData

Render and update the table:

  >>> request = DummyRequest()
  >>> getTupleColumnTable = GetTupleColumnTable(container, request)
  >>> getTupleColumnTable.update()
  >>> print(getTupleColumnTable.render())
  <table>
    <thead>
      <tr>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>missing</td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
    </tbody>
  </table>

A missing ``idx`` in ``GetItemColumn`` would also end in return the
``default_value``:

  >>> class BadIdxColumn(column.GetItemColumn):
  ...
  ...     default_value = 'missing'

  >>> firstItem = sampleTupleData[0]
  >>> simpleTable = table.Table(sampleTupleData, request)
  >>> badColumn = column.add_column(simpleTable, BadIdxColumn, 'bad')
  >>> badColumn.render_cell(firstItem)
  'missing'


GetAttrFormatterColumn
----------------------

The ``GetAttrFormatterColumn`` column is a get attr column which is able to
format the value. Let's use the Dublin Core adapter for our sample:

  >>> from zope.dublincore.interfaces import IZopeDublinCore
  >>> class GetCreatedColumn(column.GetAttrFormatterColumn):
  ...
  ...     def get_value(self, item):
  ...         dc = IZopeDublinCore(item, None)
  ...         return dc.created

  >>> class GetAttrFormatterColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, GetCreatedColumn, 'created'),
  ...         ]

Render and update the table:

  >>> request = DummyRequest()
  >>> getAttrFormatterColumnTable = GetAttrFormatterColumnTable(container,
  ...     request)
  >>> getAttrFormatterColumnTable.update()
  >>> print(getAttrFormatterColumnTable.render())
  <table>
    <thead>
      <tr>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
      <tr>
        <td>on 01/01/2001 at 01:01</td>
      </tr>
    </tbody>
  </table>


We can also change the formatter settings in such a column:

  >>> class ShortCreatedColumn(column.GetAttrFormatterColumn):
  ...
  ...     format_string = SH_DATETIME_FORMAT
  ...
  ...     def get_value(self, item):
  ...         dc = IZopeDublinCore(item, None)
  ...         return dc.created

  >>> class ShortFormatterColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, ShortCreatedColumn, 'created'),
  ...         ]

Render and update the table:

  >>> request = DummyRequest()
  >>> shortFormatterColumnTable = ShortFormatterColumnTable(container,
  ...     request)
  >>> shortFormatterColumnTable.update()
  >>> print(shortFormatterColumnTable.render())
  <table>
    <thead>
      <tr>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>01/01/2001 - 01:01</td>
      </tr>
      <tr>
        <td>01/01/2001 - 01:01</td>
      </tr>
      <tr>
        <td>01/01/2001 - 01:01</td>
      </tr>
      <tr>
        <td>01/01/2001 - 01:01</td>
      </tr>
      <tr>
        <td>01/01/2001 - 01:01</td>
      </tr>
    </tbody>
  </table>


EMailColumn
-----------

The ``EMailColumn`` column is ``GetAttrColumn`` which is used to
display a mailto link. By default in the link content the e-mail
address is displayed, too.


  >>> class EMailColumn(column.EMailColumn):
  ...
  ...     attr_name = 'email'
  ...     default_value = 'missing'

  >>> class EMailColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, EMailColumn, 'email'),
  ...         ]

When a cell does not contain an e-mail address, the ``default_value``
is rendered:

  >>> request = DummyRequest()
  >>> eMailColumnTable = EMailColumnTable(container, request)
  >>> eMailColumnTable.update()
  >>> print(eMailColumnTable.render())
  <table>
    <thead>
      <tr>
        <th>E-Mail</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="mailto:first@example.com">first@example.com</a></td>
      </tr>
      <tr>
        <td><a href="mailto:second@example.com">second@example.com</a></td>
      </tr>
      <tr>
        <td><a href="mailto:third@example.com">third@example.com</a></td>
      </tr>
      <tr>
        <td><a href="mailto:zero@example.com">zero@example.com</a></td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
    </tbody>
  </table>

The link content can be overwriten by setting the ``link_content`` attribute:

  >>> class StaticEMailColumn(column.EMailColumn):
  ...
  ...     attr_name = 'email'
  ...     default_value = 'missing'
  ...     link_content = 'Mail me'

  >>> class StaticEMailColumnTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, StaticEMailColumn, 'mail'),
  ...             ]

Render and update the table:

  >>> request = DummyRequest()
  >>> staticEMailColumnTable = StaticEMailColumnTable(container, request)
  >>> staticEMailColumnTable.update()
  >>> print(staticEMailColumnTable.render())
  <table>
    <thead>
      <tr>
        <th>E-Mail</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="mailto:first@example.com">Mail me</a></td>
      </tr>
      <tr>
        <td><a href="mailto:second@example.com">Mail me</a></td>
      </tr>
      <tr>
        <td><a href="mailto:third@example.com">Mail me</a></td>
      </tr>
      <tr>
        <td><a href="mailto:zero@example.com">Mail me</a></td>
      </tr>
      <tr>
        <td>missing</td>
      </tr>
    </tbody>
  </table>


LinkColumn
----------

Let's define a table using the LinkColumn. This column allows us to write
columns which can point to a page with the item as context:

  >>> class MyLinkColumns(column.LinkColumn):
  ...     link_name = 'myLink.html'
  ...     link_target = '_blank'
  ...     link_css = 'myClass'
  ...     link_title = 'Click >'

  >>> class MyLinkTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, MyLinkColumns, 'link',
  ...                              weight=1),
  ...             column.add_column(self, NumberColumn, name='number',
  ...                              weight=2, header='Number')
  ...             ]

Now create, update and render our table:

  >>> request = DummyRequest()
  >>> myLinkTable = MyLinkTable(container, request)
  >>> myLinkTable.__parent__ = container
  >>> myLinkTable.__name__ = 'myLinkTable.html'
  >>> myLinkTable.update()
  >>> print(myLinkTable.render())
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="http://example.com/first/myLink.html" target="_blank" class="myClass" title="Click &gt;">first</a></td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td><a href="http://example.com/fourth/myLink.html" target="_blank" class="myClass" title="Click &gt;">fourth</a></td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td><a href="http://example.com/second/myLink.html" target="_blank" class="myClass" title="Click &gt;">second</a></td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td><a href="http://example.com/third/myLink.html" target="_blank" class="myClass" title="Click &gt;">third</a></td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td><a href="http://example.com/zero/myLink.html" target="_blank" class="myClass" title="Click &gt;">zero</a></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>


ContentsLinkColumn
------------------

There are some predefined link columns available. This one will generate a
``contents.html`` link for each item:

  >>> class ContentsLinkTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.ContentsLinkColumn, 'link',
  ...                              weight=1),
  ...             column.add_column(self, NumberColumn, name='number',
  ...                              weight=2, header='Number')
  ...             ]

  >>> contentsLinkTable = ContentsLinkTable(container, request)
  >>> contentsLinkTable.__parent__ = container
  >>> contentsLinkTable.__name__ = 'contentsLinkTable.html'
  >>> contentsLinkTable.update()
  >>> print(contentsLinkTable.render())
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="http://example.com/first/contents.html">first</a></td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td><a href="http://example.com/fourth/contents.html">fourth</a></td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td><a href="http://example.com/second/contents.html">second</a></td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td><a href="http://example.com/third/contents.html">third</a></td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td><a href="http://example.com/zero/contents.html">zero</a></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>


IndexLinkColumn
---------------

This one will generate a ``index.html`` link for each item:

  >>> class IndexLinkTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.IndexLinkColumn, 'link',
  ...                              weight=1),
  ...             column.add_column(self, NumberColumn, name='number',
  ...                              weight=2, header='Number')
  ...             ]

  >>> indexLinkTable = IndexLinkTable(container, request)
  >>> indexLinkTable.__parent__ = container
  >>> indexLinkTable.__name__ = 'indexLinkTable.html'
  >>> indexLinkTable.update()
  >>> print(indexLinkTable.render())
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="http://example.com/first/index.html">first</a></td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td><a href="http://example.com/fourth/index.html">fourth</a></td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td><a href="http://example.com/second/index.html">second</a></td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td><a href="http://example.com/third/index.html">third</a></td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td><a href="http://example.com/zero/index.html">zero</a></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>


EditLinkColumn
--------------

And this one will generate a ``edit.html`` link for each item:

  >>> class EditLinkTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.EditLinkColumn, 'link',
  ...                              weight=1),
  ...             column.add_column(self, NumberColumn, name='number',
  ...                              weight=2, header='Number')
  ...             ]

  >>> editLinkTable = EditLinkTable(container, request)
  >>> editLinkTable.__parent__ = container
  >>> editLinkTable.__name__ = 'editLinkTable.html'
  >>> editLinkTable.update()
  >>> print(editLinkTable.render())
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Number</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="http://example.com/first/edit.html">first</a></td>
        <td>number: 1</td>
      </tr>
      <tr>
        <td><a href="http://example.com/fourth/edit.html">fourth</a></td>
        <td>number: 4</td>
      </tr>
      <tr>
        <td><a href="http://example.com/second/edit.html">second</a></td>
        <td>number: 2</td>
      </tr>
      <tr>
        <td><a href="http://example.com/third/edit.html">third</a></td>
        <td>number: 3</td>
      </tr>
      <tr>
        <td><a href="http://example.com/zero/edit.html">zero</a></td>
        <td>number: 0</td>
      </tr>
    </tbody>
  </table>


SelectedItemColumn
------------------

The ``SelectedItemColumn`` can be used to provide a column which will allow to select an
item from a request param:

  >>> class SelectedItemTable(table.Table):
  ...     css_class_sorted_on = None
  ...
  ...     def setup_columns(self):
  ...         return [
  ...             column.add_column(self, column.SelectedItemColumn, 'link',
  ...                              weight=1)
  ...         ]

  >>> selectedItemTable = SelectedItemTable(container, request)
  >>> selectedItemTable.__parent__ = container
  >>> selectedItemTable.__name__ = 'selectedItemTable.html'
  >>> selectedItemTable.update()
  >>> print(selectedItemTable.render())
  <table>
    <thead>
      <tr>
        <th>Name</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="http://example.com/selectedItemTable.html?table-link-0-selected-items=first">first</a></td>
      </tr>
      <tr>
        <td><a href="http://example.com/selectedItemTable.html?table-link-0-selected-items=fourth">fourth</a></td>
      </tr>
      <tr>
        <td><a href="http://example.com/selectedItemTable.html?table-link-0-selected-items=second">second</a></td>
      </tr>
      <tr>
        <td><a href="http://example.com/selectedItemTable.html?table-link-0-selected-items=third">third</a></td>
      </tr>
      <tr>
        <td><a href="http://example.com/selectedItemTable.html?table-link-0-selected-items=zero">zero</a></td>
      </tr>
    </tbody>
  </table>

  >>> selectedItemTable.selected_items
  []

  >>> request = DummyRequest(params={'table-link-0-selected-items': 'second'})
  >>> selectedItemTable = SelectedItemTable(container, request)
  >>> selectedItemTable.__parent__ = container
  >>> selectedItemTable.__name__ = 'selectedItemTable.html'
  >>> selectedItemTable.update()
  >>> selectedItemTable.selected_items
  [<pyams_table.tests.test_utilsdocs.Content object at 0x...>]


Tests cleanup:

  >>> tearDown()
