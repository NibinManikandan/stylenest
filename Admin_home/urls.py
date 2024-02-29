from django.urls import path
from . import views



urlpatterns = [
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('users/', views.User_list, name='users'),
    path('users/user_status/<str:id>/', views.user_status, name = 'user_status'),

    path('adm_products/', views.products_list, name='adm_products'),
    path('adm_products/prod_sts/<str:id>/', views.product_status, name = 'prod_sts'),
    path('add_product/', views.add_products, name = 'add_product'),
    path('edit_product/<str:id>', views.Edit_product, name='edit_product'),

    path('adm_category/', views.admin_catogory, name = 'adm_category'),
    path('adm_category/category_status/<str:id>/', views.category_status, name='category_status'),
    path('add_category/', views.add_category, name = 'add_category'),
    path('adm_category/edit_category/<int:id>/', views.edit_category, name='edit_category'),

    path('admin_logout/', views.admin_logout, name = 'admin_logout'),
    
]    