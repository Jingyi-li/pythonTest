from django.db import models
from django.utils import timezone

# Create your models here.


class PublicCourses(models.Model):
    course_name = models.CharField('课程名称', max_length=50)
    course_context = models.CharField('课程描述', max_length=255, null=True, blank=True)
    course_level = models.CharField(choices=(('E', '低级'), ('M', '中级'), ('H', '高级')), max_length=2, default='E')
    course_students = models.SmallIntegerField('学习人数', null=True, blank=True)
    course_len = models.SmallIntegerField('时长', default=0)
    course_chapters = models.SmallIntegerField('章节',default=0)
    course_field = models.CharField('课程类别', max_length=100, null=True, blank=True)
    course_detail = models.TextField('课程详情', null=True, blank=True)
    course_colleage = models.CharField('授课机构', max_length=20, null=True, blank=True)
    course_teacher = models.CharField('授课教师', max_length=20)
    course_pubdate = models.DateTimeField('发布时间', default=timezone.now())
    course_cover = models.ImageField('课程封面', upload_to='PublicCourse/%Y/%M', null=True, blank=True)

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name
        ordering = ('-course_pubdate', )



