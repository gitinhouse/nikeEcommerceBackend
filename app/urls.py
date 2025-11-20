from django.urls import path,include
from app import views

urlpatterns = [
    path('',views.RegisterUserView.as_view(),name='register'),
    path('login/',views.LoginUserView.as_view(),name='login'),
    path('shoeDetails/',views.ShoeView.as_view(),name='shoes'),
    path('shoeDetails/<int:pk>/',views.SingleShoeDetialView.as_view(),name='singleShoe'),
    
    path('google/', views.GoogleLoginApi.as_view(), name='google-login-callback'),
    path('user/', views.UserStatusView.as_view(), name='user-status'),
    
    path('apple/',views.AppleLoginApi.as_view(),name='apple-login-callback')
    
]

