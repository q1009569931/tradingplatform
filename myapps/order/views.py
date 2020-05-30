from django.shortcuts import render, redirect
from django.views.generic.base import View
from user.models import mall_address, mall_user
from product.models import mall_product_normal
from .models import mall_order, mall_pay_info
from django.contrib.auth.mixins import LoginRequiredMixin
from trading_platform.alipay_keys.alipay_custom import AliPayPageTrade, AliPayOauthToken
from django.http import HttpResponse
import random
from django.conf import settings
from urllib.parse import urlencode
from json import loads
import requests

# Create your views here.
def aliPay(A):
	# 初始化支付宝接口实例
    obj = A(
        appid="2016102300746249",                              # 支付宝沙箱里面的APPID，需要改成你自己的
        app_notify_url="http://hello.shenzhuo.vip:12057/order/result/",  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问，需要改成你自己的服务器地址
        return_url="http://hello.shenzhuo.vip:12057/order/result/",            # 如果支付成功，重定向回到你的网站的地址。需要你自己改，这里是我的服务器地址
        alipay_public_key_path=settings.ALIPAY_PUBLIC,  # 支付宝公钥
        app_private_key_path=settings.APP_PRIVATE,      # 应用私钥
        debug=True,  # 默认False,True表示使用沙箱环境测试
    )
    return obj

def tradeNoGenerator(user, good):
	'''
	user: 用户的实例
	good: 商品的实例
	return: str
	'''
	user_id = user.id
	good_id = good.id
	trade_no = str(user_id) + str(good_id) + str(random.randint(1,1000))
	return trade_no

class Purchase(LoginRequiredMixin, View):
	login_url = "/user/login/"

	def get(self, request):
		user = request.user
		pid = request.GET.get("pid")

		product = mall_product_normal.objects.get(id=pid)

		address = mall_address.objects.filter(user_id=user.id)
		context = {
			"address": address,
			"product": product,
		}
		return render(request, "purchasing.html", context=context)

	def post(self, request):
		# print(request.POST)
		# return HttpResponse("success")
		# 初始化支付宝实例
		alipay = aliPay(AliPayPageTrade)
		address_id = request.POST["address"]
		good_id = request.POST["good"]

		# 在数据库拿到相对应的数据
		product = mall_product_normal.objects.get(id=good_id)
		address = mall_address.objects.get(id=address_id)
		seller = mall_user.objects.get(id=product.user_id_seller) # 商品的发布者

		# 初始化需要的数据
		money = float(product.price)
		out_trade_no = tradeNoGenerator(request.user, product)
		subject = product.model
		trans_in_id = seller.alipay_id # 商品发布者的支付宝号


		# 更新数据库
		res = mall_order.objects.create(
				user_id=request.user.id,
				order_no=out_trade_no,
				product_id=good_id,
				address_id=address_id,
				payment=money,
				payment_type=0,
				status=1
			)

		# 拼接url
		query_params = alipay.direct_pay(
				subject=subject,
				out_trade_no=out_trade_no,
				total_amount=money,
				trans_in=trans_in_id
			)
		pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

		return redirect(pay_url)

class alipayResult(View):
	def get(self, request):
		# print(request.GET)
		money = request.GET.get("total_amount", "0") # 订单金额
		order_no = request.GET.get("out_trade_no") # 订单号
		trade_no = request.GET.get("trade_no") # 支付宝流水号

		# 更新订单
		order = mall_order.objects.get(order_no=order_no)
		if order.status == 1:
			order.status = 4
			order.save()
			product = mall_product_normal.objects.get(id=order.product_id)
			product.status = 0
			product.save()
			res = mall_pay_info.objects.create(
					user_id=order.user_id,
					order_no=order_no,
					payment_platform=0,
					platform_number=trade_no,
					platform_status="1"
				)

		title = "结算成功"
		detail = "已支付了%s元" % (money)
		context = {
			"title":title,
			"detail":detail,
		}
		return render(request, "remind.html", context=context)

	def post(self, request):
		order_no = request.POST.get("out_trade_no") # 订单号
		trade_no = request.POST.get("trade_no") # 支付宝流水号

		# 更新订单
		order = mall_order.objects.get(order_no=order_no)
		if order.status == 1:
			order.status = 4
			order.save()
			product = mall_product_normal.objects.get(id=order.product_id)
			product.status = 0
			product.save()
			res = mall_pay_info.objects.create(
					user_id=order.user_id,
					order_no=order_no,
					payment_platform=0,
					platform_number=trade_no,
					platform_status="1"
				)

		return HttpResponse("")


class alipayLogin(View, LoginRequiredMixin):
	# 获取支付宝用户信息测试
	login_url = "/user/login/"

	def get(self, request):
		parameter = {
			"app_id": "2016102300746249",
			"scope": "auth_user",
			"redirect_uri": "http://hello.shenzhuo.vip:12057/order/alipayredirect/"+str(request.user.id),
			"state": "init"
		}
		origin_url = "https://openauth.alipaydev.com/oauth2/publicAppAuthorize.htm"

		data = urlencode(parameter)
		alipay_url = origin_url + "?" + data
		print(alipay_url)

		return redirect(alipay_url)

class alipayRedirect(View):
	# 获取支付宝回调地址
	def get(self, request, userid):
		import uuid

		THREAD_LOCAL_uuid = str(uuid.uuid1())
		headers = {
			'Content-type': 'application/x-www-form-urlencoded;charset=GBK',
			"Cache-Control": "no-cache",
			"Connection": "Keep-Alive",
			"log-uuid": THREAD_LOCAL_uuid
		}
		code = request.GET.get("auth_code")
		alipay = aliPay(AliPayOauthToken)
		query_string, param = alipay.get_param(code)
		url = "https://openapi.alipaydev.com/gateway.do" + "?" + query_string
		response = requests.post(url, data=param, headers=headers)
		# print(type(response.text))
		# print(response.text)

		data = loads(response.text)
		alipay_id = data["alipay_system_oauth_token_response"]["user_id"]
		user = mall_user.objects.get(id=userid)
		user.alipay_id = alipay_id
		user.save()

		return redirect("/user/userhome/")
		