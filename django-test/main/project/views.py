# from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,  HttpResponseRedirect
from django.http.response import Http404
from django.template import context, loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.core import serializers
from polls.models import Question
def test(request):
    return HttpResponse("<h1> mysite</h1> <p> my site home page </p>")

def index(request):
    ehe=13
    return render(request, 'project/index.html')

def info(request):
    return render(request, 'project/info.html')

def showNumber(request, ehe):
    return render(request, 'project/index.html', {'ehe':ehe})

def testSerialize(request):
    data = serializers.serialize("json", Question.objects.all())
    return HttpResponse(data)