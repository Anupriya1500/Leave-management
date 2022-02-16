from django.db import models

from datetime import datetime

from django.contrib.auth.models import (
   BaseUserManager, AbstractBaseUser
)
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
       user.save(using=self._db)
       return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',unique=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.now())
    name = models.CharField(max_length=50)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

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
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    line_manager=models.ForeignKey(to='self',null=True,on_delete=models.SET_NULL,default=None,blank=True)
    position = models.CharField(max_length=80)
    max_leaves = models.IntegerField(default=31)
    leaves_remaining = models.IntegerField(default=31)
    is_a_line_manager = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if self.line_manager is None:
    #         User.objects.get
    #         ceo=Employee(empId=1,)
    #     super().save(*args, **kwargs)

class Leave(models.Model):
    id = models.IntegerField(auto_created=True,primary_key=True)
    from_date = models.DateTimeField(auto_now=False,auto_now_add=False)
    to_date = models.DateTimeField(auto_created=False,auto_now_add=False)
    employee = models.ForeignKey(to=Employee,on_delete=models.CASCADE)
