from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import re

@csrf_exempt
def validates_date(request):

    if request.method == 'GET':
        try:
            if request.GET['date']:
                result = re.match("[\d]{1,2}/[\d]{1,2}/[\d]{4}", request.GET['date'])
                if result:
                    return HttpResponse('true')
                else:
                    return HttpResponse('false')

        except Exception as e:
            return HttpResponse('false')

