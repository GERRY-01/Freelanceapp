from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('freelancer', views.freelancer, name='freelancer'),
    path('client', views.client, name='client'),
    path('jobs', views.jobs, name='jobs'),
    path('logout', views.logout_user, name='logout'),
]
