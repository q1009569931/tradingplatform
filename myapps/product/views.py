from django.shortcuts import render
from django.views.generic.base import View
from .models import mall_product_auction, mall_product_normal, mall_category
from user.models import mall_user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import json

# Create your views here.

class Home(View):
    def get(self, request):
        user = None
        if request.user.is_authenticated:
            user = request.user
        product = mall_product_normal.objects.filter(status=1).order_by('-update_time')[:5]
        context = {
            "user": user,
            "product": product,
        }
        print(user)
        return render(request, 'index.html', context=context)

class Product(View):
    #商品筛选页or商品详情页
    def get(self, request):
        keyword = request.GET.get('keyword') #如果有，就是筛选页
        productid = request.GET.get("pid")  #如果有，就是详情页
        content = request.GET.get("content")
        page = request.GET.get("page")
        user = request.user if request.user.is_authenticated else None

        #判断筛选页还是详情页
        if keyword:
            #说明是筛选页
            if keyword == 'all':
                #全部商品，默认按更新时间排序
                products = mall_product_normal.objects.filter(status=1).order_by('-update_time')
            else:
                pass
            # 获取分类信息
            categorys = mall_category.objects.all()


            product_list = Paginator(products, 9)   #每页商品数
            num_pages = product_list.num_pages
            #判断页数
            if page:
                page_now = int(page)
                #页码修正
                if page_now < 1:
                    page_now = 1
                if page_now > num_pages:
                    page_now = num_pages
            else:
                page_now = 1
            #尽量把当前页放在中间
            page_left = page_now - 3 if page_now -3 >= 1 else 1
            page_right = page_left + 6 if page_left + 6 <= num_pages else num_pages
            page_list = list(range(page_left, page_right+1))
            product_list = product_list.page(page_now)
            context = {
                'user': user,
                'keyword':keyword,
                'products':product_list,
                'page_now':page_now,
                'page_list':page_list,
                'num_pages': num_pages,
                'categorys': categorys,
            }
            return render(request, 'product.html', context=context)

        elif productid:
            product = mall_product_normal.objects.get(id=productid)
            user = request.user if request.user.is_authenticated else None
            seller = mall_user.objects.get(id=product.user_id_seller)
            context = {
                "user": user,
                "product": product,
                "seller": seller,
            }
            if not content or content == "detail":
                context["content"] = "detail"
            else:
                context["content"] = "image"
                sub_image_dict = json.loads(product.sub_image)
                sub_image_list  = []
                for i in sub_image_dict.values():
                    sub_image_list.append(i)
                context["sub_image"] = sub_image_list
            return render(request, 'productdetail.html', context=context)
        else:
            pass
        return render(request, 'product.html', context={'products':products})
