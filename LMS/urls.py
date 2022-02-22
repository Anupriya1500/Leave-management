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
# For pwd change
from django.contrib.auth import views as auth_views

from myapp.views import dashboard, home_page, leaves_view, line_manager_leave_requests,signup,employeelogin, update_leave_request,userlogout,create_leave_request,grant_leaves_request,list_leave_requests,list_line_managers_employees,list_pending_requests,list_approved_requests,list_rejected_requests
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page, name='home_page'),
    #path('',dashboard, name = 'dash'),
    path('signup/',signup, name = 'signup'),
    path('login/',employeelogin, name = 'login'),
    path('logout/',userlogout, name = 'logout'),

    path('request-leave/',create_leave_request, name = 'leave_request'),
    path('grant-leave/<int:leave_id>/',grant_leaves_request, name = 'grant_leaves_request'),
    path('update-leave/<int:leave_id>/',update_leave_request, name = 'update_leaves_request'),

    path('list-leave-requests/',list_leave_requests, name = 'list_leave_requests'),
    path('line-manger-leave-requests/',line_manager_leave_requests,name='line_manager_leave_requests'),
    path('list-line-managers-employees/',list_line_managers_employees,name='list_line_managers_employees'),
    path('list-pending-requests/', list_pending_requests , name = 'list_pending_requests'),
    path('list-approved-requests/', list_approved_requests, name = 'list_approved_requests'),
    path('list-rejected-requests/', list_rejected_requests, name = 'list_rejected_requests'),

    
    path('Dashboard/',dashboard, name='dashboard'),


    # Password change
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='commons/change-password.html',
            success_url = '/'
        ),
        name='change_password'),

# View Leaves
    path('leaves/all/view/<int:id>/',leaves_view,name='userleaveview'),
]




