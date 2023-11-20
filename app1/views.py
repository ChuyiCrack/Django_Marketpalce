from django.shortcuts import render,redirect
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login ,logout


def home(request):
    user = request.user
    context={
        'user':user
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