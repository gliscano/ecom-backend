from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from stores import views

 
urlpatterns = [ 
    path('stores/', views.StoreList.as_view()),
    path('stores/<int:pk>', views.StoreDetail.as_view()),
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>', views.ProductDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>', views.CategoryDetail.as_view()),
    path('subcategories/<int:pk>', views.SubCategoryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)