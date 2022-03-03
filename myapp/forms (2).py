from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Employee, Leave, User
import numpy as np 
import holidays
from django.contrib.admin.widgets import AdminDateWidget
from cryptography.fernet import Fernet
#case1` When Both the date are same `-check if the from day is holiday or not if yes return 0 else 1  and if half day then 0.5
#case 2 when they are not
def date_diff(leave):
        fraction_day_count = 1
        if (leave.from_date==leave.to_date):
            if leave.half_day_morning_shift or leave.half_day_evening_shift:
                fraction_day_count = 0.5
            if not np.is_busday(leave.from_date.strftime('%Y-%m-%d')) and not leave.include_sat_sun:
                fraction_day_count = 0

        if leave.include_sat_sun:
            business_days_count=np.busday_count(leave.from_date.strftime('%Y-%m-%d'),leave.to_date.strftime('%Y-%m-%d'),weekmask='1111111')+fraction_day_count 
        else:
            business_days_count=np.busday_count(leave.from_date.strftime('%Y-%m-%d'),leave.to_date.strftime('%Y-%m-%d'),weekmask='1111100')+fraction_day_count
        
        return business_days_count

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

 
class UserCreationForm(forms.ModelForm):
   password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
   password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
 
   class Meta:
       model = User
       fields = ('email',)
 
   def clean_password2(self):
       # Check that the two password entries match
       password1 = self.cleaned_data.get("password1")
       password2 = self.cleaned_data.get("password2")
       if password1 and password2 and password1 != password2:
           raise ValidationError("Passwords don't match")
       return password2
 
   def save(self, commit=True):
       # Save the provided password in hashed format
       user = super().save(commit=False)
       
       user.set_password(self.cleaned_data["password1"])
       
       if commit:
           user.save()
       return user

class SignUp(forms.ModelForm):
    pass

class LeaveRequestForm(forms.ModelForm):
    #from_date=forms.DateField(widget = forms.SelectDateWidget())
    #to_date=forms.DateField(widget = forms.SelectDateWidget())

    # from_date=forms.DateField(input_formats=['%d/%m/%Y'],
    #     widget=forms.DateTimeInput(attrs={
    #         'class': 'form-control datetimepicker-input',
    #         'data-target': '#datetimepicker1'
    #     }))
    # to_date=forms.DateField(widget = AdminDateWidget())

    class Meta:
        model=Leave
        exclude=['id','employee','is_leave_approved','status','is_leave_rejected','is_leave_cancelled','is_leave_pending']
    def clean(self):
        cleaned_data = super().clean()
        from_date=cleaned_data.get("from_date")
        to_date=cleaned_data.get("to_date")
        print(from_date)
        print(to_date)
        if(from_date>to_date):
            raise ValidationError(
                "From Date can Not be After To Date"
            )
    @transaction.atomic
    def save(self,current_user):
        leave_request=super().save(commit=False)
        
        leave_request.is_leave_pending=True
        leave_request.is_leave_rejected=False
        leave_request.is_leave_cancelled=False
        leave_request.is_leave_approved=True
        leave_request.employee=Employee.objects.get(user=current_user)
        leave_request.save()
        return leave_request

class GrantLeaveRequestForm(forms.ModelForm):
    employee_id = forms.CharField(max_length=50,disabled=True,required=False)
    max_leaves = forms.FloatField(disabled=True,required=False)
    leaves_remaining = forms.FloatField(disabled=True,required=False)
    from_date = forms.DateTimeField(disabled=True,required=False)
    to_date = forms.DateTimeField(disabled=True,required=False)
    reason = forms.CharField(disabled=True,required=False)
    Status_Choices=[
    ('Approved','Approved'),
    ('Rejected','Rejected'),
    ]
    status=forms.ChoiceField(choices=Status_Choices)
    def __init__(self,*args, **kwargs):
            #self.default_text = kwargs.pop('text')

        super(GrantLeaveRequestForm, self).__init__(*args, **kwargs)
        
        leave=self.instance
        employee=leave.employee
        self.fields['employee_id'].initial=employee.empId
        self.fields['max_leaves'].initial=employee.max_leaves
        self.fields['leaves_remaining'].initial=employee.leaves_remaining
