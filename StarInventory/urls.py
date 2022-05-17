from django.urls import path

from . import views
from .views import CreatePartView, UpdatePartView, list_parts, list_customers, CreateCustomerView, UpdateCustomerView, \
    list_suppliers, UpdateSupplierView, CreateSupplierView, OrderListView, \
    ajax_calculate_results_view, CreateOrderView, OrderUpdateView, delete_order, ajax_add_product, \
    ajax_modify_order_item, order_action_view, ajax_search_parts, CreateSupplierOrderView, SupplierOrderDetailView, \
    SupplierOrderListView, SupplierOrderUpdateView, ajax_add_product_supplier, ajax_modify_supplier_order_item, \
    delete_supplier_order

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
    path('supplier/order/create', CreateSupplierOrderView.as_view(), name="create_supplier_order"),
    path('supplier/order/update/<int:pk>/', SupplierOrderUpdateView.as_view(), name="update_supplier_order"),
    path('supplier/order/list/', SupplierOrderListView.as_view(), name="list_supplier_order"),
    path('supplier/order/detail/<int:pk>', SupplierOrderDetailView.as_view(), name="detail_supplier_order"),
    path('supplier/orders/delete/<int:pk>/', delete_supplier_order, name='delete_supplier_order'),
    path('customer/orders/list', OrderListView.as_view(), name="list_orders"),
    path('customer/orders/create', CreateOrderView.as_view(), name='create-order'),
    path('customer/orders/update/<int:pk>/', OrderUpdateView.as_view(), name='update_order'),
    path('customer/orders/delete/<int:pk>/', delete_order, name='delete_order'),
    path('customer/orders/action/<int:pk>/<slug:action>/', order_action_view, name='order_action'),


    #  ajax_calls
    path('ajax/search-products/<int:pk>/', ajax_search_parts, name='ajax-search'),
    path('ajax/add-product/<int:pk>/<int:dk>/', ajax_add_product, name='ajax_add'),
    path('ajax/modify-product/<int:pk>/<slug:action>', ajax_modify_order_item, name='ajax_modify'),
    path('ajax/calculate-results/', ajax_calculate_results_view, name='ajax_calculate_result'),
    path('ajax/add-product-supplier/<int:pk>/<int:dk>', ajax_add_product_supplier, name="ajax_add_supplier"),
    path('ajax/modify-product-supplier/<int:pk>/<slug:action>', ajax_modify_supplier_order_item, name='ajax_modify_supplier'),
]
