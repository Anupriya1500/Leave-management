from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
def signup(request):
    if not request.user.is_authenticated:
        return HttpResponse('<h1>SignUp Page</h1>')
def employeelogin(request):
    if request.user.is_authenticated:
        return HttpResponse('<h1> Current Session User is already Authenticated <a href="/Dashboard"> Dashboard </a></h1>') 
        
    else:
        if request.method=="POST":
            form=AuthenticationForm(request,data=request.POST)
            if form.is_valid():
                email=form.cleaned_data.get('username')
                password=form.cleaned_data.get('password')
                varuser=authenticate(username=email,password=password)
                if varuser is not None:
                    login(request,varuser)
                   # messages.info(request,f"You are logged in as {email}")
                    print("user authenticated Sucessfully ")
                    return render(request,'dashboard.html',{'user':varuser})
                else:
                     print(f'Not Authenticated {email}{password}')
                    #messages.error(request,f"Invalid")
            else:
                 print('Invalid')
               
               # messages.error(request,"Invalid email")

        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})
def userlogout(request):    
    logout(request)
    messages.info(request,"You have Successfully logged out")
    return redirect("/login")

def dashboard(request):
    return render(request,'dashboard.html')

def apply_for_leave(request):
    pass

def grant_leaves_request(request):
    pass

def reset_passwordd(request):
    pass