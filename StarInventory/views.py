from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from StarInventory.forms import PartForm, CustomerForm, SupplierForm
from StarInventory.models import Part, Customer, Supplier


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
