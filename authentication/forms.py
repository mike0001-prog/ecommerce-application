from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomerProfile,ShippingInfo
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth.forms import UserChangeForm

class CustomUserChange(UserChangeForm):

    # def __init__(self, *args, **kwargs):
    #     for field_name,field in self.fields.items():
    #         field.widget.attrs["class"] = "form-control"
    #     super().__init__(*args, **kwargs)
    class Meta:
        model = User
        fields = ["last_name","first_name","username"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ["user_image","user_address"]

class ShippingInfoForm(forms.ModelForm):
    recipient_name = forms.CharField(max_length=20, label="Recipient Name",)
    recipient_phone = forms.CharField(max_length=11, label="Recipient Phone")
    lg_area = forms.CharField(max_length=11, label="Local Goverment Area")
    recipient_address = forms.Textarea()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("recipient_name", css_class="col-md-6"),
                Column("recipient_phone", css_class="col-md-6"),
                css_class="mb-3"
            ),
            Row(
                Column("lg_area", css_class="col-md-12"),
                css_class="mb-3"
            ),
             Row(
                Column("recipient_address", css_class="col-md-12"),
                css_class="mb-3"
            )
        )
    class Meta:
        model = ShippingInfo
        fields = ["recipient_name","recipient_phone","lg_area","recipient_address"]













# forms.py



# class ProfileForm(forms.Form):
#     first_name = forms.CharField(max_length=50, label="First Name")
#     last_name = forms.CharField(max_length=50, label="Last Name")
#     email = forms.EmailField(label="Email")
#     phone = forms.CharField(max_length=15, label="Phone")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = "post"
#         self.helper.layout = Layout(
#             Row(
#                 Column("first_name", css_class="col-md-6"),
#                 Column("last_name", css_class="col-md-6"),
#                 css_class="mb-3"
#             ),
#             Row(
#                 Column("email", css_class="col-md-6"),
#                 Column("phone", css_class="col-md-6"),
#                 css_class="mb-3"
#             ),
#             Submit("submit", "Submit", css_class="btn btn-primary")
#         )

# from allauth.account.forms import SignupForm
# from allauth.account.decorators import verified_email_required
# class CustomUserCreation(SignupForm):
#     last_name = forms.CharField(max_length = 40)
#     first_name = forms.CharField(max_length = 40)
#     class Meta:
#         model = User
#         fields = ["email","username","last_name","first_name"]
#         ordering = ("email",)
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user