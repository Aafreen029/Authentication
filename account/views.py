from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages 
from .helpers import send_forget_password_mail
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import Customer
import uuid

# Create your views here.
#@login_required(login_url='/login')
def index(request):
    if request.user.is_authenticated:
        print(request.user)
        customers=Customer.objects.filter(user=request.user)
        return render(request,'index.html',{"customers":customers})
    return render(request,'index.html')

def loginViews(request):
    redirect_url = request.GET.get('next')
    print(redirect_url)
    if request.method == 'POST':
        email1=request.POST.get('email1')
        password=request.POST.get('pass1')
        #print(email1)
        #print(pass1)
        user_obj = User.objects.get(email=email1)
        username = user_obj.username
    
        user=authenticate(request,username=username,password=password)
    
        if user is not None:
            login(request,user)
            messages.success(request, 'Successfully logged in!')
            if redirect_url:
                print("Redirect URL")
                return redirect(redirect_url)
            
            return redirect('accounts')
        else: 
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')
#@login_required(login_url='/login')
  
                                            
def logoutViews(request):
    logout(request)
    messages.error(request, "Successfully logged out")
    return redirect('accounts')
    
def signup(request):
   if request.method == 'POST':
       uname=request.POST['uname']
       fname=request.POST['fname']
       lname=request.POST['lname']
       email=request.POST['email']
       pass1=request.POST['pass1']
       pass2=request.POST['pass2']

       if pass1 != pass2:
           messages.error(request,"password do not match")
           return redirect('/signup/')
       
       if User.objects.filter(email=email).exists():
           messages.error(request," Email already Registerd")
           return redirect('/signup/')
       
       if not uname.isalnum():
           messages.error(request,"Username must contain Numbers and Alphabet")
           return redirect('/signup/')
       
       email_username=email.split('@')[0]

       if uname != email_username:
           messages.error(request,"Username must match your email address")
           return redirect('/signup/')
           

       myuser=User.objects.create_user(uname,email,pass1)
       myuser.first_name=fname
       myuser.last_name=lname
       myuser.save()
       Profile.objects.create(user=myuser)
       messages.success(request,"Account created successfully")
       return redirect('/signup/')
      
   else:
       return render(request,'signup.html')
   
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username=request.POST.get('username')
            print(username,"hellooo")

            if not User.objects.filter(username=username).first():
                messages.success(request,'Not user found with this username')
                return redirect('/forget-password/')
            
            user_obj=User.objects.get(username=username)
            print(user_obj,"54545454")
            token= str(uuid.uuid4())
            profile_obj=Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token= token
            profile_obj.save()
            send_forget_password_mail(user_obj.email,token)
            messages.success(request,'An email is sent')
            return redirect('/forget-password/')

    except Exception as e:
        print(e)
    return render(request,'forget-password.html')
    
def ChangePassword(request,token):
        context={}
        try:
            profile_obj=Profile.objects.filter(forget_password_token=token).first()
            print(profile_obj.user)
           
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('reconfirm_password')

            
                if  new_password != confirm_password:
                 messages.success(request, 'both should  be equal.')
                 return redirect(f'/change-password/{token}/')
                         
            
                user_obj = User.objects.get(id = profile_obj.user.id)
                user_obj.set_password(new_password)
                user_obj.save()
                messages.success(request, "Password updated successfully!")
                return redirect('/')
            return render(request,'change-password.html',context)
            
              
        except Exception as e:
         print(e)
         return render(request,'change-password.html',context)

#@login_required(login_url='/login')
def getCustomer(request):
    return render(request, "list-customer.html")

def add_customer(request):
    if request.method == "POST":
        full_name=request.POST.get("full_name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        age=request.POST.get("age")

        if request.user.is_authenticated:
            user=request.user
        else:
            user=None

        Customer.objects.create(user=user,full_name=full_name,email=email,phone=phone,age=age)
       
        messages.success(request,"New Customer added successfully")
        return redirect('accounts')
    return render(request,'add-customer.html')

def edit_customer(request,customer_id):
    customer= get_object_or_404(Customer,id=customer_id)
    print(customer.full_name)
    if request.method == "POST":
        full_name=request.POST.get("full_name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        age=request.POST.get("age")
        print(full_name,age,email,phone)

        #if not full_name or not email:
            #messages.error(request,"Name and Email are required fields")
            #return render(request,'edit.html',{"customer":customer})
        try:
            customer.full_name=full_name
            customer.email=email
            customer.phone=phone
            customer.age=age

            customer.save()
            messages.success(request,"Update successfully")
            return redirect('accounts')
        
        except Exception as e:
            messages.error(request,"Error updating customer",str(e))
        
    context={'customer':customer,'user':request.user}

    return render(request,'edit.html',context)

def delete_customer(request,customer_id):
    customer= get_object_or_404(Customer,id=customer_id)

    customer.delete()
    messages.success(request,"deleted successfully")

    return redirect('/')




        
    

    
