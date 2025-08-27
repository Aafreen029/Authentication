from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
     return self.user.username



# Table Name (Model Name ) Customer

# user = models.ForeignKey(User, on_delete=models.CASCADE)
# full_name: CharField
# email = CharField
# phone = CharField
# age = int

# html page
# add customer
# delete
# Edit/Update
# table display all customers

