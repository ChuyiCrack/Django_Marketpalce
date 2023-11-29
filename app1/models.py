from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Type(models.Model):
    Type=models.CharField(max_length=25)

    def __str__(self):
        return self.Type
    

class Product(models.Model):
    Name=models.CharField(max_length=50,blank=False)
    Description=models.TextField(max_length=250,blank=True)
    type_product=models.ForeignKey(Type,on_delete=models.SET_NULL, null=True, blank=True)
    Price=models.IntegerField(default=0)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image=models.ImageField(upload_to='./images',blank=False, null=True)


    def save(self, *args, **kwargs):
        # If the created_by field is not set and a user is logged in, set the current user as the creator
        if not self.created_by and hasattr(self, 'request') and self.request.user.is_authenticated:
            self.created_by = self.request.user

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.Name
    
class Message(models.Model):
    transmitter=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='transmitter_messages')
    product_selling=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    Receiver=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_messages')
    Title=models.CharField(max_length=50,blank=False)
    message=models.TextField(max_length=50,blank=False)
    creation=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Title
    

class chat(models.Model):
    Principal_Chat=models.ForeignKey(Message,on_delete=models.SET_NULL, null=True, blank=False)
    Creator=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message_chat=models.CharField(max_length=150)
    creation_msg=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message_chat


    