#Pending     
        if leave.is_leave_pending and leave.is_leave_approved and not leave.is_leave_rejected and not leave.is_leave_cancelled:
            Status_Choices=[('Approved','Approved'),
    ('Rejected','Rejected'),
    ]
#Updating
        elif not leave.is_leave_pending and (leave.is_leave_approved or  leave.is_leave_rejected) and not leave.is_leave_cancelled:
            Status_Choices=[('Approved','Approved'),
    ('Rejected','Rejected'),
    ]
#Cancellation
    #Pending
        elif leave.is_leave_pending and leave.is_leave_approved and not leave.is_leave_rejected and leave.is_leave_cancelled:
            Status_Choices=[('Cancelation Approved','Cancelation Approved'),
    ('Cancelation Rejected','Cancelation Rejected'),
    
    ]
    #Updating
        elif not leave.is_leave_pending and (leave.is_leave_approved or  leave.is_leave_rejected) and leave.is_leave_cancelled:
            Status_Choices=[('Cancelation Approved','Cancelation Approved'),
    ('Cancelation Rejected','Cancelation Rejected'),
    
    ]
        
        else:
            Status_Choices=[('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        ('Cancelation Approved','Cancelation Approved'),
        ('Cancelation Rejected','Cancelation Rejected'),
        ('Cancelation Pending','Cancelation Pending'),
        ]
        self.fields['status'].choices = Status_Choices
    class Meta:
        model=Leave
        fields=['from_date','to_date','status','reason']
    def save(self,leave_request):
        leave=self.instance
        employee=leave.employee
        old_status=leave.status
        new_status=self.cleaned_data['status']
# Pending Leave Request--------------------------------
        # 1 1 0 0
        if leave.is_leave_pending and leave.is_leave_approved and not leave.is_leave_rejected and not leave.is_leave_cancelled:
            #This is the Case when an Employee Creates a Leave Request 
            if new_status=='Approved':
                # reduce the No of leave remaining for this employee
                business_days_count=date_diff(leave)
                employee.leaves_remaining =employee.leaves_remaining - business_days_count
                
                leave.is_leave_pending=False
                leave.is_leave_approved=True
                leave.is_leave_rejected=False
                leave.is_leave_cancelled=False
                leave.status='Approved'
                employee.save()
                leave.save()
            #  0 1 0 0  
                        
            if new_status=='Rejected':
                #No Need to Reduce the leave Remaining since Request is rejected
                leave.is_leave_pending=False
                leave.is_leave_approved=False
                leave.is_leave_rejected=True
                leave.is_leave_cancelled=False
                leave.status='Rejected'
                employee.save()
                leave.save()
            # 0 0 1 0
# Updating Approved or Rejected-------------------------
        # 0 0 1 0    
        elif not leave.is_leave_pending and not leave.is_leave_approved and leave.is_leave_rejected and not leave.is_leave_cancelled:
            """ When Employee Leave Request Was already Rejected and Now Updating it """
            if new_status=='Approved':
                business_days_count=date_diff(leave)
                employee.leaves_remaining =employee.leaves_remaining - business_days_count
                
                leave.is_leave_pending=False
                leave.is_leave_approved=True
                leave.is_leave_rejected=False
                leave.is_leave_cancelled=False
                leave.status='Approved'
                employee.save()
                leave.save()
            # 0 1 0 0
            if new_status=='Rejected':
                pass
        # 0 1 0 0
        elif not leave.is_leave_pending and leave.is_leave_approved and not leave.is_leave_rejected and not leave.is_leave_cancelled:
            """ When Employee Leave Request Was already Approved and Now Updating it """
            if new_status=='Approved':
                pass
            if new_status=='Rejected':
                business_days_count=date_diff(leave)
                employee.leaves_remaining =employee.leaves_remaining + business_days_count
                
                leave.is_leave_pending=False
                leave.is_leave_approved=False
                leave.is_leave_rejected=True
                leave.is_leave_cancelled=False
                leave.status='Rejected'
                employee.save()
                leave.save()
            # 0 0 1 0
# Cancellation--------------------------
    # Pending
        # 1 1 0 1
        elif leave.is_leave_pending and leave.is_leave_approved and not leave.is_leave_rejected and leave.is_leave_cancelled:
            #This is the Case when an already Approved Request is to be Cancelled by the Employee
            if new_status=='Cancelation Approved':
                # incre the No of leave remaining for this employee
                business_days_count=date_diff(leave)
                employee.leaves_remaining =employee.leaves_remaining + business_days_count
                
                leave.is_leave_pending=False
                leave.is_leave_approved=True
                leave.is_leave_rejected=False
                leave.is_leave_cancelled=True
                leave.status='Cancelation Approved'
                employee.save()
                leave.save()
            # 0 1 0 1
            if new_status=='Cancelation Rejected':
                #No Need to incre the leave Remaining since Cancelation Request is rejected
                leave.is_leave_pending=False
                leave.is_leave_approved=True
                leave.is_leave_rejected=True
                leave.is_leave_cancelled=True
                leave.status='Cancelation Rejected'
                employee.save()
                leave.save()
            # 0 1 1 1
            
            if new_status=='Cancelation Pending':
                #Default Status When Employee's Cancelation is waiting to be responded by aproval or rejection
                pass            
        
    # Updating  
        # 0 1 0 1
        elif not leave.is_leave_pending and leave.is_leave_approved and not leave.is_leave_rejected and leave.is_leave_cancelled:
            """ When Employee's Already Approved Leave Request is requested to be Cancelled and that was also approved and now Updating it"""
            if new_status=='Cancelation Approved':
                #No Need to Reduce the leave Remaining since Cancelation Request is was already approved
                
                pass
            if new_status=='Cancelation Rejected':
                # reduc the No of leave remaining for this employee
                business_days_count=date_diff(leave)
                employee.leaves_remaining =employee.leaves_remaining - business_days_count
                
                leave.is_leave_pending=False
                leave.is_leave_approved=True
                leave.is_leave_rejected=True
                leave.is_leave_cancelled=True
                leave.status='Cancelation Rejected'
                employee.save()
                leave.save()
            # 0 1 1 1
            
        # 0 1 1 1
        elif not leave.is_leave_pending and leave.is_leave_approved and not leave.is_leave_rejected and leave.is_leave_cancelled:
            """ When Employee Leave Request Was already Approved and Its Cancelation request is Rejected Now Updating it """
            if new_status=='Cancelation Approved':
                # incre the No of leave remaining for this employee
                business_days_count=date_diff(leave)
                employee.leaves_remaining =employee.leaves_remaining + business_days_count
                
                leave.is_leave_pending=False
                leave.is_leave_approved=True
                leave.is_leave_rejected=False
                leave.is_leave_cancelled=True
                leave.status='Cancelation Approved'
                employee.save()
                leave.save()
            # 0 1 0 1
            if new_status=='Cancelation Rejected':
                #No Need to Reduce the leave Remaining since Cancelation Request is rejected
                pass
            
    
        else:
            pass
        return leave

class GrantLeaveRequestModelForm(forms.ModelForm):
    employee_id = forms.CharField(max_length=50,disabled=True)
    max_leaves = forms.FloatField(disabled=True)
    leaves_remaining = forms.FloatField(disabled=True)
    class Meta:
        model=Leave
        exclude=["employee"]


# ---------------------------------------Cancellation request by user--------------------------------------- 

class CancelLeaveRequestForm(forms.Form):
    from_date = forms.DateField(disabled=True,required=False)
    to_date = forms.DateField(disabled=True,required=False)
    cancellation_reason = forms.CharField(required=True)

    def save(self,leave_request):
        if leave_request.is_leave_approved:
            leave_request.is_leave_cancelled = True
            leave_request.is_leave_pending = True
            leave_request.is_leave_rejected=False
            temp = leave_request.reason
            temp += self.cleaned_data['cancellation_reason']
            leave_request.reason =  temp

            leave_request.status='Cancelation Pending'
            leave_request.save()

        return leave_request
        

def get_leave_count(from_date, to_date):
    business_days_count=np.busday_count(from_date.strftime('%Y-%m-%d'),to_date.strftime('%Y-%m-%d'),holidays=[])
        




