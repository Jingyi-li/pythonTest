from django.conf.urls import url
from . import views


app_name = 'PublicCourse'

urlpatterns = [
    url(r'^course-list/$', views.CourseList.as_view(), name='courselist')
]