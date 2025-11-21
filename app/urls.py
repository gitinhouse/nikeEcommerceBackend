from django.urls import path,include,re_path
from app import views

urlpatterns = [
    
    path('api/register/',views.RegisterUserView.as_view(),name='register'),
    path('api/login/',views.LoginUserView.as_view(),name='login'),
    path('api/shoeDetails/',views.ShoeView.as_view(),name='shoes'),
    path('api/shoeDetails/<int:pk>/',views.SingleShoeDetialView.as_view(),name='singleShoe'),
    
    path('api/google/', views.GoogleLoginApi.as_view(), name='google-login-callback'),
    path('api/user/', views.UserStatusView.as_view(), name='user-status'),
    
    path('api/apple/',views.AppleLoginApi.as_view(),name='apple-login-callback'),
    
    re_path(r'^(?!api/).*$', views.index, name='index'), 
    
]

