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


urlpatterns = [
    url(r'^requesttoken/?', views.Register_NodeInfo, name='Register_NodeInfo'),
    url(r'^file/?', views.Upload_File, name='Upload_File'),
    url(r'^sensor/?', views.Update_Sensordata, name='Update_Sensordata'),
    url(r'^updatepriority/?', views.Update_Priority, name='Update_Priority'),
    url(r'^refreshtoken/?', views.Update_Token, name='Update_Token'),
    url(r'^updateservicetype/?', views.Update_Service_Type, name='Update_Service_Type'),
    url(r'^updatesecuritylevel/?', views.Update_Token_Security_Level, name='Update_Token_Security_Level'),
    url(r'^priority/?', views.Get_Priority, name='Get_Priority'),
    url(r'^servicetype/?', views.Get_Service_Type, name='Get_Service_Type'),
    url(r'^securitylevel/?', views.Get_Token_Security_Level, name='Get_Token_Security_Level'),
]
