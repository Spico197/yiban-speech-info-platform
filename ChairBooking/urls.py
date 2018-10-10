"""ChairBooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from BookingApp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^stu-register/', views.stu_register),
    url(r'^logout/', views.logout),
    url(r'^booking$', views.booking),
    url(r'^booking-yiban$', views.booking_yiban),
    url(r'^booking-list/', views.booking_list),
    url(r'^cancel-booking$', views.cancel_booking),
    url(r'^get_oauth/$', views.get_oauth),
    url(r'^index', views.index),
    url(r'^detail$', views.detail),
    url(r'^debug/', views.debug),
    url(r'^$', views.index)
]
