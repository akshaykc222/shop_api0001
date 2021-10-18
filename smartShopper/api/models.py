from django.contrib.auth.models import AbstractUser, User
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    icon = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='sub_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)


class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)

    def __str__(self):
        return self.size_name


class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=100)

    def __str__(self):
        return self.variant_name


class ColorVariant(models.Model):
    color_name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name


class Product(models.Model):
    category = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    market_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    stock = models.IntegerField(default=5)
    quantity_type = models.ForeignKey(QuantityVariant, blank=True, null=True, on_delete=models.PROTECT)
    color_type = models.ForeignKey(ColorVariant, blank=True, null=True, on_delete=models.PROTECT)
    size_type = models.ForeignKey(SizeVariant, blank=True, null=True, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_added",)

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.ImageField(upload_to="uploads/")


class Favourite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isFavourite = models.BooleanField(default=False)

    def __str__(self):
        return f'ProductId ={self.product.id}user={self.user.username}|isFavourite={self.isFavourite}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    isComplete = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User= {self.user.username}|isComplete={self.isComplete}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Quantity=={self.quantity}"


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"Cart=={self.cart.id}<==>phone:{self.phone}==address=={self.address}"

# class User(AbstractUser):
#     phone_regex = Regex
