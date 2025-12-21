from django import forms
class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 60px'
        })
    )


    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )