from django.db import models
from eduservice.models import OrgTeacher, Orgnization

# Create your models here.


class PubCourse(models.Model):
    course_name = models.CharField('课程名称', max_length=20, default='Python')
    # course_teacher = models.CharField('授课老师', max_length=20, default=tch.tch_name)
    course_context = models.TextField('课程描述', null=True, blank=True)
    org = models.ForeignKey(Orgnization, verbose_name='课程机构', on_delete=models.CASCADE)
    tch = models.ForeignKey(OrgTeacher, verbose_name='上课老师', on_delete=models.CASCADE)
    course_level = models.CharField(choices=(('低级', '低级'), ('中级', '中级'), ('高级', '高级')), default='低级', max_length=4)
    course_students = models.IntegerField('上课人数', default=0)
    course_length = models.IntegerField('课程时长', default=0)
    course_chapter = models.IntegerField('课程章节', default=0)
    course_field = models.CharField('课程类别', max_length=200, null=True, blank=True, default='Python')
    course_follower = models.IntegerField('收藏', default=0)
    course_detail = models.TextField('课程详情', null=0, blank=0)
    # course_org = models.CharField('授课机构', max_length=30, default=org.org_name)
    course_cover = models.ImageField('课程封面', upload_to='PubCourse/%Y/%M', default='PubCourse/default.jpg')

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = '公开课'
        verbose_name_plural = verbose_name
