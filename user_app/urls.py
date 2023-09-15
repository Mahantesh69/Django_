from django.urls import path,include
from django.contrib import admin
from user_app import views

urlpatterns=[
    path('',views.home,name='home'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('add_emp',views.add_emp,name='add_emp'),
    path('view_all',views.view_all,name='view_all'),
    path('BackBtn',views.BackBtn,name='BackBtn'),
    path('update/<emp_PIN>',views.update, name='update'), 
    path('do_update/<emp_PIN>',views.do_update, name='do_update'), 
    path('remove',views.remove,name='remove'),
    path('filter_emp',views.filter_emp,name='filter_emp'),
    path('upload',views.upload,name='upload'),



    path('delete_all/<emp_PIN>',views.delete_all ,name='delete_all'),

    path('remove/<emp_PIN>',views.remove,name='remove'),
    path('sign_in',views.sign_in,name='sign_in'),
    path('sign_out',views.sign_out,name='sign_out'),
    path('activate/<uidb64><token>',views.activate,name='activate'),
    

]