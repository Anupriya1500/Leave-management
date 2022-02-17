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
from myapp.views import dashboard, home_page, list_leave_requests

from myapp.views import dashboard,signup,employeelogin,userlogout,create_leave_request,grant_leaves_request
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page),
    path('signup/',signup),
    path('login/',employeelogin),
    path('logout/',userlogout),
    path('request-leave/',create_leave_request),
    path('grant-leave/<int:leave_id>/',grant_leaves_request),
    path('list-leave-requests/',list_leave_requests),
    path('Dashboard/',dashboard),
]
