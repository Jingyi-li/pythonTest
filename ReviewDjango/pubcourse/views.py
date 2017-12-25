from django.shortcuts import render, get_object_or_404
from .models import PubCourse
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


class CoursesList(View):

    def get(self, request):
        course = PubCourse.objects.all()
        return render(request, 'course-list.html', {'courses': course})


class CourseDetail(View):

    def get(self, request, course_id):
        course = PubCourse.objects.get(pk=course_id)
        return render(request, 'course-detail.html', {'Pubcourse': course})
