from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Person(BaseModel):
    first_name = models.CharField(max_length=244, null=True)
    last_name = models.CharField(max_length=244, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=244, null=True)
    address = models.CharField(max_length=244, null=True)
    def __str__(self):
        return self.user.username


class Product(BaseModel):
    title = models.CharField(max_length=244, null=True)
    description = models.TextField(null=True)
    product_type_choices = (('qty', 'QTY'), ('mtr', 'MTR'), ('len', 'LEN'))
    type = models.CharField(max_length=7, null=True, default='LEN', choices=product_type_choices)
    sale_price = models.CharField(max_length=244, null=True)
    purchase_price = models.CharField(max_length=244, null=True)
    stock = models.CharField(max_length=244, null=True)
    def __str__(self):
        return self.title


class OrderProduct(BaseModel):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=244, null=True)
    sale_bill = models.CharField(max_length=244, null=True)
    purchase_bill = models.CharField(max_length=244, null=True)
    
    def save(self, *args, **kwargs):
        sale_bill = str(int(self.product.sale_price) * int(self.quantity))
        purchase_bill = str(int(self.product.purchase_price) * int(self.quantity))
        return super(OrderProduct, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.product.title


class Order(BaseModel):
    customer_name = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='customer_name')
    description = models.TextField(null=True)
    products = models.ManyToManyField(OrderProduct)
    sale = models.CharField(max_length=244, null=True)
    purchase = models.CharField(max_length=244, null=True)
    order_creator = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='order_creator', default=1)
    def __str__(self):
        return self.customer_name.user.username


class Balance(BaseModel):
    title = models.CharField(max_length=244, null=True)
    description = models.TextField(null=True)
    bill = models.CharField(max_length=244, null=True)
    balance_type_choices = (('profit', 'profit'), ('expense', 'expense'), ('sale', 'sale'), ('cashed', 'cashed'))
    balance = models.CharField(max_length=10, null=True, choices=balance_type_choices)
    def __str__(self):
        return self.title
