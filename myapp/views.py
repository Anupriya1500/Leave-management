from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required

from myapp.forms import  LeaveRequestForm
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
        

def grant_leaves_request(request):
    pass

def reset_passwordd(request):
    pass


def home_page(request):
    return render(request,'home.html')

def trial(request):
    return render(request, 'accounts/index.html')






from django.shortcuts import render,redirect,get_object_or_404

def index_view(request):
	return render(request,'index.html',{})

def dashboard_(request):
	
	'''
	Summary of all apps - display here with charts etc.
	eg.lEAVE - PENDING|APPROVED|RECENT|REJECTED - TOTAL THIS MONTH or NEXT MONTH
	EMPLOYEE - TOTAL | GENDER 
	CHART - AVERAGE EMPLOYEE AGES
	'''
	dataset = dict()
	user = request.user

	if not request.user.is_authenticated:
		return redirect('accounts:login')

	employees = Employee.objects.all()
	leaves = Leave.objects.all_pending_leaves()
	
	staff_leaves = Leave.objects.filter(user = user)

	
	dataset['employees'] = employees
	dataset['leaves'] = leaves
	
	dataset['staff_leaves'] = staff_leaves
	dataset['title'] = 'summary'
	

	return render(request,'dashboard/dashboard_index.html',dataset)




def dashboard_employees(request):


	return render(request,'dashboard/employee_app.html')




def dashboard_employees_create(request):
	
	return render(request,'dashboard/employee_create.html')


def employee_edit_data(request,id):

	return render(request,'dashboard/employee_create.html')






def dashboard_employee_info(request,id):
	if not request.user.is_authenticated:
		return redirect('/')
	
	employee = get_object_or_404(Employee, id = id)
	
	
	dataset = dict()
	dataset['employee'] = employee
	dataset['title'] = 'profile - {0}'.format(employee.get_full_name)
	return render(request,'dashboard/employee_detail.html',dataset)






# ---------------------LEAVE-------------------------------------------



def leave_creation(request):
	
	return render(request,'dashboard/create_leave.html')
	







def leaves_list(request):

	return render(request,'dashboard/leaves_recent.html')



def leaves_approved_list(request):

	return render(request,'dashboard/leaves_approved.html')



def leaves_view(request,id):

	return render(request,'dashboard/leave_detail_view.html')









def approve_leave(request,id):

	return redirect('dashboard:userleaveview', id = id)


def cancel_leaves_list(request):

	return render(request,'dashboard/leaves_cancel.html')



def unapprove_leave(request,id):
 
	return redirect('dashboard:leaveslist') #redirect to unapproved list




def cancel_leave(request,id):
	
	return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view


# Current section -> here
def uncancel_leave(request,id):
	
	return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view



def leave_rejected_list(request):

	
	return render(request,'dashboard/rejected_leaves_list.html')



def reject_leave(request,id):
	
	return redirect('dashboard:leavesrejected')

	# return HttpResponse(id)


def unreject_leave(request,id):
	

	return redirect('dashboard:leavesrejected')



#  staffs leaves table user only
def view_my_leave_table(request):
	
	return render(request,'dashboard/staff_leaves_table.html')
