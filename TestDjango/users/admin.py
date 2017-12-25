from django.contrib import admin
from .models import UserProfile
# from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    fields = ('nick_name', 'sex', 'phone_no', 'birth_date', 'address', 'last_login', 'email', 'username',
              'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')
    list_display = ('nick_name', 'sex', 'phone_no', 'address', 'last_login', 'email' )
    list_filter = ['is_staff']
    search_fields = ['nick_name']


admin.site.register(UserProfile, UserAdmin)