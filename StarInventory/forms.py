from django import forms

from StarInventory.models import Part


class PartCreateForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ('name','stock','cost','reorder_level','order_quantity','reserved_stock','description','manufacturer','supplier')
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

