from django.urls import path
from . import views,HodView

urlpatterns = [
    path('members/', views.members, name='members'),
    
   
]