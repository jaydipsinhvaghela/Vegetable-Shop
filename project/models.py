from django.db import models

class seller(models.Model):
    name = models.CharField(max_length = 150)
    email = models.CharField(max_length = 150)
    password = models.CharField(max_length = 20)
    contact = models.ImageField(default = 0)
    description = models.CharField(max_length = 200)
    city = models.CharField(max_length = 50)
    address = models.CharField(max_length = 150)
    pincode = models.IntegerField(default = 0)
    state = models.CharField(max_length = 50)
    isdeleted = models.IntegerField(default = 0)

class user(models.Model):
    name = models.CharField(max_length = 150)
    email = models.CharField(max_length = 150)
    password = models.CharField(max_length = 20)
    contact = models.ImageField(default = 0)
    city = models.CharField(max_length = 50)
    address = models.CharField(max_length = 150)
    pincode = models.IntegerField(default = 0)
    # state = models.CharField(max_length = 50)
    isdeleted = models.IntegerField(default = 0)

class category(models.Model):
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 200)
    isdeleted = models.IntegerField(default = 0)
    image = models.ImageField(upload_to='image')

class product(models.Model):
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 200)
    price = models.IntegerField(default = 0)
    image = models.ImageField(upload_to='image')
    discount = models.IntegerField(default = 0)
    categoryid = models.IntegerField(default = 0)
    sellerid= models.IntegerField(default = 0)
    stock = models.IntegerField(default = 0)
    isdeleted = models.IntegerField(default = 0)

class feedback(models.Model):
    
    title = models.CharField(max_length = 150)
    description = models.CharField(max_length = 200)
    productid = models.IntegerField(default = 0)
    userid = models.IntegerField(default = 0)
    sellerid = models.IntegerField(default = 0)

class cart(models.Model):
    productid = models.IntegerField(default = 0)
    userid = models.IntegerField(default = 0)
    quantity = models.IntegerField(default = 0)
    categoryid = models.IntegerField(default = 0)
    sellerid = models.IntegerField(default = 0)
# 
class wishlist(models.Model):
    productid = models.IntegerField(default = 0)
    userid = models.IntegerField(default = 0)

class orders(models.Model):
    userid = models.IntegerField(default = 0)
    orderid=models.IntegerField(default=0)
    cartid = models.IntegerField(default = 0)
    amount = models.IntegerField(default = 0)
    quantity= models.IntegerField(default=0)
    
    address = models.CharField(max_length = 200)
    payment_mode = models.IntegerField(default = 0)
    status = models.IntegerField(default = 0)
    seller = models.IntegerField(default=0)

class contact(models.Model):
    userid = models.IntegerField(default=0)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email=models.CharField(max_length=250) 
    mobile_no = models.IntegerField(max_length = 10)
    message = models.CharField(max_length = 250)