from django.contrib import admin
from StarInventory.models import Customer, Supplier, OrderItem, CustomerOrder, Part, SupplierOrder

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(OrderItem)
admin.site.register(CustomerOrder)
admin.site.register(Part)
admin.site.register(SupplierOrder)
