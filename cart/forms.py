from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # When the cart is added(False) if we overrite the quantity(True)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
