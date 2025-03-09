from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('search/', views.search_orders, name='search_orders'),
    path('change_status/<int:order_id>/', views.change_status, name='change_status'),
    path('edit/<int:order_id>/', views.edit_order, name='edit_order'),  # Новый маршрут
    path('revenue/', views.calculate_revenue, name='calculate_revenue'),
]