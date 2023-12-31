from django.shortcuts import render,redirect
from .forms import UserCreationForm,MessageForm,ProductForm,ChatForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login ,logout
from .models import Product,Message,chat
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

#Tratar de colocar un apartado de fecha de envio de mensaje
def home(request):
    user = request.user
    products=Product.objects.all()
    if request.method=='POST':
        if 'edit' in request.POST:
            pk=request.POST.get('edit')
            return redirect('update_product',pk)
            print('Search')
            search_query = request.POST['search_bar']
            print(search_query)
        elif 'delete' in request.POST:
            pk=request.POST.get('delete')
            product=Product.objects.get(id=pk)
            product.delete()
            return redirect('home')
        
        elif 'search' in request.POST:
            search_query = request.GET['search_bar']
            print(search_query)
        

    context={
        'user':user,
        'products':products,
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
    messages=Message.objects.all()
    counter=0

    for msg in messages:
        if request.user in (msg.Receiver,msg.transmitter):
            if msg.product_selling.id == product.id:
                counter+=1
                message=msg.id
                break

        else:
            message=None


    context={
        'product':product,
        'message':message,
        'counter':counter
    }
    return render(request,'inf_product.html',context)

def edit_product(request,pk):
    product=Product.objects.get(id=pk)

    if request.method=='POST':
        form=ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            form.save()
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
    messages=Message.objects.filter(Q(transmitter=request.user  ) | Q(Receiver=request.user  ))
    ordered_messages=messages.order_by('-creation')
    latest_chat=chat.objects.filter(Q(Principal_Chat__transmitter=request.user  ) | Q(Principal_Chat__Receiver=request.user  ) ).order_by('-creation_msg').first()
    user_message=[]
    print(latest_chat)
    if latest_chat:
        user_message.append(latest_chat.Principal_Chat)
        for x in ordered_messages:
            if x !=latest_chat.Principal_Chat:
                user_message.append(x)



    User_Products=[product for product in products if product.created_by.id == user.id]

    context={
        'User':user,
        'products':products,
        'user_products':User_Products,
        'message':user_message


    }
    
    return render(request,'Profile.html',context)

def send_message(request,pk):
    product=Product.objects.get(id=pk)
    Destination_User=product.created_by
    user=request.user
    if request.method=='POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            new_message=form.save(commit=False)
            new_message.Receiver = Destination_User
            new_message.transmitter= user
            new_message.product_selling= product
            new_message.save()
            return redirect('home')
    else:
        form=MessageForm()

    context={
        'Destination_User':Destination_User,
        'user':user,
        'form':form,
        
    }
    return render(request,'message.html',context)


def Chat_View(request,pk):
    message=Message.objects.get(id=pk)
    form=ChatForm()
    if request.method == 'POST':
        form=ChatForm(request.POST)
        
        if form.is_valid():
            print(True)
            new_form=form.save(commit=False)
            new_form.Principal_Chat= message
            new_form.Creator= request.user
            new_form.save()
            return redirect('chat',message.id)

        else:
            print(False)
    
    User=request.user
    Chats=chat.objects.all()
    Chat_Pr=[cht for cht in Chats if cht.Principal_Chat == message]
    print(Chat_Pr)
    context={
        'Message':message,
        'form':form,
        'chat':Chat_Pr,
        'user':User
    }
    return render(request,'chat.html',context)

def search_product(request):
    if request.method == 'POST':
        search_query = request.POST['search_bar']
        if search_query=="":
            return redirect('home')
        
        else:
            products=Product.objects.filter(Name__contains=search_query)
        
        print(search_query)

        context={
            'search':search_query,
            'products':products,
        }
    return render(request,'search.html',context)