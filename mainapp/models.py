from django.db import models
from userapp.models import User
import uuid

# Create your models here.


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}. {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=64)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    cost = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to="products_images")

    def beautiful_cost(self):
        s = str(self.cost)[::-1]
        output = ""
        for i in range(0, len(s), 3):
            output += s[i : i + 3] + " "
        output = output[::-1]
        return f"{output[1:]} р."

    def __str__(self):
        return f"{self.id}. {self.name}"
    @property
    def brand_info(self):
        return Brand.objects.get(id=self.brand_id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    device_id = models.UUIDField(default=uuid.uuid4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    completed = models.BooleanField(default=False)

    def sum(self):
        return self.quantity * self.product.cost

    def total_sum(self):
        carts = Cart.objects.filter(user=self.user, completed=0)
        return sum([cart.sum() for cart in carts])

    def total_quantity(self):
        carts = Cart.objects.filter(user=self.user, completed=0)
        return sum([cart.quantity() for cart in carts])


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    device_id = models.UUIDField(default=uuid.uuid4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # status = models.BooleanField(default=False)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(
        max_length=50,
        verbose_name="Фамилия имя",
        error_messages={"requared": "Поле должно быть заполнено"},
    )
    adress = models.CharField(max_length=400)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    is_user = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    payment_id = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return f'{"✅" if self.completed else "⏰"} Заказ {self.id}. {self.name}'


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{"✅" if self.order.completed else "⏰"} Заказ {self.order.id}. {self.product.name}'
