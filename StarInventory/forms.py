from django import forms

from StarInventory.models import Part, Customer, Supplier, CustomerOrder


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = (
        'name', 'stock', 'cost', 'reorder_level', 'order_quantity', 'reserved_stock', 'description', 'manufacturer',
        'supplier')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'reserved_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manufacturer'}),
            'supplier': forms.Select(attrs={'class': 'form-control'})
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "phoneNumber", "email")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ("name", "phoneNumber", "email")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = ('date', 'customer')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'customer': forms.Select(attrs={'class': 'form-control'})
        }


class OrderEditForm(BaseForm, forms.ModelForm):

    class Meta:
        model = CustomerOrder
        fields = ['date', 'customer', 'status']
