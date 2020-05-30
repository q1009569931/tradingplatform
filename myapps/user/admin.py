from django.contrib import admin
from .models import mall_user

# Register your models here.

# Register your models here.
'''
user:admin
email:admin@163.com
password:admin
'''

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'phone', 'status')
    fields = ("username", "password", "email", "phone", "status", "role")

admin.site.register(mall_user, UserAdmin)