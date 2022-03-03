from ast import Pass
from email.policy import default
from typing import List
from unicodedata import name
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
   BaseUserManager, AbstractBaseUser
)
import numpy as np

# Create your models here.
 
class MyUserManager(BaseUserManager):
   def create_user(self,email,name,password=None):
       """
       Creates and saves a User with the given email,and password.
       """
       if not email:
           raise ValueError('Users must have an email address')
 
       user = self.model(email=self.normalize_email(email), name=name)
       user.set_password(password)
       user.save(using=self._db)
       return user
 

#admin

   def create_superuser(self,email,name, password=None):
       """
       Creates and saves a superuser with the given email, date of
       birth and password.
       """
       user = self.create_user(email, name=name,password=password)
       user.is_admin = True
       user.is_staff = True
       user.save(using=self._db)
       return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',unique=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    # def __str__(self):
    #     return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Employee(models.Model):
    empId=models.CharField(max_length=50,primary_key=True)
    user= models.OneToOneField(User,on_delete=models.CASCADE,related_name='employee')
    line_manager=models.ForeignKey(to='self',null=True,on_delete=models.SET_NULL,default=None,blank=True,related_name='employees')
    position = models.CharField(max_length=80)
<<<<<<< HEAD
    max_leaves = models.PositiveIntegerField(default=31)
    leaves_remaining = models.PositiveIntegerField(default=31)
=======
    max_leaves = models.IntegerField(default=31)
    leaves_remaining = models.FloatField(default=31)
>>>>>>> 9d245a7e128456c6eb50a5f626fec1df7c1678c1
    is_a_line_manager = models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.user.name}"
    def get_leave_count(self):
        return self.leaves.all().count()
    def get_max_leaves(self):
        return self.max_leaves
    def get_leave_remaining(self):
        return self.leaves_remaining
        
    def my_leave_days(self):
        return self.get_max_leaves() - self.get_leave_remaining()

    
    #For Line Managers
    def get_line_manager_employee_count(self):
        if self.is_a_line_manager:
            return self.employees.all().count()
        return 0
    
    def list_of_emp_under_line_manager(self):
        if self.is_a_line_manager:
            return Employee.objects.filter(line_manager=self)
        return None

    def get_pending_requests_count(self):
        if self.is_a_line_manager:
            return Leave.objects.filter(status__in =('Pending','Cancelation Pending'),employee__line_manager=self).count()
        return 0
    
    
    def list_of_pending_request(self):
        if self.is_a_line_manager:
            return Leave.objects.filter(status__in =('Pending','Cancelation Pending'),employee__line_manager=self)
    

    def get_approved_requests_count(self):
        if self.is_a_line_manager:
            return Leave.objects.filter(status='Approved',employee__line_manager=self).count()
        return 0

    def list_of_approved_request(self):
        if self.is_a_line_manager:
            return Leave.objects.filter(status='Approved', employee__line_manager=self)
        if self.user:
            return Leave.objects.filter(status='Approved')
        return None


    def get_rejected_requests_count(self):
        if self.is_a_line_manager:
            return Leave.objects.filter(status='Rejected',employee__line_manager=self).count()
        return 0

    def list_of_rejected_request(self):
        if self.is_a_line_manager:
            return Leave.objects.filter(status='Rejected', employee__line_manager=self)


'from_date','to_date','status','reason'

class Leave(models.Model):
    id = models.IntegerField(auto_created=True,primary_key=True)
    from_date = models.DateTimeField(auto_now=False,auto_now_add=False)
    to_date = models.DateTimeField(auto_created=False,auto_now_add=False)
    employee = models.ForeignKey(to=Employee,on_delete=models.CASCADE,related_name='leaves')
    include_sat_sun = models.BooleanField(default=False)
<<<<<<< HEAD
    half_day_start = models.BooleanField('Half Day Start', default=False)
    half_day_end = models.BooleanField('Half Day End', default=False)
=======
    half_day_morning_shift = models.BooleanField(default=True)
    half_day_evening_shift = models.BooleanField(default=True)
>>>>>>> 9d245a7e128456c6eb50a5f626fec1df7c1678c1
    # is_pending ia a boolean field which will denote the state of leave obj

    is_leave_pending = models.BooleanField(null=True,blank=True, default=True)
    is_leave_approved = models.BooleanField(null=True,blank=True,default=False)
    is_leave_rejected = models.BooleanField(null=True,blank=True,default=False)
    is_leave_cancelled = models.BooleanField(null=True,blank=True,default=False)
    
    Status_Choices=[('Pending','Pending'),
    ('Approved','Approved'),
    ('Rejected','Rejected'),
    ('Cancelation Approved','Cancelation Approved'),
    ('Cancelation Rejected','Cancelation Rejected'),
    ('Cancelation Pending','Cancelation Pending'),
    ]
    status=models.CharField(choices=Status_Choices,default="Pending",max_length=50)
    reason=models.TextField(default=" ",null=True)
  


    def date_diff(self):
        if self.include_sat_sun:
            business_days_count=np.busday_count(self.from_date.strftime('%Y-%m-%d'),self.to_date.strftime('%Y-%m-%d'),weekmask='1111111')
        else:
            business_days_count=np.busday_count(self.from_date.strftime('%Y-%m-%d'),self.to_date.strftime('%Y-%m-%d'),weekmask='1111100')
        # leaves_remaining =leaves_remaining - business_days_count
        # diff = (self.to_date.day-self.from_date.day)+1
        #business_days_count=np.busday_count(self.from_date.strftime('%Y-%m-%d'),self.to_date.strftime('%Y-%m-%d'))
        return business_days_count+1

    # def half_Day_start(self):
    #     pass
    
    # def half_Day_end(self):
    #     pass

    
    
