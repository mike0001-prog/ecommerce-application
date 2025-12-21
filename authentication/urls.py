from django.urls import path
from authentication.views import CustomSignupView,profile,shippinginfo,update_info,update_add_info
urlpatterns = [
    path('signup/',CustomSignupView.as_view(),name="user_signup" ),
    path('profile/',profile,name="user_profile" ),
    path('Shippinginfo/',shippinginfo,name="user_shipping" ),
    path('update_basic_info/',update_info,name="user_update" ),
    path('update_add_info/',update_add_info,name="user_basic" ),
    # path('checkprofile/',profileview,name="user_profile_view"),
    # path('test/',test,name="test_view")
]