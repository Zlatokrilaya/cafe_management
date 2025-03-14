from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'display_items', 'total_price', 'status')
    list_filter = ('status',)
    search_fields = ('table_number', 'status')

    def display_items(self, obj):
        """
        Форматирует отображение поля items в административной панели.
        """
        return ", ".join([f"{item['name']} - {item['price']} руб." for item in obj.items])
    display_items.short_description = 'Блюда'