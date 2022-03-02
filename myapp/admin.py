
from curses.ascii import EM
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm
from .models import Employee, Leave, User
 
class UserAdmin(UserAdmin):
   add_form = UserCreationForm
 
   # define fields to be used in displaying the User model.
  
   list_display = ('email', 'name', 'is_admin')
   list_filter = ('is_admin',)
   fieldsets = (
       (None, {'fields': ('email', 'name', 'password')}),
       ('Permissions', {'fields': ('is_admin',)}),
   )
   add_fieldsets = (
       (None, {
           'classes': ('wide',),
           'fields': ('email','name', 'password1', 'password2'),
       }),
   )
   ordering = ('email',)
   filter_horizontal = ()
 

class EmployeeAdminSide(admin.ModelAdmin):
    model = Employee
    list_display = ('empId','user','line_manager','position')
    list_filter = ('line_manager',)


class LeaveAdminSide(admin.ModelAdmin):
    model = Leave
    list_display = ('id','from_date','to_date','employee','status',)
    list_filter = ('employee',)

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Employee,EmployeeAdminSide)
admin.site.register(Leave,LeaveAdminSide)