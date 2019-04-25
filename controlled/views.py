# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    #response = "Hi to controlled index page"
    #return HttpResponse(response)
    content = IndexPageContent.objects.filter(default = True).first()
    return render(request, 'controlled/index.html', {'content': content}) 