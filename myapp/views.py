from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required

from myapp.forms import  GrantLeaveRequestForm, GrantLeaveRequestModelForm, LeaveRequestForm
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

def create_leave_request(request):
    if request.user.is_authenticated:
        leave_request_form=LeaveRequestForm()
            
        if request.method=="POST":
            leave_request_form=LeaveRequestForm(data=request.POST)
            if leave_request_form.is_valid():
                leave_request=leave_request_form.save(current_user=request.user)
                #leave_request_form=LeaveRequestForm(instance=leave_request)
        return render(request,'leave_request.html',{"form":leave_request_form})
        

def grant_leaves_request(request,leave_id):
    if request.user.is_authenticated :
        employee=Employee.objects.get(user=request.user)
        try:
            leave_request=Leave.objects.get(id=leave_id)
        except Leave.DoesNotExist:
            leave_request=None
        if employee is not None and employee.is_a_line_manager and leave_request is not None and leave_request.employee.line_manager==employee:
            grant_leaves_request_form=GrantLeaveRequestModelForm(instance=leave_request)
            if request.method=="POST":
                grant_leaves_request_form=GrantLeaveRequestModelForm(data=request.POST,instance=leave_request)
                if grant_leaves_request_form.is_valid():
                    leave_request=grant_leaves_request_form.save()
                    grant_leaves_request_form=GrantLeaveRequestModelForm(instance=leave_request)
                
                return render(request,'grant_leaves.html',{"form":grant_leaves_request_form})
            else:
                return render(request,'grant_leaves.html',{"form":grant_leaves_request_form})
                
        return HttpResponse('<h1>Permission Denied</h1>')
    return HttpResponse('<h1>User Not Authenticated , Please Login </h1>')
    
def list_leave_requests(request):
    pass
def reset_passwordd(request):
    pass