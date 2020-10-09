from django.urls import path
from . import views

app_name="donationapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('account/', views.account, name="account")
]
