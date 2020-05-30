from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Create your models here.

# Create your models here.

'''

1. 由于Django不能修改AutoField的起始值，所以我尝试在表迁移成功后，利用Mysql语句
”ALTER TABLE table_name AUTO_INCREMENT = start_value;“，来修改起始值.

'''
# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, password, email, phone, status=1):
#         user = self.model(username=username, email=email, phone=phone, status=1)
#         user.set_password(password)
#         user.is_admin = False
#         user.is_staff = False
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password, email, phone, status=1):
#         user = self.create_user(username=username, password=password, email=email, phone=phone, status=1)
#         user.is_admin = True
#         user.is_staff = True
#         user.save(using=self._db)
#         return user

class mall_user(AbstractUser):
    '''
    1.ALTER TABLE mall_user AUTO_INCREMENT = 1001;
    2.继承了AbstractBaseUser字段有：password，last_login, is_active
    '''
    role_choices = [
        (1, "普通用户"),
        (2, "管理员"),
    ]
    status_choices = [
        (1, "正常"),
        (2, "注销"),
        (3, "异常"),
    ]
    username = models.CharField(max_length=20, verbose_name="用户名，唯一", unique=True)
    email = models.CharField(max_length=30, verbose_name="邮箱")
    phone = models.CharField(max_length=20, verbose_name="手机号")
    alipay_id = models.CharField(blank=True, max_length=30, verbose_name="支付宝用户号")
    status = models.IntegerField(choices=status_choices, verbose_name="用户状态", default=1)
    role = models.IntegerField(choices=role_choices, verbose_name="用户身份", default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mall_user"
        indexes = [
            models.Index(fields=['username'], name='username_unique'),
        ]

    @classmethod
    def createuser(cls, **d):
        user = cls.objects.create_user(
                username=d["username"],
                password=d["password"],
                email=d["email"],
                phone=d["phone"],
            )
        return user

class mall_address(models.Model):
    '''
    ALTER TABLE mall_address AUTO_INCREMENT = 10001;
    '''
    user_id = models.IntegerField(verbose_name="用户id")
    name = models.CharField(max_length=20, verbose_name="收获姓名")
    phone = models.CharField(max_length=20, verbose_name="收获电话")
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    district = models.CharField(max_length=20, verbose_name="区/县")
    detail_address = models.CharField(max_length=30, verbose_name="详细地址")
    zip_number = models.CharField(max_length=20, verbose_name="邮编", default="000000")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "mall_address"
        indexes = [
            models.Index(fields=['user_id'], name='user_id_idx'),
        ]

class mall_collect(models.Model):
    '''
    ALTER TABLE mall_collect AUTO_INCREMENT = 10001;
    '''
    user_id = models.IntegerField(verbose_name="用户id")
    product_id = models.IntegerField(verbose_name="商品id")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "mall_collect"
        indexes = [
            models.Index(fields=['user_id'], name='user_id_idx'),
        ]