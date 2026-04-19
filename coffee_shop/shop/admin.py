from django.contrib import admin
from .models import Product, Category, Order, OrderItem
from .models import ContactMessage
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'