from django.urls import path
from . import views



urlpatterns = [
    path('dashboard/', views.Dashboard, name='dashboard'),

    path('users/', views.User_list, name='users'),
    path('users/user_status/<str:id>/', views.user_status, name = 'user_status'),

    path("sales_report/", views.sales_report, name="sales_report"),
    path('pdf_download1/', views.DownloadPDF1.as_view(), name="pdf_download1"),
    path('pdf_download2/', views.DownloadPDF2.as_view(), name="pdf_download2"),
    path('pdf_download3/', views.DownloadPDF3.as_view(), name="pdf_download3"),

    path('download_exel1',views.download_exel1,name='download_exel1'),
    path('download_exel2',views.download_exel2,name='download_exel2'),
    path('download_exel3',views.download_exel3,name='download_exel3'),

    path('adm_products/', views.products_list, name='adm_products'),
    path('adm_products/prod_sts/<str:id>/', views.product_status, name = 'prod_sts'),
    path('add_product/', views.add_products, name = 'add_product'),
    path('edit_product/<str:id>', views.Edit_product, name='edit_product'),

    path('adm_category/', views.admin_catogory, name = 'adm_category'),
    path('adm_category/category_status/<str:id>/', views.category_status, name='category_status'),
    path('add_category/', views.add_category, name = 'add_category'),
    path('adm_category/edit_category/<int:id>/', views.edit_category, name='edit_category'),

    path('adm_orders/', views.adm_orders, name='adm_orders'),
    path('adm_orders/order_status_change/<str:id>', views.order_status_change, name='order_status_change'),

    path('offers/', views.offers, name='offers'),
    path('productOffer/', views.productOffer, name='productOffer'),
    path('addProductOffer/', views.addProductOffer, name='addProductOffer'),
    path('productOffer/edit_prod_offer/<str:id>', views.edit_prod_offer, name='edit_prod_offer'),
    path('productOffer/cancel_prod_offer/<str:id>', views.cancel_prod_offer, name='cancel_prod_offer'),

    path('cateOffer/', views.cateOffer, name='cateOffer'),
    path('add_cate_offers/', views.add_cate_offers, name='add_cate_offers'),
    path('cateOffer/edit_cate_offer/<str:id>', views.edit_cate_offer, name='edit_cate_offer'),
    path('cateOffer/cancel_category_offers/<str:id>', views.cancel_category_offers, name='cancel_category_offers'),

    path('banners/', views.banners, name='banners'),
    path('add_banners/', views.add_banners, name='add_banners'), 
    path('banner_controlling/<str:id>/', views.banner_controlling, name='banner_controlling'),

    path('admin_logout/', views.admin_logout, name = 'admin_logout'),
    
]    