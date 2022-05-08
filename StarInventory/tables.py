import django_tables2 as tables

from .models import OrderItem, CustomerOrder


class OrderTable(tables.Table):
    tag_final_value = tables.Column(orderable=False, verbose_name='Value')
    action = tables.TemplateColumn(
        '<a href="{{ record.get_edit_url }}" class="btn btn-info"><i class="fa fa-edit"></i></a>', orderable=False)

    class Meta:
        model = CustomerOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'customer', 'tag_final_value']
