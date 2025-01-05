from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add-item/', views.add_item, name='add_item'),
    path('create-order/', views.create_order, name='create_order'),
    path('order-log/', views.order_log, name='order_log'),
    path('update-stock/<int:pk>/', views.update_stock, name='update_stock'),
]
