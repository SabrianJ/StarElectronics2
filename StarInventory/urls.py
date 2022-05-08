from django.urls import path

from . import views
from .views import CreatePartView, UpdatePartView, list_parts, list_customers, CreateCustomerView, UpdateCustomerView, \
    list_suppliers, UpdateSupplierView, CreateSupplierView, list_orders

urlpatterns = [
    path('', views.index, name='home'),
    path('part/create', CreatePartView.as_view(), name="create_part"),
    path('part/<int:pk>/update', UpdatePartView.as_view(), name="update_part"),
    path('parts', list_parts, name="list_parts"),
    path('customers', list_customers, name="list_customers"),
    path('customer/create', CreateCustomerView.as_view(), name="create_customer"),
    path('customer/<int:pk>/update', UpdateCustomerView.as_view(), name="update_customer"),
    path('suppliers', list_suppliers, name="list_suppliers"),
    path('supplier/create', CreateSupplierView.as_view(), name="create_supplier"),
    path('supplier/<int:pk>/update', UpdateSupplierView.as_view(), name="update_supplier"),
    path('customer/orders', list_orders, name="list_orders")
]