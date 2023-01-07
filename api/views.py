import time
import asyncio
import httpx
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from asgiref.sync import sync_to_async, async_to_sync

from .models import *
from .forms import QuestionForm, QuestionModelFrom, LoginForm


def index(request):
    return HttpResponse("Hello, world! It is Beetroot)")


def test(request):
    print(request.method)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('api/test.html')
    context = {
        'list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def blog_view(request):
    all_blogs = Blog.objects.all()
    template = loader.get_template('api/blog.html')
    context = {
        'list': all_blogs,
    }
    return HttpResponse(template.render(context, request))


def create_question(request):
    template = loader.get_template('api/question.html')
    if request.method == 'POST':
        form = QuestionModelFrom(request.POST)
        if form.is_valid():
            Question.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('test/')
    else:
        form = QuestionModelFrom()
    return HttpResponse(template.render({'form': form}, request))


def update_question(request, id):
    quest = Question.objects.get(id=id)
    template = loader.get_template('api/update.html')
    context = {'quest': quest}
    return HttpResponse(template.render(context, request))


def perform_update(request, id):
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken', None)
    Question.objects.filter(id=id).update(**data)
    return HttpResponseRedirect(reverse('test'))


class QuestionList(ListView):
    template_name = 'api/test.html'
    model = Question

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Question.objects.all()
        return context


def home_view(request):
    query = Entry.objects.all()
    template = loader.get_template('extended.html')
    context = {'blog_entries': query}
    return HttpResponse(template.render(context, request))


def login_view(request):
    template = loader.get_template('api/login.html')
    form = LoginForm()
    return HttpResponse(template.render({'form': form}, request))


def auth_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('test'))
        else:
            return HttpResponse('Wrong method')


def test_api(request):
    time.sleep(1)
    message = {'message': 'Hello from Beetroot'}
    if 'task_id' in request.GET:
        message['task_id'] = request.GET.get('task_id')
    return JsonResponse(message)


async def http_for_async():
    for i in range(5):
        async with httpx.AsyncClient() as client:
            req = await client.get('http://localhost:8000/api/test', params={'task_id': i})
            print(req.json())

async def main_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_for_async())
    return HttpResponse('Not blocking request')


def http_for_sync():
    for i in range(5):
        req = httpx.get('http://localhost:8000/api/test', params={'task_id': i})
        print(req.json())
def sync_main_view(request):
    http_for_sync()
    return HttpResponse('Blocking request')


async def async_with_sync_view(request):
    loop = asyncio.get_event_loop()
    async_function = sync_to_async(http_for_sync, thread_sensitive=False)
    loop.create_task(async_function())
    return HttpResponse("Non-blocking HTTP request (via sync_to_async)")


def sync_with_async_view(request):
    sync_func = async_to_sync(http_for_async)
    sync_func()
    return HttpResponse('Blocking HTTP request (via async_to_sync)')


def http_blog_view():
    time.sleep(10)
    print('redirect')
    return redirect('http://localhost:8000/blogs/')

async def async_blog_view(request):
    loop = asyncio.get_event_loop()
    async_blog = sync_to_async(http_blog_view, thread_sensitive=False)
    loop.create_task(async_blog())
    return HttpResponse('Async Blog View')