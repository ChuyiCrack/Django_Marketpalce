from django.shortcuts import render,redirect
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login ,logout
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home(request):
    user = request.user
    products=Product.objects.all()
    if request.method=='POST':
        if 'edit' in request.POST:
            pk=request.POST.get('edit')
            return redirect('update_product',pk)
        
        elif 'delete' in request.POST:
            pk=request.POST.get('delete')
            product=Product.objects.get(id=pk)
            product.delete()
            return redirect('home')
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

@login_required
def add_products(request):
    if request.method=='POST':
        if 'submit' in request.POST:
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

def product_info(request, pk):
    product= Product.objects.get(id=pk)
    context={
        'product':product
    }
    return render(request,'inf_product.html',context)

def edit_product(request,pk):
    product=Product.objects.get(id=pk)

    if request.method=='POST':
        form=ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            form.save()
            print('gg')
            return redirect('home')
        
    else:
        form=ProductForm(instance=product)

    context={
        'form':form
    }
    return render(request,'update.html',context)

def profile(request,pk):
    if request.method=='POST':
        if 'edit' in request.POST:
            pk=request.POST.get('edit')
            return redirect('update_product',pk)
        
        elif 'delete' in request.POST:
            pk=request.POST.get('delete')
            product=Product.objects.get(id=pk)
            product.delete()
            return redirect('home')
        
    user=User.objects.get(id=pk)
    products=Product.objects.all()
    User_Products=[product for product in products if product.created_by.id == user.id]

    context={
        'User':user,
        'products':products,
        'user_products':User_Products

    }
    
    return render(request,'Profile.html',context)