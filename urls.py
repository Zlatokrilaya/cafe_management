from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from orders import views  # Импортируем views из приложения orders

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.order_list, name='order_list'),  # Главная страница
    path('orders/', include('orders.urls')),  # URL-адреса приложения orders
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit/<int:order_id>/', views.edit_order, name='edit_order'),
]