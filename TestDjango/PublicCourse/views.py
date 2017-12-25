from django.shortcuts import render
from django.views.generic import View
from .models import PublicCourses

# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class CourseList(View):

    def get(self, request):
        course = PublicCourses.objects.all()
        return render(request, 'course-list.html', {'courses': course})
