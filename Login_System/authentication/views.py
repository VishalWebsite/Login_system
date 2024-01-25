
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from login_system import settings
from django.core.mail import send_mail




# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    
    if request.method=="POST":
        username=request.POST["username"]
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        pass1=request.POST["pass1"]
        pass2=request.POST["pass2"]
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist, try with another username!")
            return redirect("home")
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already exist!")
            return redirect("home")
        
        if len(username)>10:
            messages.error(request, "Username should be under 10 characters!")
            print("asdfgh")
            return redirect("home")
            
        if pass1!= pass2:
            messages.error(request, "Password did not match!")
            return redirect("home")
            
        if not username.isalnum():  
            messages.error("Username must be alphanumeric!")
            return redirect("home")
        
        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        # myuser.phone=phone
        myuser.save()
        
        messages.success(request, "You are account has been succesfully created!")
        
        # Welcome Email
        subject = "Welcome to Login_system!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Login_system!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nVishal Sangale"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        return redirect("signin")
    return render(request, "authentication/signup.html")

def signin(request):
    
    if request.method=="POST":
        username=request.POST["username"]
        pass1=request.POST["pass1"]
        
        user=authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname=user.first_name
            return render(request, "authentication/index.html", {"fname":fname})
        else:
            messages.error(request,"You enter invalid credentials!")
            return redirect("home")
            
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"You are succesfully logged out!")
    return redirect("home")