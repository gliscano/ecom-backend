from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views
from users import views

urlpatterns = [ 
    path('users/', views.UserList.as_view()),

    path('users/<int:pk>', views.UserDetail.as_view()),
    path('address/', views.AddressList.as_view()),
    path('address/<int:pk>', views.AddressDetail.as_view()),
    path('email/verification/<token>', views.VerifyEmail.as_view(), name='email_verify'),

        path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
     path('create/', views.CustomUserCreate.as_view(), name="create_user"),
]

urlpatterns = format_suffix_patterns(urlpatterns)