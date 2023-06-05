from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('users_part.urls')),
    path('', include('products.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
]

urlpatterns += doc_urls

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
