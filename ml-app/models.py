from django.db import models

class Customer(models.Model):
    companyName = models.CharField(max_length=100)
    contactName = models.CharField(max_length=100)
    contactTitle = models.CharField(max_length=100)
    city = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.companyName

class Category(models.Model):
    categoryName = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.categoryName


class Employee(models.Model):
    employeeName = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    reportsTo = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )

    def __str__(self):
        return self.employeeName


class Shipper(models.Model):
    companyName = models.CharField(max_length=100)

    def __str__(self):
        return self.companyName


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='orders')
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True, related_name='orders')

    orderDate = models.DateTimeField()
    requiredDate = models.DateTimeField(blank=True, null=True)
    shippedDate = models.DateTimeField(blank=True, null=True)
    freight = models.DecimalField(max_digits=10, decimal_places=2)

    products = models.ManyToManyField('Product', through='OrderDetail', related_name='orders')

    def __str__(self):
        return f"Order #{self.id} - {self.customer.companyName}"

class Product(models.Model):
    productName = models.CharField(max_length=100)
    quantityPerUnit = models.CharField(max_length=100)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    discontinued = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.productName



class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details')
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.order} - {self.product} ({self.quantity} units)"
