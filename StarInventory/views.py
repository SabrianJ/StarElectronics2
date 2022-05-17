from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django_tables2 import RequestConfig

from StarElectronics2.settings import CURRENCY
from StarInventory.forms import PartForm, CustomerForm, SupplierForm, OrderCreateForm, OrderEditForm, SupplierOrderForm, \
    SupplierOrderEditForm
from StarInventory.models import Part, Customer, Supplier, CustomerOrder, OrderItem, SupplierOrder, SupplierOrderItem
from StarInventory.tables import OrderTable, PartTable, OrderItemTable, SupplierOrderTable, SupplierOrderDetailTable, \
    SupplierOrderItemTable, PartTableSupplier


@login_required(login_url='/login')
def index(request):
    return render(request, "welcome.html", {"title": "Welcome Page", "content": "My content"})


def login_view(request):
    if request.POST:
        print("logging in")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("<h1>Invalid Credentials, Please try again </h1>")
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url='/login')
def list_parts(request):
    parts = Part.objects.all()
    context = {"parts": parts}
    return render(request, "list_parts.html", context)


class CreatePartView(LoginRequiredMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = "create_part.html"

    login_url = '/login'

    success_url = reverse_lazy("list_parts")


class UpdatePartView(LoginRequiredMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = "update_part.html"

    login_url = '/login'

    success_url = reverse_lazy("list_parts")


@login_required(login_url='/login')
def list_customers(request):
    customers = Customer.objects.all()
    context = {"customers": customers}
    return render(request, "list_customers.html", context)


class CreateCustomerView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "create_customer.html"

    login_url = '/login'

    success_url = reverse_lazy("list_customers")


class UpdateCustomerView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "update_customer.html"

    login_url = '/login'

    success_url = reverse_lazy("list_customers")


@login_required(login_url='/login')
def list_suppliers(request):
    suppliers = Supplier.objects.all()
    context = {"suppliers": suppliers}
    return render(request, "list_suppliers.html", context)


class CreateSupplierView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "create_supplier.html"

    login_url = '/login'

    success_url = reverse_lazy("list_suppliers")


class UpdateSupplierView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "update_supplier.html"

    login_url = '/login'

    success_url = reverse_lazy("list_suppliers")


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'list.html'
    model = CustomerOrder
    paginate_by = 8

    login_url = '/login'

    def get_queryset(self):
        qs = CustomerOrder.objects.all()
        if self.request.GET:
            qs = CustomerOrder.filter_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = OrderTable(self.object_list)
        RequestConfig(self.request, paginate={"per_page": 8}).configure(orders)
        context.update(locals())
        return context


@login_required(login_url='/login')
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


class CreateSupplierOrderView(LoginRequiredMixin, CreateView):
    model = SupplierOrder
    template_name = "create_supplier_order.html"
    form_class = SupplierOrderForm

    login_url = '/login'

    def get_success_url(self):
        self.new_object.refresh_from_db()
        return reverse('update_supplier_order', kwargs={'pk': self.new_object.id})

    def form_valid(self, form):
        object = form.save()
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)


class SupplierOrderListView(LoginRequiredMixin, ListView):
    template_name = 'list_supplier_order.html'
    model = SupplierOrder
    paginate_by = 8

    login_url = '/login'

    def get_queryset(self):
        qs = SupplierOrder.objects.all()
        if self.request.GET:
            qs = SupplierOrder.filter_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier_orders = SupplierOrderTable(self.object_list)
        RequestConfig(self.request, paginate={"per_page": 8}).configure(supplier_orders)
        context.update(locals())
        return context


class SupplierOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = SupplierOrder
    template_name = 'supplier_order_update.html'
    form_class = SupplierOrderEditForm

    login_url = '/login'

    def get_success_url(self):
        instance = self.object
        return reverse('update_supplier_order', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        qs_p = Part.objects.all()
        parts = PartTableSupplier(qs_p)
        parts.order_by = "-available_stock"
        supplier_order_items = SupplierOrderItemTable(instance.supplier_order_items.all())
        RequestConfig(self.request).configure(parts)
        RequestConfig(self.request).configure(supplier_order_items)
        context.update(locals())
        return context


class SupplierOrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'detail_supplier_order.html'
    model = SupplierOrder
    paginate_by = 50

    login_url = '/login'

    def get_success_url(self):
        return reverse('list_supplier_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        qs = SupplierOrder.objects.filter(id=instance.id)
        supplier_order = SupplierOrderDetailTable(qs)
        RequestConfig(self.request).configure(supplier_order)
        context.update(locals())
        return context


class CreateOrderView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = OrderCreateForm
    model = CustomerOrder

    login_url = '/login'

    def get_success_url(self):
        self.new_object.refresh_from_db()
        return reverse('update_order', kwargs={'pk': self.new_object.id})

    def form_valid(self, form):
        object = form.save()
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomerOrder
    template_name = 'order_update.html'
    form_class = OrderEditForm

    login_url = '/login'

    def get_success_url(self):
        instance = self.object
        order_item = OrderItem.objects.filter(customerOrder=instance)
        for item in order_item:
            if item.part.stock <= item.part.reorder_level:
                supplier_order = SupplierOrder.objects.create(supplier=item.part.supplier)
                supplier_order.part.add(item.part)
                supplier_order_item, created = SupplierOrderItem.objects.get_or_create(supplierOrder=supplier_order,
                                                                                       part=item.part)
                if created:
                    supplier_order_item.quantity = item.part.order_quantity
                    supplier_order_item.price = item.part.cost
                else:
                    supplier_order_item.quantity = item.part.order_quantity

                item.part.item_in_order = item.part.order_quantity
                item.part.save()
                supplier_order_item.save()
                supplier_order.save()

        return reverse('update_order', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        qs_p = Part.objects.all()
        parts = PartTable(qs_p)
        parts.order_by = "-available_stock"
        order_items = OrderItemTable(instance.order_items.all())
        RequestConfig(self.request, paginate={"per_page": 10}).configure(parts)
        RequestConfig(self.request).configure(order_items)
        context.update(locals())
        return context


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def ajax_search_parts_supplier(request, pk):
    instance = get_object_or_404(SupplierOrder, id=pk)
    q = request.GET.get('q', None)
    parts = Part.objects.filter(name__startswith=q)
    parts = parts[:12]
    parts = PartTableSupplier(parts, order_by="-available_stock")
    RequestConfig(request).configure(parts)
    data = dict()
    data['parts'] = render_to_string(template_name='include/supplier_product_container.html',
                                     request=request,
                                     context={
                                         'parts': parts,
                                         'instance': instance
                                     })
    return JsonResponse(data)


@login_required(login_url='/login')
def order_action_view(request, pk, action):
    instance = get_object_or_404(CustomerOrder, id=pk)
    if action == 'is_paid':
        instance.status = True
        instance.save()
    if action == 'delete':
        if not instance.confirm:
            instance.delete()
    return redirect(reverse('home'))


@login_required(login_url='/login')
def ajax_add_product(request, pk, dk):
    instance = get_object_or_404(CustomerOrder, id=pk)
    part = get_object_or_404(Part, id=dk)
    if not part.available_stock == 0:
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
    all_parts = PartTable(Part.objects.all())
    all_parts.order_by = "-available_stock"
    order_items = OrderItemTable(instance.order_items.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(all_parts)
    RequestConfig(request).configure(order_items)
    data = dict()
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={'instance': instance,
                                               'order_items': order_items
                                               }
                                      )
    data['product'] = render_to_string(template_name='include/product_container.html',
                                       request=request,
                                       context={'instance': instance,
                                                'parts': all_parts,
                                                }
                                       )
    return JsonResponse(data)


@login_required(login_url='/login')
def ajax_add_product_supplier(request, pk, dk):
    instance = get_object_or_404(SupplierOrder, id=pk)
    part = get_object_or_404(Part, id=dk)

    supplier_order_item, created = SupplierOrderItem.objects.get_or_create(supplierOrder=instance, part=part)
    if not instance.confirm:
        if created:
            supplier_order_item.quantity = 1
            supplier_order_item.price = part.cost
        else:
            supplier_order_item.quantity += 1
        supplier_order_item.save()
        part.item_in_order += 1
        part.save()

    instance.refresh_from_db()
    supplier_order_items = SupplierOrderItemTable(instance.supplier_order_items.all())
    all_parts = PartTableSupplier(Part.objects.all())
    all_parts.order_by = "-available_stock"
    RequestConfig(request, paginate={"per_page": 10}).configure(all_parts)
    RequestConfig(request).configure(supplier_order_items)
    data = dict()
    data['result'] = render_to_string(template_name='include/supplier_order_container.html',
                                      request=request,
                                      context={'instance': instance,
                                               'supplier_order_items': supplier_order_items
                                               }
                                      )
    data['product'] = render_to_string(template_name='include/supplier_product_container.html',
                                       request=request,
                                       context={'instance': instance,
                                                'parts': all_parts,
                                                }
                                       )
    return JsonResponse(data)


@login_required(login_url='/login')
def ajax_modify_order_item(request, pk, action):
    order_item = get_object_or_404(OrderItem, id=pk)
    part = order_item.part
    instance = order_item.customerOrder
    if not instance.confirm:
        if action == 'remove':
            order_item.quantity -= 1
            part.reserved_stock -= 1
            if order_item.quantity < 1:
                order_item.quantity = 1
                part.reserved_stock += 1
        if not part.available_stock == 0:
            if action == 'add':
                order_item.quantity += 1
                part.reserved_stock += 1

        part.save()
        order_item.save()

        if action == 'delete':
            order_item.delete()
    data = dict()
    instance.refresh_from_db()
    all_parts = PartTable(Part.objects.all())
    all_parts.order_by = "-available_stock"
    order_items = OrderItemTable(instance.order_items.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(all_parts)
    RequestConfig(request).configure(order_items)
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance,
                                          'order_items': order_items
                                      }
                                      )
    data['product'] = render_to_string(template_name='include/product_container.html',
                                       request=request,
                                       context={'instance': instance,
                                                'parts': all_parts,
                                                }
                                       )
    return JsonResponse(data)


@login_required(login_url='/login')
def ajax_modify_supplier_order_item(request, pk, action):
    supplier_order_item = get_object_or_404(SupplierOrderItem, id=pk)
    part = supplier_order_item.part
    instance = supplier_order_item.supplierOrder
    if not instance.confirm:
        if action == 'remove':
            supplier_order_item.quantity -= 1
            part.item_in_order -= 1
            if supplier_order_item.quantity < 1:
                supplier_order_item.quantity = 1
                part.item_in_order += 1

        if action == 'add':
            supplier_order_item.quantity += 1
            part.item_in_order += 1

        part.save()
        supplier_order_item.save()

        if action == 'delete':
            supplier_order_item.delete()
    data = dict()
    instance.refresh_from_db()
    all_parts = PartTableSupplier(Part.objects.all())
    all_parts.order_by = "-available_stock"
    supplier_order_items = SupplierOrderItemTable(instance.supplier_order_items.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(all_parts)
    RequestConfig(request).configure(supplier_order_items)
    data['result'] = render_to_string(template_name='include/supplier_order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance,
                                          'supplier_order_items': supplier_order_items
                                      }
                                      )
    data['product'] = render_to_string(template_name='include/supplier_product_container.html',
                                       request=request,
                                       context={'instance': instance,
                                                'parts': all_parts,
                                                }
                                       )
    return JsonResponse(data)


@login_required(login_url='/login')
def delete_order(request, pk):
    instance = get_object_or_404(CustomerOrder, id=pk)
    if not instance.confirm:
        instance.delete()
        messages.warning(request, 'The order is deleted!')
        return redirect(reverse('home'))
    else:
        return redirect((reverse('control_orders')))


@login_required(login_url='/login')
def delete_supplier_order(request, pk):
    instance = get_object_or_404(SupplierOrder, id=pk)
    if not instance.confirm:
        instance.delete()
        messages.warning(request, 'The supplier order is deleted!')
        return redirect(reverse('home'))
    else:
        return redirect((reverse('control_orders')))
