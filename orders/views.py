from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import Q, Sum
from .models import Order
from .forms import OrderForm, OrderStatusForm, DishForm  # Добавлен импорт DishForm
from django.contrib.auth.decorators import login_required
import json

@login_required
def order_list(request: HttpRequest) -> HttpResponse:
    """
    Отображает список всех заказов.
    """
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def add_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            dish_form = DishForm(request.POST, prefix='dish')
            if dish_form.is_valid():
                dish = {
                    "name": dish_form.cleaned_data['name'],
                    "price": float(dish_form.cleaned_data['price']),
                }
                order.items = json.dumps([dish])
                order.total_price = dish['price']
                order.save()
                return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/add_order.html', {'form': form})

def delete_order(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Удаляет заказ по его ID.
    """
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')

def search_orders(request):
    query = request.GET.get('q', '').strip()  # Получаем поисковый запрос

    if query:
        if query.isdigit():
            orders = Order.objects.filter(table_number=int(query))
        else:
            status_mapping = {status[1].lower(): status[0] for status in Order.STATUS_CHOICES}
            status_query = query.lower()
            if status_query in status_mapping:
                orders = Order.objects.filter(status__iexact=status_mapping[status_query])
            else:
                orders = Order.objects.none()
    else:
        orders = Order.objects.all()

    return render(request, 'orders/order_list.html', {'orders': orders})

def change_status(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Изменяет статус заказа.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'orders/change_status.html', {'form': form})

def calculate_revenue(request: HttpRequest) -> HttpResponse:
    """
    Рассчитывает общую выручку за смену.
    """
    revenue = Order.objects.filter(status='paid').aggregate(total_revenue=Sum('total_price'))
    return render(request, 'orders/revenue.html', {'revenue': revenue['total_revenue'] or 0})

def edit_order(request, order_id):
    """
    Редактирует существующий заказ.
    """
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            dish_form = DishForm(request.POST, prefix='dish')
            if dish_form.is_valid():
                # Обновляем данные блюда
                dish = {
                    "name": dish_form.cleaned_data['name'],
                    "price": float(dish_form.cleaned_data['price']),
                }
                order.items = json.dumps([dish])  # Сохраняем обновлённое блюдо
                order.total_price = dish['price']  # Обновляем общую стоимость
                order.save()
                return redirect('order_list')
    else:
        # Загружаем текущие данные заказа
        initial_data = {}
        if order.items:  # Проверяем, что поле items не пустое
            try:
                items = json.loads(order.items)  # Пытаемся загрузить JSON
                if items:  # Если есть блюда, загружаем первое (и единственное) блюдо
                    initial_data = {
                        'name': items[0]['name'],
                        'price': items[0]['price'],
                    }
            except json.JSONDecodeError:
                # Если JSON некорректен, оставляем initial_data пустым
                pass
        
        # Инициализируем формы с текущими данными
        form = OrderForm(instance=order)
        dish_form = DishForm(prefix='dish', initial=initial_data)
    
    return render(request, 'orders/edit_order.html', {
        'form': form,
        'dish_form': dish_form,
        'order': order,
    })