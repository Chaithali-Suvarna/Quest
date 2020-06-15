from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

class Signup(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Post(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.BigIntegerField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    posttitle = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='pics', blank=True, null=True)
    price= models.IntegerField()



