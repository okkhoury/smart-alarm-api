# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def getResponse(request):
    # if post request came
    if request.method == 'POST':
        username = request.POST.get('username')
        response = {}

        response['value'] = 'Message'

        return JsonResponse(response, safe=False)

# Create your views here.
