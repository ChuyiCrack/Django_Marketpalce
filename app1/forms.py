from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Product,Message,chat

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields='__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields='__all__'
        exclude=['created_by']

class MessageForm(forms.ModelForm):
    class Meta:
        model= Message
        fields='__all__'
        exclude=['transmitter','Receiver','creation','product_selling']

class ChatForm(forms.ModelForm):
    class Meta:
        model=chat
        fields='__all__'
        exclude=['creation_msg','Principal_Chat','Creator']
