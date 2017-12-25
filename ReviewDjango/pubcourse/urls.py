from django.conf.urls import url
from pubcourse import views

app_name = 'PubCourse'
urlpatterns = [
    url(r'^$', views.CoursesList.as_view(), name='PubCourses'),
    url(r'^(?P<course_id>[0-9]+)/course-detail/$', views.CourseDetail.as_view(), name='CourseDetail')
]