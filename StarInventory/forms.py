from django import forms

from StarInventory.models import Part, Customer, Supplier, CustomerOrder, SupplierOrder


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = (
            'manufacturer_number', 'name', 'stock', 'cost', 'reorder_level', 'order_quantity', 'description',
            'manufacturer',
            'supplier')
        widgets = {
            'manufacturer_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Manufacture number'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
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


class SupplierOrderForm(forms.ModelForm):
    class Meta:
        model = SupplierOrder
        fields = ('date', 'supplier')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'})
        }


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SupplierOrderEditForm(BaseForm, forms.ModelForm):
    class Meta:
        model = SupplierOrder
        fields = ('date', 'supplier', 'status')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-control'})
        }


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
        fields = ('date', 'customer', 'status')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-control'})
        }
