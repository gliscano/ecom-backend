from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = [ 
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('info/', views.UserAddressInfoAPIView.as_view()),
    path('address_info/', views.UserAddressInfoAPIView.as_view()),
    path('reset_password/<token>', views.ResetPassword.as_view(), name='reset_password'),
    path('forgot_password/', views.ChangePassword.as_view(), name='forgot_password'),
    path('address/', views.AddressList.as_view()),
    path('address/<int:pk>', views.AddressDetail.as_view()),
    path('email/verification/<token>', views.VerifyEmail.as_view(), name='email_verify'),
    path('token/obtain/', views.MyTokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', views.MyTokenObtainPairView.as_view(), name='token_refresh'),
    path('create/', views.CustomUserCreate.as_view(), name="create_user"),
]

urlpatterns = format_suffix_patterns(urlpatterns)