from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField('昵称', max_length=200, null=True, blank=True)
    birth_date = models.DateTimeField('生日', null=True, blank=True)
    sex = models.CharField(choices=(('malse', '男'),('female','女'),('secrete','保密')), max_length=7, default='secrete')
    address = models.CharField('地址', max_length=500, null=True, blank=True)
    phone_no = models.CharField('手机号', max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

