from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import UserProfile,ShoesDetail
from .serializers import RegisterSerializer,LoginSerializer,ShoeDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters,pagination

from django.contrib.auth import get_user_model
from .services import get_user_data,apple_get_user_data
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login,logout
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.views.decorators.csrf import ensure_csrf_cookie

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from django.http import HttpResponse
from rest_framework.authtoken.models import Token 
import traceback 
from django.shortcuts import render



User = get_user_model() 

def index(request):
    return render(request,'index.html')

class RegisterUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfile.objects.all()
    serializer_class = RegisterSerializer
    
    parser_classes = (MultiPartParser,FormParser)
    
    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    

class LoginUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request , *args , **kwargs):
        serializer = LoginSerializer(data = request.data)
        
        if serializer.is_valid():
            user_profile = serializer.validated_data['user_profile']
            
            token, created = Token.objects.get_or_create(user=user_profile)
            user_data = RegisterSerializer(user_profile).data 
            
            return Response({
                'user': user_data,
                'token': token.key, 
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
    
class CustomPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100

class ShoeView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = ShoesDetail.objects.all()
    serializer_class = ShoeDetailSerializer
    parser_classes = (MultiPartParser,FormParser)
    
    pagination_class = CustomPagination 
    
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields =  ['id','shoeName', 'shoeColorName', 'shoeStyleName','shoeOriginCountry']
    
    ordering_fields = ['id','shoePrice'] 
    
    def perform_create(self,serializer):
        serializer.save()
        
    def create(self,request , *args ,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        shoe_instance = serializer.instance
        
        for i in range(1,10):
            field_name = f'shoeMainImage{i}'
            if field_name in request.FILES:
                image_file = request.FILES[field_name]
                
                setattr(shoe_instance,field_name,image_file)
        
        shoe_instance.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data ,status=status.HTTP_201_CREATED,headers=headers)
    
    def get_serializer_context(self):
        return {'request': self.request}
    


class SingleShoeDetialView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = ShoesDetail.objects.all()
    serializer_class = ShoeDetailSerializer
    parser_classes = (MultiPartParser,FormParser)
    lookup_field = 'pk'
    
    def update(self,request,*args,**kwargs):
        partial = kwargs.pop('partial',False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data = request.data , partial=partial)
        serializer.is_valid(raise_exception=True)
        
        self.perform_update(serializer)
        
        shoe_instance = serializer.instance
        
        for i in range(1,10):
            field_name = f'shoeMainImage{i}'
            if field_name in request.FILES:
                image_file = request.FILES[field_name]
                setattr(shoe_instance,field_name,image_file)
            
            elif field_name in request.data and not request.data[field_name]:
                setattr(shoe_instance,field_name,None)
        
        shoe_instance.save()
        
        if partial:
            pass
            
        return Response(serializer.data)
    
    def get_serializer_context(self):
        return {'request': self.request}





class GoogleLoginApi(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        error = request.GET.get('error')
        validated_data = {
            'code':code,
            'error':error
        }
        
        try:
            user = get_user_data(validated_data=validated_data, request=request)
            if not user.is_authenticated:
                raise Exception(f"User authentication check failed: user.is_authenticated is {user.is_authenticated}")

            token, created = Token.objects.get_or_create(user=user)
            success_url = f"{settings.FRONTEND_LOGIN_SUCCESS_URL}?token={token.key}&username={user.username}&firstname={user.firstname}&lastname={user.lastname}&is_staff={user.is_staff}"
            
            print(f"Redirecting to: {success_url}") 
            
            return redirect(success_url)
            
        except Exception as e:
            traceback.print_exc() 
            print(f"--- Google Login Callback Failed: {e} ---")
            return redirect(f'{settings.FRONTEND_LOGIN_ERROR_URL}?error={str(e)}')


class LogoutApi(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse('200')
    
@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserStatusView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            'isAuthenticated': True,
            'username': user.username, 
            'firstname': user.firstname,
            'lastname': user.lastname,
            'is_staff': user.is_staff,
        })
        
class AppleLoginApi(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request, *args, **kwargs):
        code = request.GET.get('code')
        error = request.GET.get('error')
        validated_data = {
            'code':code,
            'error':error
        }
        try:
            user = apple_get_user_data(validated_data=validated_data,request=request)
            if not user.is_authenticated:
                raise Exception(f'Apple User authentication check failed:user.is_authenticated is {user.is_authenticated}')
            
            token, created = Token.objects.get_or_create(user=user)
            success_url = f'{settings.FRONTEND_LOGIN_SUCCESS_URL}?token={token.key}&username={user.username}&firstname={user.firstname}&lastname={user.lastname}&is_staff={user.is_staff}'
            
            print(f"Redirecting to : {success_url}")
            return redirect(success_url)
        except Exception as e:
            traceback.print_exc()
            print(f"Apple Login Callback Failed : {e}")
            return redirect(f'{settings.FRONTEND_LOGIN_ERROR_URL}?error={str(e)}')
        