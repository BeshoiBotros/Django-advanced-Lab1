from django.contrib import admin

from .models import Customer, Employee, Shipper, Category, Product, Order, OrderDetail

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Shipper)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
