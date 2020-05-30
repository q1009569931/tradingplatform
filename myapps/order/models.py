from django.db import models

# Create your models here.

'''

1. 由于Django不能修改AutoField的起始值，所以我尝试在表迁移成功后，利用Mysql语句
”ALTER TABLE table_name AUTO_INCREMENT = start_value;“，来修改起始值.

'''

class mall_order(models.Model):
    '''
    ALTER TABLE mall_order AUTO_INCREMENT = 10001;
    '''
    payment_type_choices = [
        (0, "在线支付"),
        (1, "货到付款"),
    ]
    status_choices = [
        (0, "已取消"),
        (1, "未付款"),
        (2, "已付款"),
        (3, "已发货"),
        (4, "交易成功"),
        (5, "交易关闭"),
    ]

    user_id = models.IntegerField(verbose_name="用户id")
    order_no = models.BigIntegerField(verbose_name="订单号")
    product_id = models.IntegerField(verbose_name="商品id")
    address_id = models.IntegerField(verbose_name="地址id")
    payment = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="实付价格（元）")
    payment_type = models.IntegerField(choices=payment_type_choices, verbose_name="支付类型，比如在线支付")
    status = models.IntegerField(choices=status_choices, verbose_name="订单状态")
    payment_time = models.DateTimeField(blank=True, null=True, verbose_name="支付时间")
    send_time = models.DateTimeField(blank=True, null=True, verbose_name="发货时间")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="交易完成时间")
    close_time = models.DateTimeField(blank=True, null=True, verbose_name="交易关闭时间")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "mall_order"
        indexes = [
            models.Index(fields=['order_no'], name='order_idx'),
            models.Index(fields=['user_id', 'order_no'], name='user_id_order_no_idx'),
        ]

class mall_pay_info(models.Model):
    '''
    ALTER TABLE mall_pay_info AUTO_INCREMENT = 10001;
    '''
    payment_platform_choices = [
        (0, "支付宝"),
        (1, "微信"),
    ]

    user_id = models.IntegerField(verbose_name="用户id")
    order_no = models.BigIntegerField(verbose_name="订单号")
    payment_platform = models.IntegerField(choices=payment_platform_choices, verbose_name="支付平台")
    platform_number = models.CharField(max_length=50, verbose_name="支付流水号")
    platform_status = models.CharField(max_length=30, verbose_name="支付状态")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "mall_pay_info"