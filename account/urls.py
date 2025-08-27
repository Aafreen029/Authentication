from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
   path('',views.index,name = 'accounts'),
   path('login/',views.loginViews,name='login'),
   path('signup/',views.signup,name='signup'),
   path('logout/',views.logoutViews,name='logout'),
   path('forget-password/',views.ForgetPassword,name='forget_password'),
   path('change-password/<token>/',views.ChangePassword,name='change_password'),
   path('get-customer/', views.getCustomer, name='getCustomer'),
   path('add_customer/', views.add_customer, name='add_customer'),
   path('edit_customer/<customer_id>', views.edit_customer, name='edit_customer'),
   path('delete_customer/<customer_id>', views.delete_customer, name='delete_customer'), 
   

]