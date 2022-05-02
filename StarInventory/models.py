from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Customer(models.Model):
    name = models.CharField(null=False, blank=False, max_length=50)
    phoneNumber = models.CharField(null=False, blank=False, max_length=15)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(Customer, self).save(*args, **kwargs)


class Supplier(models.Model):
    name = models.CharField(null=False, blank=False, max_length=50)
    phoneNumber = models.CharField(null=False, blank=False, max_length=15)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(Supplier, self).save(*args, **kwargs)


class Part(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)
    stock = models.IntegerField(null=False, blank=False, default=0)
    cost = models.FloatField(null=False, blank=False)
    reorder_level = models.IntegerField(null=False, blank=False, default=0)
    order_quantity = models.IntegerField(null=False, blank=False, default=20)
    reserved_stock = models.IntegerField(null=False, blank=False, default=0)
    description = models.TextField(null=False, blank=False, max_length=100)
    manufacturer = models.CharField(null=False, blank=False, max_length=20)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(null=False, default=False)
    date = models.DateField(_("Date"), default=datetime.date.today)
    part = models.ManyToManyField(Part, through="OrderItem")

    def __str__(self):
        return f"{self.id} - {self.customer.name} order"


class OrderItem(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    customerOrder = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f"{self.customerOrder.id} - {self.part.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('part', 'customerOrder'), name='once_per_customerOrder_part')
        ]


class SupplierOrder(models.Model):
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    date = models.DateField(_("Date"), default=datetime.date.today)
