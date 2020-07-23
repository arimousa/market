from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    inventory = models.IntegerField(default=0)

    def increase_inventory(self, amount):
        self.inventory += amount

    def decrease_inventory(self, amount):
        self.inventory -= amount

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    phone = models.CharField(max_length=20, default=None)
    address = models.TextField(default=None)
    balance = models.IntegerField(default=20000)

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def spend(self, amount):
        self.balance -= amount
        self.save()

    def __str__(self):
        return self.user.username


class OrderRow(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    order = models.ForeignKey('Order', on_delete=models.PROTECT)
    amount = models.IntegerField()

    def __str__(self):
        return self.product.name


class Order(models.Model):
    # Status values. DO NOT EDIT
    STATUS_SHOPPING = 1
    STATUS_SUBMITTED = 2
    STATUS_CANCELED = 3
    STATUS_SENT = 4

    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)
    # row = models.ForeignKey('OrderRow', on_delete=models.PROTECT)

    statues_choices = (
        (STATUS_SHOPPING, 'در حال خرید'),
        (STATUS_SUBMITTED, 'ثبت‌شده'),
        (STATUS_CANCELED, 'لغوشده'),
        (STATUS_SENT, 'ارسال‌شده'),
    )
    status = models.IntegerField(choices=statues_choices)
    amount = 0
    product = Product()

    @staticmethod
    def initiate(customer):
        Order.customer = customer

    def add_product(self, product, amount):
        if amount < product.inventory and not amount == 0:
            product.inventory -= amount
            product.save()
            self.status = 1
            self.total_price = amount * product.price
            self.amount = amount
            self.product = product
            self.save()

    def remove_product(self, product, amount=None):
        product.inventory += self.amount
        product.save()
        self.save()

    def submit(self):
        self.status = 2
        self.customer.balance -= self.total_price
        self.customer.save()
        self.save()

    def cancel(self):
        self.status = 3
        self.customer.balance += self.total_price
        self.save()

    def send(self):
        self.status = 4
        orderRow = OrderRow(order=self, product=self.product, amount=self.amount)
        orderRow.save()
        self.save()

    def __str__(self):
        return self.customer.user.username
