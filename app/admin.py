from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import UserProfile ,ShoesDetail

admin.site.register(UserProfile)

@admin.register(ShoesDetail)
class ShoesDetailAdmin(ModelAdmin):
    list_display = ['id' , 'shoeName' , 'shoePrice']