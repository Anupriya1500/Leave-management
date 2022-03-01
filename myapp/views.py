from urllib import request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from myapp.forms import  CancelLeaveRequestForm, GrantLeaveRequestForm, GrantLeaveRequestModelForm, LeaveRequestForm
from .models import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from cryptography.fernet import Fernet

def encryptPassword(password):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encpassword = fernet.encrypt(password.encode())
    return encpassword

def decryptPassword(password):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    decpassword = fernet.decrypt(password.encode())
    return decpassword

# Create your views here.
def signup(request):
    if not request.user.is_authenticated:
        return HttpResponse('<h1>SignUp Page</h1>')

def home_page(request):
    return render(request, 'index.html')
    
def employeelogin(request):
    if request.user.is_authenticated:
        return HttpResponse('<h1> Current Session User is already Authenticated <a href="/Dashboard"> Dashboard </a></h1>') 
    else:
        if request.method=="POST":
            form=AuthenticationForm(request,data=request.POST)
            if form.is_valid():
                email=form.cleaned_data.get('username')
                password= form.cleaned_data.get('password')
                print(password)
                varuser=authenticate(username=email,password=password)
                print(password)
                if varuser is not None:
                    login(request,varuser)
                   # messages.info(request,f"You are logged in as {email}")
                    print("user authenticated Sucessfully ")
                    return redirect("/Dashboard")
                    return render(request,'dashboard.html',{'user':varuser})

                else:
                    messages.error(request,'Account is invalid', extra_tags = 'alert alert-error alert-dismissible show')
                    return redirect('login')
            else:
                messages.error(request,"Invalid username or password",extra_tags = 'alert alert-error alert-dismissible show')
            

        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})

def userlogout(request):    
    logout(request)
    messages.info(request,"You have Successfully logged out",extra_tags = 'alert alert-error alert-dismissible show')
    return redirect("/login/")

def dashboard(request):
    return render(request,'dashboard.html')

def create_leave_request(request):
    if request.user.is_authenticated:
        leave_request_form=LeaveRequestForm()

        if request.user.employee.line_manager is None:
            messages.success(request,"Please contact your admin to assign you a line manager")

        else:   
            if request.method=="POST":
                leave_request_form=LeaveRequestForm(data=request.POST)
                if leave_request_form.is_valid():
                    leave_request=leave_request_form.save(current_user=request.user)

                    messages.success(request,"Leave Requested Created Successfully")
                    leave_request_form=LeaveRequestForm()
        return render(request,'leave_request.html',{"form":leave_request_form,"submit_button_name": 'Request Leave'})
    return render(request, 'leave_request.html')

def update_leave_request(request,leave_id):
    if request.user.is_authenticated:
        leave = Leave.objects.get(id=leave_id)
        if leave.employee.user==request.user and leave.status=='Pending':
            leave_request_form=LeaveRequestForm(instance=leave)
            if request.method=='POST':
                leave_request_form=LeaveRequestForm(data=request.POST,instance=leave)
                if leave_request_form.is_valid():
                    leave_request=leave_request_form.save(current_user=request.user)
                    messages.success(request,"Leave Request form updated Successfully")
                    leave_request_form=LeaveRequestForm(instance=leave_request)
            
                    return render(request,'leave_request.html',{"form":leave_request_form,"submit_button_name": 'Update Leave'})

            elif request.method=="GET":
                return render(request,'leave_request.html',{"form":leave_request_form, "submit_button_name": 'Update Leave'})
        
        return HttpResponse('<h1>Permission Denied</h1>')
    return HttpResponse('<h1>User Not Authenticated , Please Login </h1>')

def cancel_leave_request(request,leave_id):
    if request.user.is_authenticated:
        leave=Leave.objects.get(id=leave_id)
        if leave.employee.user==request.user and leave.status=='Approved':
            initial_data={
                'from_date':leave.from_date,
                'to_date': leave.to_date,
            }
            cancel_leave_request_form = CancelLeaveRequestForm(initial=initial_data)
            if request.method=='POST':
                cancel_leave_request_form=CancelLeaveRequestForm(data=request.POST)
                if cancel_leave_request_form.is_valid():
                    leave_request = cancel_leave_request_form.save(leave_request=leave)
                    
                    messages.success(request,"Cancel Leave Request form submitted Successfully")
                
                return redirect ("/Dashboard")
            
            return render(request,'leave_request.html',{"form":cancel_leave_request_form,
            "submit_button_name": 'Cancel Leave'})

