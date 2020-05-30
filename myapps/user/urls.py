from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('userhome/', views.UserHome.as_view(), name='userhome'),
    path('collection/', views.Collection.as_view(), name='collection'),
    path('address/', views.Address.as_view(), name='address'),
    path('publish/', views.Publish.as_view(), name='publish'),
]