from django.db import models

# Create your models here.

class Product(models.Model):
     product_id = models.AutoField
     product_name = models.CharField(max_length=50)
     category = models.CharField(max_length=50 , default="")
     subcategory = models.CharField(max_length=50 , default="")
     price = models.IntegerField(default=0)
     description = models.CharField(max_length=200)
     pub_date = models.DateField()
     image = models.ImageField(upload_to="shop/images" , default="")

     def __str__(self):
          return self.product_name

class Contact(models.Model):
     msg_id = models.AutoField(primary_key=True)
     name = models.CharField(max_length=50)
     email = models.CharField(max_length=50 , default="")
     phone = models.IntegerField(default=0)
     message = models.CharField(max_length=50 , default="")

     def __str__(self):
          return self.name

class Orders(models.Model):
     order_id = models.AutoField(primary_key=True)
     itemjason = models.CharField(max_length=5000)
     name = models.CharField(max_length=256)
     email = models.CharField(max_length=256)
     address = models.CharField(max_length=256)
     city = models.CharField(max_length=256)
     state = models.CharField(max_length=256)
     zip = models.CharField(max_length=256)
     phone = models.CharField(max_length=256)

     

class OrderUpdate(models.Model):
     update_id = models.AutoField(primary_key=True)
     order_id = models.IntegerField(default="")
     update_desc = models.CharField(max_length=5000)
     timestamp = models.DateField(auto_now_add=True)

def __str__(self):
     return self.update_desc[0:10] + "..." 