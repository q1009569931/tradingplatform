from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('purchase', views.Purchase.as_view(), name='purchase'),
    path('result/', csrf_exempt(views.alipayResult.as_view())),
    path('alipaylogin', views.alipayLogin.as_view(), name='alipayLogin'),
    path('alipayredirect/<int:userid>', views.alipayRedirect.as_view(), name='alipayredirect'),
]