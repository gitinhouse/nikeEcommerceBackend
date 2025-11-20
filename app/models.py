from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserProfileManager(BaseUserManager):
    def create_user(self,username,password=None,**extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        user = self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,username,password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username,password,**extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.EmailField(max_length=100,unique=True)
    age= models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    hobbies = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4,unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserProfileManager()
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname'] 

    def __str__(self):
        return f'{self.firstname} {self.lastname} -- {self.username}'
    
    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'

    def get_short_name(self):
        return self.firstname
    
    class Meta:
        pass
    
    
class ShoesDetail(models.Model):
    shoeName = models.CharField(max_length=100)
    shoeDescription = models.CharField(max_length=200)
    shoePrice = models.CharField(max_length=100)
    shoeCoverImage = models.ImageField(upload_to='shoesCoverImage/')
    shoeInnerDescription = models.TextField()
    shoeColorName = models.CharField(max_length=200)
    shoeStyleName = models.CharField(max_length=100)
    shoeOriginCountry = models.CharField(max_length=100)
    shoeMainImage = models.ImageField(upload_to='shoesMainImage/')
    shoeMainImage2 = models.ImageField(upload_to='shoesMainImage/',null=True,blank=True)
    shoeMainImage3 = models.ImageField(upload_to='shoesMainImage/',null=True,blank=True)
    shoeMainImage4 = models.ImageField(upload_to='shoesMainImage/',null=True,blank=True)
    shoeMainImage5 = models.ImageField(upload_to='shoesMainImage/',null=True,blank=True)
    shoeMainImage6 = models.ImageField(upload_to='shoesMainImage/',null=True,blank=True)
    shoeMainImage7 = models.ImageField(upload_to='shoesMainImage/',null=True,blank=True)
    shoeMainImage8 = models.ImageField(upload_to='shoesMainImage/',null=True,blank=True)
    shoeMainImage9 = models.ImageField(upload_to='shoesMainImage/',null=True,blank=True)
    
    def __str__(self):
        return f'{self.shoeName} -- {self.shoePrice}'