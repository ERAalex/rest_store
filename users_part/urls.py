from django.urls import include, path
from .views import ActivateUser, ContactUserApiView

from rest_framework import routers
router = routers.SimpleRouter()


urlpatterns = [
    path('users/', include(router.urls)),
    path('activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),

    path('contacts/<int:pk>', ContactUserApiView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update'})),
    path('contacts/', ContactUserApiView.as_view({
        'get': 'list',
        'post': 'create'})),
]
