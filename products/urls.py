from django.urls import include, path
from .views import *

from rest_framework import routers
router = routers.SimpleRouter()


urlpatterns = [
    path('shops/upload/', PartnerUpdate.as_view()),
    path('shops', ShopViewSet.as_view({'get': 'list'})),

    path('products', ProductsViewSet.as_view({'get': 'list'})),
    path('products/<id>', ProductsItemViewSet.as_view({'get': 'list'})),

    path('orderitem', OrderItemViewSet.as_view({'get': 'list'})),
    path('orderitem/<pk>', OrderItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('all_ordes_available', PartnerOrdersView.as_view()),

    path('basket', BasketView.as_view()),
    path('basket/change_status', OrderConfirmationByUserView.as_view()),

    path('order_confirmation/', OrderConfirmationByUserView.as_view()),

]
