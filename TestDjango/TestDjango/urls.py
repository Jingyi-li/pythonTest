"""TestDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users import views
from django.conf import settings
from django.conf.urls.static import static
from PublicCourse.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.LoginView.as_view(), name='Login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='Logout'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^course/', include('PublicCourse.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 引用本地的图片需要在url后填入上诉代码！！！！
