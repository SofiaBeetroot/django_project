from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login

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