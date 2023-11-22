from django.shortcuts import render,redirect
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login ,logout
from .forms import ProductForm
from .models import Product


def home(request):
    user = request.user
    products=Product.objects.all()
    context={
        'user':user,
        'products':products
    }
    return render(request,'home.html',context)


def login_user(request):
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form=AuthenticationForm()

    context={
        'form':form
    }
    
    return render(request,'login.html',context)


def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    
    else:
        form=UserCreationForm()

    context={
        'form':form
    }
    
    return render(request,'register.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')

def add_products(request):
    if request.method=='POST':
        pk=request.POST.get('submit')
        if not pk:
            form= ProductForm(request.POST,request.FILES)

        else:
            product=Product.objects.get(id=pk)
            form= ProductForm(request.POST,instance=Product)
        
        if form.is_valid():
            product= form.save(commit=False)
            product.request = request
            product.save()
            print(True)
            return redirect('home')

        else:
            print('Is not valid')
            print(form.errors)
    else:
        form=ProductForm()


    context={
        'form':form
    }
    
    return render(request,'Products.html',context)