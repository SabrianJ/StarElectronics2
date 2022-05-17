import django_tables2 as tables

from .models import OrderItem, CustomerOrder, Part, SupplierOrder


class OrderTable(tables.Table):
    tag_final_value = tables.Column(orderable=False, verbose_name='Value')
    date = tables.DateColumn(format="d/m/Y")
    action = tables.TemplateColumn(
        '<a href="{{ record.get_edit_url }}" class="btn btn-info"><i class="fa fa-edit"></i></a>', orderable=False)

    class Meta:
        model = CustomerOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'id', 'customer', 'tag_final_value', 'status']


class PartTable(tables.Table):
    cost = tables.Column(orderable=False, verbose_name='Cost')
    action = tables.TemplateColumn(
        '<button class="btn btn-info add_button" data-href="{% url "ajax_add" instance.id record.id %}">Add!</a>',
        orderable=False
    )

    class Meta:
        model = Part
        template_name = 'django_tables2/bootstrap.html'
        fields = ['name', 'stock', 'reserved_stock', 'available_stock', 'cost']


class PartTableSupplier(tables.Table):
    cost = tables.Column(orderable=False, verbose_name='Cost')
    item_in_order = tables.Column(orderable=False, verbose_name="In Order")
    action = tables.TemplateColumn(
        '<button class="btn btn-info add_button_supplier" data-href="{% url "ajax_add_supplier" instance.id record.id %}">Add!</a>',
        orderable=False
    )

    class Meta:
        model = Part
        template_name = 'django_tables2/bootstrap.html'
        fields = ['name', 'stock', 'reserved_stock', 'available_stock', 'item_in_order', 'cost']


class OrderItemTable(tables.Table):
    total_price = tables.Column(orderable=True, verbose_name='Total Price')
    unit_price = tables.Column(accessor='part.cost', verbose_name='@')
    action = tables.TemplateColumn('''
        {% if not instance.confirm %}
            <button data-href="{% url "ajax_modify" record.id "add" %}" class="btn btn-success edit_button"><i class="fa fa-arrow-up"></i></button>
            <button data-href="{% url "ajax_modify" record.id "remove" %}" class="btn btn-warning edit_button"><i class="fa fa-arrow-down"></i></button>
            <button data-href="{% url "ajax_modify" record.id "delete" %}" class="btn btn-danger edit_button"><i class="fa fa-trash"></i></button>
        {% endif %}
    ''', orderable=False)

    class Meta:
        model = OrderItem
        template_name = 'django_tables2/bootstrap.html'
        fields = ['part', 'quantity', 'unit_price', 'total_price']


class SupplierOrderItemTable(tables.Table):
    total_price = tables.Column(orderable=True, verbose_name='Total Price')
    unit_price = tables.Column(accessor='part.cost', verbose_name='@')
    manufacture_number = tables.Column(accessor='part.manufacturer_number', verbose_name="Manufacture No")
    action = tables.TemplateColumn('''
        {% if not instance.confirm %}
            <button data-href="{% url "ajax_modify_supplier" record.id "add" %}" class="btn btn-success edit_button_supplier"><i class="fa fa-arrow-up"></i></button>
            <button data-href="{% url "ajax_modify_supplier" record.id "remove" %}" class="btn btn-warning edit_button_supplier"><i class="fa fa-arrow-down"></i></button>
            <button data-href="{% url "ajax_modify_supplier" record.id "delete" %}" class="btn btn-danger edit_button_supplier"><i class="fa fa-trash"></i></button>
        {% endif %}
    ''', orderable=False)

    class Meta:
        model = OrderItem
        template_name = 'django_tables2/bootstrap.html'
        fields = ['part', 'manufacture_number', 'quantity', 'unit_price', 'total_price']


class SupplierOrderTable(tables.Table):
    date = tables.DateColumn(format="d/m/Y")
    value = tables.Column(orderable=True, verbose_name="Total price")
    action = tables.TemplateColumn(
        '<a href="{% url "update_supplier_order" record.id %}" class="btn btn-info"><i class="fa fa-edit"></i></a>',
        orderable=False)

    class Meta:
        model = SupplierOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'supplier', 'value', 'status']


class SupplierOrderDetailTable(tables.Table):
    date = tables.DateColumn(format="d/m/Y")
    unit_price = tables.Column(accessor='part.cost', verbose_name='@')
    manufacturer_number = tables.Column(accessor='part.manufacturer_number', verbose_name="Manufacture No")

    class Meta:
        model = SupplierOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'manufacturer_number', 'part', 'supplier', 'quantity', 'unit_price', 'total_price']
