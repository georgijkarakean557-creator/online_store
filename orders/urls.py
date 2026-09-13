from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('pickup-map/', views.pickup_point_map, name='pickup_point_map'),
    path('set-pickup-point/<int:point_id>/', views.set_pickup_point, name='set_pickup_point'),
]