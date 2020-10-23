from django.urls import path
from . import views

app_name="donationapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('account/', views.account, name="account"),
    path('causes/', views.causes, name="causes"),
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
]
