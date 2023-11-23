from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/',views.register, name='register'),
    path('logout/',views.logout_user,name='logout'),
    path('products/',views.add_products, name='products'),
    path('product/<str:pk>/',views.product_info, name='product_info')
]