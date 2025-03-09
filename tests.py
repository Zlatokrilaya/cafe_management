from django.test import TestCase, Client
from django.urls import reverse
from orders.models import Order  # Абсолютный импорт
import json

class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(
            table_number=1,
            items=json.dumps([{"name": "Кофе", "price": 100}]),
            total_price=100,
            status='waiting'
        )

    def test_add_order(self):
        response = self.client.post(reverse('add_order'), {
            'table_number': 2,
            'name': 'Чай',
            'price': 50,
            'status': 'waiting'
        })
        self.assertEqual(response.status_code, 302)  # Проверяем редирект
        self.assertEqual(Order.objects.count(), 2)   # Проверяем, что заказ добавлен

    def test_edit_order(self):
        response = self.client.post(reverse('edit_order', args=[self.order.id]), {
            'table_number': 1,
            'name': 'Капучино',
            'price': 150,
            'status': 'ready'
        })
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, 150)  # Проверяем обновлённую цену

    def test_delete_order(self):
        response = self.client.post(reverse('delete_order', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)   # Проверяем, что заказ удалён

    def test_search_orders(self):
        response = self.client.get(reverse('search_orders'), {'q': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Кофе")  # Проверяем, что заказ найден