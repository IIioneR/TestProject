from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.CreateUserAccountView.as_view(), name='registration'),
    path('login/', views.UserAccountLoginView.as_view(), name='login'),
    path('logout/', views.UserAccountLogoutView.as_view(), name='logout'),
    path('profile/', views.UserAccountProfileView.as_view(), name='profile'),
]
