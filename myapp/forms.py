from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Employee, Leave, User
 
 
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
    from_date=forms.DateField(input_formats=['%Y-%m-%d'],help_text="YYYY-MM-DD")
    to_date=forms.DateField(input_formats=['%Y-%m-%d'],help_text="YYYY-MM-DD")
    class Meta:
        model=Leave
        exclude=['id','employee','is_leave_approved']
    def clean(self):
        cleaned_data = super().clean()
        from_date=cleaned_data.get("from_date")
        to_date=cleaned_data.get("to_date")
        if(from_date>=to_date):
            raise ValidationError(
                "From Date can Not be After To Date"
            )
    @transaction.atomic
    def save(self,current_user):
        leave_request=super().save(commit=False)
        leave_request.employee=Employee.objects.get(user=current_user)
        leave_request.save()
        return leave_request

class GrantLeaveRequestForm(forms.Form):
    employee_id = forms.CharField(max_length=50,disabled=True)
    max_leaves = forms.IntegerField(disabled=True)
    leaves_remaining = forms.IntegerField(disabled=True)
    from_date = forms.DateTimeField(disabled=True)
    to_date = forms.DateTimeField(disabled=True)
    is_leave_approved = forms.BooleanField()


class GrantLeaveRequestModelForm(forms.ModelForm):
    class Meta:
        model=Leave
        fields = '__all__'