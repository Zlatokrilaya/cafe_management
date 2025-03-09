from django.db import models
from django.core.exceptions import ValidationError
import json

class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    items = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"

    def display_items(self):
        items_list = json.loads(self.items)
        return "\n".join([f"{item['name']} - {item['quantity']} шт. - {item['price']} руб." for item in items_list])
    
    @property
    def items_list(self):
        """
        Преобразует строку items в список словарей.
        """
        try:
            # Если items хранится как JSON, преобразуем его в список
            return json.loads(self.items)
        except json.JSONDecodeError:
            # Если items хранится как текст, пытаемся преобразовать его обратно в список
            items = []
            for line in self.items.split("\n"):
                if " - " in line:
                    name, price = line.split(" - ")
                    price = price.replace(" руб.", "")
                    items.append({"name": name, "price": float(price)})
            return items

    table_number = models.IntegerField()
    items = models.TextField()  # Поле для хранения текста или JSON
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"

    def clean(self):
        """
        Проверяет, что items содержит корректные данные.
        """
        try:
            items = self.items_list
            if not isinstance(items, list):
                raise ValidationError({'items': 'Items must be a list.'})
            for item in items:
                if not isinstance(item, dict) or 'name' not in item or 'price' not in item:
                    raise ValidationError({'items': 'Each item must be a dictionary with "name" and "price" keys.'})
        except (json.JSONDecodeError, ValueError):
            raise ValidationError({'items': 'Invalid format for items.'})

    def save(self, *args, **kwargs):
        """
        Преобразует список товаров в читаемый текст перед сохранением.
        """
        items = self.items_list
        if isinstance(items, list):
            # Преобразуем список товаров в читаемый текст
            self.items = "\n".join([f"{item['name']} - {item['price']} руб." for item in items])
            self.total_price = sum(item.get('price', 0) for item in items)
        else:
            self.items = "Нет данных о заказе"
            self.total_price = 0
        super().save(*args, **kwargs)

    def display_items(self):
        """
        Возвращает строку с понятным описанием заказа.
        """
        return self.items