def grant_leaves_request(request,leave_id):
    if request.user.is_authenticated :
        employee=Employee.objects.get(user=request.user)
        try:
            leave_request=Leave.objects.get(id=leave_id)
            employee_who_asked_for_leave=leave_request.employee

        except Leave.DoesNotExist:
            leave_request=None
        if employee is not None and employee.is_a_line_manager and leave_request is not None and employee_who_asked_for_leave.line_manager==employee:
            initial_data={
                'employee_id':employee_who_asked_for_leave.empId,
                'max_leaves':employee_who_asked_for_leave.max_leaves,
                'leaves_remaining':employee_who_asked_for_leave.leaves_remaining,
                'from_date':leave_request.from_date,
                'to_date':leave_request.to_date,
                'reason':leave_request.reason,
                'status' : leave_request.status
                }
            grant_leaves_request_form=GrantLeaveRequestForm(
                #initial=initial_data
                instance=leave_request
                )
            if request.method=="POST":
                grant_leaves_request_form=GrantLeaveRequestForm(data=request.POST,instance=leave_request)
                if grant_leaves_request_form.is_valid():
                    leave_request=grant_leaves_request_form.save(leave_request=leave_request)
                    initial_data={
                'employee_id':employee_who_asked_for_leave.empId,
                'max_leaves':employee_who_asked_for_leave.max_leaves,
                'leaves_remaining':employee_who_asked_for_leave.leaves_remaining,
                'from_date':leave_request.from_date,
                'to_date':leave_request.to_date,
                'reason':leave_request.reason,
                'status' : leave_request.status
                }
                grant_leaves_request_form=GrantLeaveRequestForm(instance=leave_request)

                messages.info(request,f"Leave Request {leave_request.status} ")
                return render(request,'grant_leaves.html',{"form":grant_leaves_request_form})
            else:
                return render(request,'grant_leaves.html',{"form":grant_leaves_request_form})
                
        return HttpResponse('<h1>Permission Denied</h1>')
    return HttpResponse('<h1>User Not Authenticated , Please Login </h1>')
    
def list_leave_requests(request):
    if request.user.is_authenticated :
        employee=Employee.objects.get(user=request.user)
        if employee is not None and employee.is_a_line_manager and request.method=="GET":
            try:
                list_leave_requests=Leave.objects.filter(employee__line_manager=employee)
                print(list_leave_requests)
            except Leave.DoesNotExist:
                list_leave_requests=None
                
            return render(request,'list_leave_requests.html',{"list_leave_requests":list_leave_requests})
        if employee is not None and not employee.is_a_line_manager and request.method=="GET":
            try:
                list_leave_requests=Leave.objects.filter(employee__user=request.user)
                print(list_leave_requests)
            except Leave.DoesNotExist:
                list_leave_requests=None
                
            return render(request,'list_leave_requests.html',{"list_leave_requests":list_leave_requests})
                
        return HttpResponse('<h1>Permission Denied</h1>')
    return HttpResponse('<h1>User Not Authenticated , Please Login </h1>')

def line_manager_leave_requests(request):
    if request.user.is_authenticated :
        employee=Employee.objects.get(user=request.user)
        if employee is not None and employee.is_a_line_manager:
            line_managers_leave_requests=Leave.objects.filter(employee=employee)
            return render(request,'line_manager_leave_requests.html',{"line_managers_leave_requests":line_managers_leave_requests})
        return HttpResponse('<H1>User Is Not Associated with a Employee</H1>')
    return HttpResponse('<H1>User Is Not Authorised</H1>')


#todo-Check Online
def reset_passwordd(request):
    pass

def list_line_managers_employees(request):
    if request.user.is_authenticated:
        employee = Employee.objects.get(user=request.user)
        if employee is not None and employee.is_a_line_manager:
            return render(request, 'list_emp_under_line_manager.html',{"list_emp_under_line_manager":employee.list_of_emp_under_line_manager()})

def list_pending_requests(request):
    if request.user.is_authenticated:
        employee = Employee.objects.get(user=request.user)
        if employee is not None and employee.is_a_line_manager:
            return render(request,'list_leave_requests.html', {"list_leave_requests":employee.list_of_pending_request()})

def list_approved_requests(request):
    if request.user.is_authenticated:
        employee = Employee.objects.get(user=request.user)
        if employee is not None:
            return render(request, 'list_leave_requests.html', {"list_leave_requests":employee.list_of_approved_request()})

def list_rejected_requests(request):
    if request.user.is_authenticated:
        employee = Employee.objects.get(user=request.user)
        if employee is not None and employee.is_a_line_manager:
            return render(request, 'list_leave_requests.html', {"list_leave_requests":employee.list_of_rejected_request()})




def line_manager_leave_count(request):
    return render(request,'line_manager_leave_count.html')

    
# View leave 

def leaves_view(request,id):
	if not (request.user.is_authenticated):
		return redirect('/')

	leave = get_object_or_404(Leave, id = id)
	#print(leave.user)
	employee = leave.employee
	print(employee)
	return render(request,'dashboard/leave_detail_view.html',{'leave':leave,'employee':employee,'title':'{0}-{1} leave'.format(request.user.name,leave.status)})





