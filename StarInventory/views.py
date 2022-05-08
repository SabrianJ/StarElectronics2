from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView
from django_tables2 import RequestConfig

from StarElectronics2.settings import CURRENCY
from StarInventory.forms import PartForm, CustomerForm, SupplierForm
from StarInventory.models import Part, Customer, Supplier, CustomerOrder
from StarInventory.tables import OrderTable


def index(request):
    return render(request, "welcome.html", {"title": "Welcome Page", "content": "My content"})


def list_parts(request):
    parts = Part.objects.all()
    context = {"parts": parts}
    return render(request, "list_parts.html", context)


class CreatePartView(CreateView):
    model = Part
    form_class = PartForm
    template_name = "create_part.html"

    success_url = reverse_lazy("list_parts")


class UpdatePartView(UpdateView):
    model = Part
    form_class = PartForm
    template_name = "update_part.html"

    success_url = reverse_lazy("list_parts")


def list_customers(request):
    customers = Customer.objects.all()
    context = {"customers": customers}
    return render(request, "list_customers.html", context)


class CreateCustomerView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "create_customer.html"

    success_url = reverse_lazy("list_customers")


class UpdateCustomerView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "update_customer.html"

    success_url = reverse_lazy("list_customers")


def list_suppliers(request):
    suppliers = Supplier.objects.all()
    context = {"suppliers": suppliers}
    return render(request, "list_suppliers.html", context)


class CreateSupplierView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "create_supplier.html"

    success_url = reverse_lazy("list_suppliers")


class UpdateSupplierView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "update_supplier.html"

    success_url = reverse_lazy("list_suppliers")


class HomepageView(ListView):
    template_name = 'index.html'
    model = CustomerOrder
    queryset = CustomerOrder.objects.all()[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = CustomerOrder.objects.all()
        orders = OrderTable(orders)
        RequestConfig(self.request).configure(orders)
        context.update(locals())
        return context


class OrderListView(ListView):
    template_name = 'list.html'
    model = CustomerOrder
    paginate_by = 50

    def get_queryset(self):
        qs = CustomerOrder.objects.all()
        if self.request.GET:
            qs = CustomerOrder.filter_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = OrderTable(self.object_list)
        RequestConfig(self.request).configure(orders)
        context.update(locals())
        return context


def list_orders(request):
    customer_orders = CustomerOrder.objects.all()
    context = {"orders": customer_orders}
    return render(request, "list_orders.html", context)


def ajax_calculate_results_view(request):
    orders = CustomerOrder.filter_data(request, CustomerOrder.objects.all())
    total_value, total_paid_value, remaining_value, data = 0, 0, 0, dict()
    if orders.exists():
        total_value = orders.aggregate(Sum('value'))['value__sum']
        total_paid_value = orders.filter(status=True).aggregate(Sum('value'))['value__sum'] if\
            orders.filter(status=True) else 0
        remaining_value = total_value - total_paid_value
    total_value, total_paid_value, remaining_value = f'{CURRENCY} {total_value} ',\
                                                     f'{CURRENCY}{total_paid_value} {CURRENCY}', f'{CURRENCY}{remaining_value} '
    data['result'] = render_to_string(template_name='include/result_container.html',
                                      request=request,
                                      context=locals())
    return JsonResponse(data)
