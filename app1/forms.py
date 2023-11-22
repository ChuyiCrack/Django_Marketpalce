from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Product

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields='__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields='__all__'
        exclude=['created_by']