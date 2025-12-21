from django.shortcuts import render,redirect
from authentication.forms import ProfileUpdateForm,CustomSignupForm,ShippingInfoForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import authenticate
from .models import CustomerProfile
from django.contrib.auth.decorators import login_required
from allauth.account.forms import Login
from allauth.account.views import SignupView
from .forms import CustomUserChange
from django.contrib.auth.forms import UserChangeForm
# custom signup view for registering users inherits from signupview
# it accepts CustomSignupForm class , which is available in the template
# form valid calls the validation function in the parent class 
class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'account/custom_signup.html'
    
    def form_valid(self, form):
        return super().form_valid(form)

@login_required
def profile(request):
    return render(request,"authentication/profile.html")
@login_required
def shippinginfo(request):
    shippinginfo = ShippingInfoForm()
    if request.method == "POST":
        shippinginfo  = ShippingInfoForm(request.POST,instance=request.user.shippinginfo)
        
        if shippinginfo.is_valid():
            shippinginfo.save()
            messages.info(request,"sucessfully updated")
            return redirect("storefront_home")
    else:
        shippinginfo = ShippingInfoForm(instance=request.user.shippinginfo)
    return render(request,"authentication/shipping_info.html",{"form":shippinginfo})

# def signup(request):
#     if request.method == "POST":
#         form = CustomUserCreation(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data["email"]
#             if User.objects.filter(email=email).exists():
#                 print("test")
#                 messages.info(request,"the email is linked to another account")
#                 return redirect("user_signup")
#             if not  email.endswith("@gmail.com"):
#                 messages.info(request,"we accept only gmail")
#                 return redirect("user_signup")
#             form.save(request)
#             return  redirect("user_signin")
#     else:
#         form = CustomUserCreation()
#     return render(request,"authentication/signup.html",{"form":form,"title":"Sign Up"})
# def signin(request):
#     if request.method == "POST":
#         email = request.POST["email"]
#         password = request.POST["password"]
#         print(email)
#         if not User.objects.filter(email=email).exists():
#             msg = messages.warning(request,"Invalid Email Address")
#             print(msg)
#             return redirect("user_signin")
        
#         user = authenticate(email,password)
#         if user is  None :
#             messages.warning(request,"password is incorrect")
#             return redirect("user_signin")
#         else:
#             print(request.user.username)
#             login(request,user)
#             return redirect("storefront_home")
#     return render(request,"authentication/signin.html",{"title":"Sign In"})

# Create your views here.
def test(request):
    return render(request,"authentication/test.html")

def update_info(request):
    profileform = ProfileUpdateForm(instance = request.user.customerprofile)
    form = CustomUserChange(instance = request.user)
    if request.method == "POST":
            form = CustomUserChange(request.POST,instance=request.user)
            print(form.is_valid())
           
            form.save()
            messages.success(request,"Information Update")
            return redirect("storefront_home")
    return render(request,"authentication/update_info.html",{"form":form,"profileform":profileform})

def update_add_info(request):
    profileform = ProfileUpdateForm()
    if request.method == "POST":
        profileform  = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.customerprofile)
        if profileform.is_valid():
            profileform.save()
            messages.info(request,"sucessfully updated")
            return redirect("storefront_home")
      
    return redirect("storefront_home")
