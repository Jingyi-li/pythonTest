from django.db import models


# Create your models here.


class Orgnization(models.Model):
    org_name = models.CharField('机构名称', max_length=20, default='慕课网')
    org_area = models.CharField('所在地区', max_length=200, null=True, blank=True)
    org_type = models.CharField(choices=(('培训机构', '培训机构'), ('高校', '高校'), ('个人', '个人')), max_length=8,
                                default='个人')
    org_address = models.CharField('机构地址', max_length=200, null=True, blank=True)
    org_hotcourse = models.CharField('经典课程', max_length=100, null=True, blank=True)
    org_detail = models.TextField('机构简介', null=True, blank=True)
    org_image = models.ImageField('机构封面', upload_to='eduservice/%Y/%M', default='eduservice/default_org.png')

    def __str__(self):
        return self.org_name

    class Meta:
        verbose_name = '机构信息'
        verbose_name_plural = verbose_name


class OrgTeacher(models.Model):
    org = models.ForeignKey(Orgnization,  on_delete=models.CASCADE)
    tch_name = models.CharField('教师姓名', max_length=20, default='匿名')
    tch_image = models.ImageField('教师照片', upload_to='eduservice/%Y/%M', default='eduservice/default_tch.png')

    def __str__(self):
        return self.tch_name

    class Meta:
        verbose_name = '教师信息'
        verbose_name_plural = verbose_name
