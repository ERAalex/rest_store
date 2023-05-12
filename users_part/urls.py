from django.urls import include, path
from .views import ActivateUser

from rest_framework import routers
router = routers.SimpleRouter()


urlpatterns = [
    path('users/', include(router.urls)),
    path('activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
]
