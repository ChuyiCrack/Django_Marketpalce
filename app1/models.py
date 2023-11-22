from django.db import models
from django.contrib.auth.models import User

class Type(models.Model):
    Type=models.CharField(max_length=25)

    def __str__(self):
        return self.Type
    

class Product(models.Model):
    Name=models.CharField(max_length=50,blank=False)
    Description=models.CharField(max_length=250,blank=True)
    type_product=models.ForeignKey(Type,on_delete=models.SET_NULL, null=True, blank=True)
    Price=models.IntegerField(default=0)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image=models.ImageField(upload_to='./images',blank=False, null=True)

    def __str__(self):
        return self.Name
