from django.urls import path
from . import views

app_name="donationapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('account/', views.account, name="account"),
    path('causes/', views.causes, name="causes"),
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('volunteering/', views.volunteer_opportunities, name="volunteering"),
    path('create/', views.create_opportunity, name="create"),
    path('volunteer/', views.volunteer_signup, name="volunteer")
]
