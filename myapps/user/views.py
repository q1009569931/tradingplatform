from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import mall_user, mall_collect, mall_address
from product.models import mall_product_normal
from .form import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
from django.urls import reverse

# Create your views here.


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = mall_user.createuser(**form.cleaned_data)
            user.save()
            return redirect('/home/')
        else:
            form = RegisterForm()
            return render(request, 'register.html', {'form': form})

class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home/')
            else:
                # 用户不存在
                print(user)
                return render(request, 'login.html', {'form': form})
        else:
            # 输入格式有问题
            print(form.errors)
            return render(request, 'login.html', {'form':form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/home/')

class UserHome(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request):
        user = request.user
        context = {
            "user": user,
            "create_time": user.create_time.strftime('%Y-%m-%d')
        }
        return render(request, 'userhome.html', context=context)

    def post(self, request):
        first_name = request.POST["first_name"]
        user = request.user
        user.first_name = first_name
        user.save()
        return redirect("/user/userhome/")

class Collection(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request):
        # 问题：product_id有可能出现竞拍商品和普通商品重复，怎么处理?
        user = request.user
        collections = mall_collect.objects.filter(user_id=user.id)
        products = []
        for collection in collections:
            products.append(mall_product_normal.objects.get(id=collection.product_id))
        context = {
            "products": products
        }

        return render(request, 'collection.html', context=context)

    def post(self, request):
        data = json.loads(request.body.decode())
        pid = data["data"]
        # 根据这个值来执行“删除”和“添加”的不同操作
        action = data["action"]
        user = request.user
        if action == "add":
            if mall_collect.objects.filter(user_id=user.id).filter(product_id=pid):
                print("1")
                response = HttpResponse("已收藏该商品！")
                response["Access-Control-Allow-Origin"] = "*"
                return response
            else:
                mall_collect.objects.create(
                        user_id=user.id,
                        product_id=pid
                    )
                print("2")
                response = HttpResponse("收藏成功！")
                response["Access-Control-Allow-Origin"] = "*"
                return response
        if action == "remove":
            try:
                c = mall_collect.objects.filter(user_id=user.id).get(product_id=pid)
                c.delete()
                return HttpResponse("OK")
            except:
                return HttpResponse("NO")

class Address(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request):
        user = request.user
        address_list = mall_address.objects.filter(user_id=user.id)
        aid = request.GET.get("aid")
        address = None

        if aid:
            address = mall_address.objects.get(id=aid)
            if address.user_id != user.id:
                return HttpResponse("ERROR!")

        context = {
            "address_list": address_list,
            "address": address
        }
        return render(request, "address.html", context=context)

    def post(self, request):
        user = request.user
        # 没有POST的是AJAX，就是删除；有的就是表单提交，添加或修改地址。
        if not request.POST:
            data = json.loads(request.body.decode())
            aid = data["data"]

            try:
                address = mall_address.objects.get(id=aid)
                if address.user_id == user.id:
                    address.delete()
                    return HttpResponse("OK")
                else:
                    return HttpResponse("NO")
            except:
                return HttpResponse("NO")

        else:
            aid = request.POST.get("id")
            if not aid:
                # 添加
                address = mall_address.objects.filter(user_id=user.id)
                # 超过6个不能在添加
                if len(address) >= 6:
                    return redirect("/user/address/")

                # 格式化数据
                data = {
                    'user_id': user.id,
                    'name': request.POST['name'],
                    'phone': request.POST['phone'],
                    'province': request.POST['province'],
                    'city': request.POST['city'],
                    'district': request.POST['district'],
                    'detail_address': request.POST['detail_address']
                }
                if request.POST['zip_number']:
                    data['zip_number'] = request.POST['zip_number']

                mall_address.objects.create(**data)
                print("success")
                return redirect("/user/address/")
            else:
                # 修改
                address = mall_address.objects.get(id=aid)
                if address.user_id != user.id:
                    return HttpResponse("ERROR!")
                else:
                    address.name = request.POST["name"]
                    address.phone = request.POST["phone"]
                    address.province = request.POST['province']
                    address.city = request.POST['city']
                    address.district = request.POST['district']
                    address.detail_address = request.POST['detail_address']
                    address.zip_number = request.POST['zip_number']
                    address.save()
                    return redirect("/user/address/")

class Publish(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request):
        return render(request, "publish.html")

    def post(self, request):
        if not request.user.alipay_id:
            return HttpResponse(
                '''
                您没有绑定支付宝账号，请先到"个人主页"绑定！ <br>
                <a href="/user/userhome/">点击跳转</a>
                ''')

        import os
        from django.conf import settings
        # 根据用户名生成路径
        path = os.path.join(settings.MEDIA_ROOT, request.user.username)

        post = request.POST
        main_image_data = request.FILES.get("main_image")
        sub_image_data = request.FILES.getlist("sub_image[]")
        data = {}
        data["user_id_seller"] = request.user.id
        data["user_id_consumer"] = 0

        # 用户发布的商品数
        num_product = len(mall_product_normal.objects.filter(user_id_seller=request.user.id))
        #处理文件
        self.handler_img(data, path, num_product+1, main_image_data, True)
        self.handler_img(data, path, num_product+1, sub_image_data, False)
        
        for k,v in post.items():
            if k not in ['csrfmiddlewaretoken', 'submit']:
                data[k] = v

        print(data)
        product = mall_product_normal.objects.create(**data)

        # 拼接url，重定向到商品详情页
        product_url = reverse('product') + "?" + "pid=" + str(product.id)
        return redirect(product_url)


    @staticmethod
    def handler_img(filedict, path, num_product, data, is_main):
        # filedict需要更新的字典, path路径, num_product发布商品数, data图片数据, is_main是否封面图
        # 保存文件并将文件目录添加到字典中
        # 图片的保存文件名是：
        # 如果是封面照，格式为：用户发布商品数+_+封面照+.+图片格式。如“2_封面照.jpg”
        # 如果是详情照，格式为：用户发布商品数+_+详情照照+_+第几张+.+图片格式。如“2_详情照_p3.jpg”
        import os
        if not os.path.exists(path):
            os.makedirs(path)

        if is_main:
            # 针对封面图片的处理，它只有一张
            imgformat = data.name.split(".")[-1] # 图片格式
            dirname = os.path.join(path, str(num_product) + "_" + "封面照" + "." + imgformat)
            # 并更新键值文件目录
            filedict["main_image"] =  "/media/" + os.path.split(path)[-1] + "/" + os.path.split(dirname)[-1] + "/"
            with open(dirname, "wb+") as file:
                for chunk in data.chunks():
                    file.write(chunk)
        else:
            # 针对详情图片的处理，它是一个列表
            file_json = dict()
            for i in range(len(data)):
                imgformat = data[i].name.split(".")[-1] # 图片格式
                dirname = os.path.join(path, str(num_product) + "_" + "详情照" + "_p" + str(i+1) + "." + imgformat)
                # 将文件的路径转换成网页的url，并拼接成字典，后续转换成json格式存入数据库
                file_json[str(i+1)] = "/media/" + os.path.split(path)[-1] + "/" + os.path.split(dirname)[-1] + "/"
                with open(dirname, "wb+") as file:
                    for chunk in data[i].chunks():
                        file.write(chunk)
            filedict["sub_image"] = json.dumps(file_json)
        