from decimal import Decimal

from django.db import models
import datetime

from django.db.models import Sum
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.conf import settings

CURRENCY = settings.CURRENCY


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
    cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=20, null=False, blank=False)
    reorder_level = models.IntegerField(null=False, blank=False, default=0)
    order_quantity = models.IntegerField(null=False, blank=False, default=20)
    reserved_stock = models.IntegerField(null=False, blank=False, default=0)
    available_stock = models.IntegerField(null=False, blank=False, default=0)
    description = models.TextField(null=False, blank=False, max_length=100)
    manufacturer = models.CharField(null=False, blank=False, max_length=20)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.available_stock = self.stock - self.reserved_stock
        super().save(*args, **kwargs)


class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(null=False, default=False)
    date = models.DateField(_("Date"), default=datetime.date.today)
    part = models.ManyToManyField(Part, through="OrderItem")
    value = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.id} - {self.customer.name} order"

    def get_edit_url(self):
        return reverse('update_order', kwargs={'pk': self.id})

    def tag_final_value(self):
        return f'{CURRENCY} {self.value}'

    def save(self, *args, **kwargs):
        order_items = self.order_items.all()
        self.value = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        super().save(*args, **kwargs)

    @staticmethod
    def filter_data(request, queryset):
        date_start = request.GET.get('date_start', None)
        date_end = request.GET.get('date_end', None)
        if date_end and date_start and date_end >= date_start:
            date_start = datetime.datetime.strptime(date_start, '%m/%d/%Y').strftime('%Y-%m-%d')
            date_end = datetime.datetime.strptime(date_end, '%m/%d/%Y').strftime('%Y-%m-%d')
            print(date_start, date_end)
            queryset = queryset.filter(date__range=[date_start, date_end])
        return queryset


class OrderItem(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    customerOrder = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(null=False, blank=False, default=1)
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)



    def __str__(self):
        return f"{self.part.name}"

    def save(self, *args, **kwargs):
        self.total_price = Decimal(self.quantity) * Decimal(self.part.cost)
        super().save(*args, **kwargs)
        self.customerOrder.save()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('part', 'customerOrder'), name='once_per_customerOrder_part')
        ]


@receiver(post_delete, sender=OrderItem)
def delete_order_item(sender, instance, **kwargs):
    part = instance.part
    part.stock += instance.quantity
    part.save()
    instance.customerOrder.save()


class SupplierOrder(models.Model):
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    date = models.DateField(_("Date"), default=datetime.date.today)
