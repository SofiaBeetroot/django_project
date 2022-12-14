"""django_beetroot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from api.views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('hello/', index),
    path('test/', QuestionList.as_view(), name='test'),
    path('blogs/', blog_view),
    path('question/create/', create_question),
    path('question/update/<int:id>', update_question),
    path('question/perform_update/<int:id>', perform_update),
    path('login/', login_view),
    path('login/auth/', auth_view),
    path('api/test', test_api),
    path('api/', main_view),
    path('api/sync', sync_main_view),
    path('api/async', async_with_sync_view),
    path('api/atos', sync_with_async_view),
    path('blog/async', async_blog_view)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
