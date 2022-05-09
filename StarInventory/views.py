from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django_tables2 import RequestConfig

from StarElectronics2.settings import CURRENCY
from StarInventory.forms import PartForm, CustomerForm, SupplierForm, OrderCreateForm, OrderEditForm, SupplierOrderForm
from StarInventory.models import Part, Customer, Supplier, CustomerOrder, OrderItem, SupplierOrder
from StarInventory.tables import OrderTable, PartTable, OrderItemTable, SupplierOrderTable


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


def ajax_calculate_results_view(request):
    orders = CustomerOrder.filter_data(request, CustomerOrder.objects.all())
    total_value, total_paid_value, remaining_value, data = 0, 0, 0, dict()
    if orders.exists():
        total_value = orders.aggregate(Sum('value'))['value__sum']
        total_paid_value = orders.filter(status=True).aggregate(Sum('value'))['value__sum'] if \
            orders.filter(status=True) else 0
        remaining_value = total_value - total_paid_value
    total_value, total_paid_value, remaining_value = f'{CURRENCY} {total_value} ', \
                                                     f'{CURRENCY}{total_paid_value}', f'{CURRENCY}{remaining_value} '
    data['result'] = render_to_string(template_name='include/result_container.html',
                                      request=request,
                                      context=locals())
    return JsonResponse(data)


class CreateSupplierOrderView(CreateView):
    model = SupplierOrder
    template_name = "create_supplier_order.html"
    form_class = SupplierOrderForm

    success_url = reverse_lazy("list_supplier_order")


class SupplierOrderListView(ListView):
    template_name = 'list_supplier_order.html'
    model = SupplierOrder
    paginate_by = 50

    def get_queryset(self):
        qs = SupplierOrder.objects.all()
        if self.request.GET:
            qs = SupplierOrder.filter_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier_orders = SupplierOrderTable(self.object_list)
        RequestConfig(self.request).configure(supplier_orders)
        context.update(locals())
        return context


class SupplierOrderDetailView(DetailView):
    template_name = 'detail_supplier_order.html'
    model = SupplierOrder
    paginate_by = 50

    def get_success_url(self):
        return reverse('list_supplier_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        qs = self.get_queryset()
        supplier_order = SupplierOrderTable(qs)
        RequestConfig(self.request).configure(supplier_order)
        context.update(locals())
        return context


class CreateOrderView(CreateView):
    template_name = 'form.html'
    form_class = OrderCreateForm
    model = CustomerOrder

    def get_success_url(self):
        self.new_object.refresh_from_db()
        return reverse('update_order', kwargs={'pk': self.new_object.id})

    def form_valid(self, form):
        object = form.save()
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = CustomerOrder
    template_name = 'order_update.html'
    form_class = OrderEditForm

    def get_success_url(self):
        return reverse('update_order', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        qs_p = Part.objects.all()[:12]
        parts = PartTable(qs_p)
        order_items = OrderItemTable(instance.order_items.all())
        RequestConfig(self.request).configure(parts)
        RequestConfig(self.request).configure(order_items)
        context.update(locals())
        return context


def ajax_search_parts(request, pk):
    instance = get_object_or_404(CustomerOrder, id=pk)
    q = request.GET.get('q', None)
    parts = Part.objects.filter(name__startswith=q)
    parts = parts[:12]
    parts = PartTable(parts)
    RequestConfig(request).configure(parts)
    data = dict()
    data['parts'] = render_to_string(template_name='include/product_container.html',
                                     request=request,
                                     context={
                                         'parts': parts,
                                         'instance': instance
                                     })
    return JsonResponse(data)


def order_action_view(request, pk, action):
    instance = get_object_or_404(CustomerOrder, id=pk)
    if action == 'is_paid':
        instance.status = True
        instance.save()
    if action == 'delete':
        if not instance.confirm:
            instance.delete()
    return redirect(reverse('home'))


def ajax_add_product(request, pk, dk):
    instance = get_object_or_404(CustomerOrder, id=pk)
    part = get_object_or_404(Part, id=dk)
    order_item, created = OrderItem.objects.get_or_create(customerOrder=instance, part=part)
    if not instance.confirm:
        if created:
            order_item.quantity = 1
            order_item.price = part.cost
        else:
            order_item.quantity += 1
        order_item.save()
        part.reserved_stock += 1
        part.save()
    instance.refresh_from_db()
    order_items = OrderItemTable(instance.order_items.all())
    RequestConfig(request).configure(order_items)
    data = dict()
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={'instance': instance,
                                               'order_items': order_items
                                               }
                                      )
    return JsonResponse(data)


def ajax_modify_order_item(request, pk, action):
    order_item = get_object_or_404(OrderItem, id=pk)
    part = order_item.part
    instance = order_item.customerOrder
    if not instance.confirm:
        if action == 'remove':
            order_item.quantity -= 1
            part.reserved_stock -= 1
            if order_item.quantity < 1: order_item.quantity = 1
        if action == 'add':
            order_item.quantity += 1
            part.reserved_stock += 1
        part.save()
        order_item.save()
        if action == 'delete':
            order_item.delete()
    data = dict()
    instance.refresh_from_db()
    order_items = OrderItemTable(instance.order_items.all())
    RequestConfig(request).configure(order_items)
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance,
                                          'order_items': order_items
                                      }
                                      )
    return JsonResponse(data)


def delete_order(request, pk):
    instance = get_object_or_404(CustomerOrder, id=pk)
    if not instance.confirm:
        instance.delete()
        messages.warning(request, 'The order is deleted!')
        return redirect(reverse('home'))
    else:
        return redirect((reverse('control_orders')))
