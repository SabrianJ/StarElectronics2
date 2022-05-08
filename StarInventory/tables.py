import django_tables2 as tables

from .models import OrderItem, CustomerOrder, Part


class OrderTable(tables.Table):
    tag_final_value = tables.Column(orderable=False, verbose_name='Value')
    action = tables.TemplateColumn(
        '<a href="{{ record.get_edit_url }}" class="btn btn-info"><i class="fa fa-edit"></i></a>', orderable=False)

    class Meta:
        model = CustomerOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'customer', 'tag_final_value', 'status']


class PartTable(tables.Table):
    cost = tables.Column(orderable=False, verbose_name='Cost')
    action = tables.TemplateColumn(
        '<button class="btn btn-info add_button" data-href="{% url "ajax_add" instance.id record.id %}">Add!</a>',
        orderable=False
    )

    class Meta:
        model = Part
        template_name = 'django_tables2/bootstrap.html'
        fields = ['name', 'stock', 'reserved_stock','available_stock', 'cost']


class OrderItemTable(tables.Table):
    total_price = tables.Column(orderable=False, verbose_name='Total Price')
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
        fields = ['part', 'quantity', 'total_price']
