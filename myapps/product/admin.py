from django.contrib import admin
from .models import mall_product_normal
from .models import mall_product_auction

# Register your models here.

admin.site.register(mall_product_normal)
admin.site.register(mall_product_auction)