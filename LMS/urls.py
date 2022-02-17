"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import home_page
from myapp.views import dashboard
from myapp.views import trial
from myapp.views import *
from django.urls import path,include

from myapp.views import dashboard,signup,employeelogin,userlogout,create_leave_request,grant_leaves_request
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page),
    path('trial/', trial),
    path('signup/',signup),
    path('login/',employeelogin),
    path('logout/',userlogout),
    path('request-leave/',create_leave_request),
    path('grant-leave/',grant_leaves_request),
    path('Dashboard/',dashboard),
    path('index_view/',index_view ,name='home'),
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('dashboard/',include('dashboard.urls',namespace='dashboard')),





    path('welcome/',dashboard,name='dashboard'),

    # Employee
    path('employees/all/',dashboard_employees,name='employees'),
    path('employee/create/',dashboard_employees_create,name='employeecreate'),
    path('employee/profile/<int:id>/',dashboard_employee_info,name='employeeinfo'),
    path('employee/profile/edit/<int:id>/',employee_edit_data,name='edit'),

    # # Emergency
    # path('emergency/create/',views.dashboard_emergency_create,name='emergencycreate'),
    # path('emergency/update/<int:id>',views.dashboard_emergency_update,name='emergencyupdate'),

    # # Family
    # path('family/create/',views.dashboard_family_create,name='familycreate'),
    # path('family/edit/<int:id>',views.dashboard_family_edit,name='familyedit'),
    
    # #Bank
    # path('bank/create/',views.dashboard_bank_create,name='bankaccountcreate'),

    #---work-on-edit-view------#
    # path('bank/edit/<int:id>/',views.employee_bank_account_update,name='accountedit'),
    path('leave/apply/',leave_creation,name='createleave'),
    path('leaves/pending/all/',leaves_list,name='leaveslist'),
    path('leaves/approved/all/',leaves_approved_list,name='approvedleaveslist'),
    path('leaves/cancel/all/',cancel_leaves_list,name='canceleaveslist'),
    path('leaves/all/view/<int:id>/',leaves_view,name='userleaveview'),
    path('leaves/view/table/',view_my_leave_table,name='staffleavetable'),
    path('leave/approve/<int:id>/',approve_leave,name='userleaveapprove'),
    path('leave/unapprove/<int:id>/',unapprove_leave,name='userleaveunapprove'),
    path('leave/cancel/<int:id>/',cancel_leave,name='userleavecancel'),
    path('leave/uncancel/<int:id>/',uncancel_leave,name='userleaveuncancel'),
    path('leaves/rejected/all/',leave_rejected_list,name='leavesrejected'),
    path('leave/reject/<int:id>/',reject_leave,name='reject'),
    path('leave/unreject/<int:id>/',unreject_leave,name='unreject'),

    
]




