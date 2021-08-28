from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from carts import views

 
urlpatterns = [ 
    path('shoping_cart/', views.CartList.as_view()),
    path('shoping_cart/<int:pk>', views.CartDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)