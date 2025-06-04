from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'address', 
            'postal_code', 
            'city'
        ]
        # You can customize widgets or labels here if needed, for example:
        # widgets = {
        #     'address': forms.Textarea(attrs={'rows': 3}),
        # }
        # labels = {
        #     'postal_code': 'ZIP / Postal Code',
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mb-2'}) # Add a common CSS class