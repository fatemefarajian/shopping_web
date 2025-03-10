from django.db import models

from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_post_cost(self):
        total_weight = sum(item.get_weight() for item in self.items.all())

        if total_weight == 0:
            return 0
        elif total_weight < 1000:
            return 20000
        elif 1000 < total_weight < 2000:
            return 30000
        else:
            return 50000

    def get_final_cost(self):
        final_price = self.get_total_cost() + self.get_post_cost()
        return final_price

    def __str__(self):
        return f"order: {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.weight * self.quantity

    def __str__(self):
        return f"{self.id}"

