from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('User_home.urls')),
    path('', include('userAuth.urls')),
    path('',include('Admin_auth.urls')),
    path('', include('Admin_home.urls')),
    path('',include('Cart.urls')),
    path('', include('Userprofile.urls')),
    path('', include('order_manage.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)