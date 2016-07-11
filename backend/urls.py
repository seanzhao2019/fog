"""fog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name="backend"
urlpatterns = [
    url(r'index/$', views.List_user, name='backend_index'),
    url(r'api-info/$', views.Api_iot, name='backend_api'),
    url(r'account/$', views.Acc_manager, name='backend_account'),
    url(r'login/$', views.Login, name='backend_login'),
    url(r'detail/(?P<node_id>[0-9]+)/$', views.Admin_detail, name='backend_detail'),
]
