from django.db import models

# Create your models here.

'''

1. 由于Django不能修改AutoField的起始值，所以我尝试在表迁移成功后，利用Mysql语句
”ALTER TABLE table_name AUTO_INCREMENT = start_value;“，来修改起始值.

'''

class mall_product_normal(models.Model):
    '''
    ALTER TABLE mall_product_normal AUTO_INCREMENT = 10001;
    '''
    status_choices = [
        (0, "已售"),
        (1, "在售"),
        (2, "下架"),
        (3, "删除"),
    ]

    brand = models.CharField(max_length=20, verbose_name="品牌")
    brand_sub = models.CharField(max_length=20, verbose_name="子品牌", default="无")
    model = models.CharField(max_length=20, verbose_name="型号")
    detail = models.TextField(verbose_name="商品的描述")
    price = models.DecimalField(max_digits=20, decimal_places=2)
    main_image = models.CharField(max_length=30, verbose_name="展示框的图片")
    sub_image = models.TextField(verbose_name="更多图片")
    status = models.IntegerField(choices=status_choices, verbose_name="商品的状态", default=1)
    user_id_seller = models.IntegerField(verbose_name="卖家id")
    user_id_consumer = models.IntegerField(blank=True, verbose_name="买家id")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mall_product_normal"
        indexes = [
            models.Index(fields=['brand', 'model', 'price'], name='brand_model_price_idx'),
            models.Index(fields=['user_id_seller'], name='user_id_idx'),
        ]

class mall_product_auction(models.Model):
    '''
    ALTER TABLE mall_product_auction AUTO_INCREMENT = 10001;
    '''
    status_choices = [
        (0, "在售"),
        (1, "已售"),
        (2, "下架"),
        (3, "删除"),
    ]

    brand = models.CharField(max_length=20, verbose_name="品牌")
    brand_sub = models.CharField(max_length=20, verbose_name="子品牌", default="无")
    model = models.CharField(max_length=20, verbose_name="型号")
    detail = models.TextField(verbose_name="商品的描述")
    first_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="首拍价格")
    late_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="当前的价格")
    main_image = models.CharField(max_length=30, verbose_name="展示框的图片")
    sub_image = models.TextField(verbose_name="更多图片")
    status = models.IntegerField(choices=status_choices, verbose_name="商品的状态")
    user_id_seller = models.IntegerField(verbose_name="卖家id")
    user_id_consumer = models.IntegerField(blank=True, null=True, verbose_name="买家id")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mall_product_auction"
        indexes = [
            models.Index(fields=['brand', 'model', 'late_price'], name='brand_model_price_idx'),
            models.Index(fields=['user_id_seller'], name='user_id_idx'),
        ]

class mall_goods_info(models.Model):
    brand = models.CharField(max_length=30, verbose_name="品牌")
    model = models.CharField(max_length=40, verbose_name="型号")
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="参考价格")
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mall_goods_info"
        indexes = [
            models.Index(fields=['model'], name='model_idx'),
        ]

class mall_category(models.Model):
    name = models.CharField(max_length=20, verbose_name="分裂名称")

    class Meta:
        db_table = "mall_category"