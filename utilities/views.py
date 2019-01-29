from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import re
from datetime import datetime
from dateutil.parser import parse
@csrf_exempt
def validates_date(request):

    print(request)

    if request.method == 'GET':
        try:
            if request.GET['date']:
                result = re.match("[\d]{1,2}/[\d]{1,2}/[\d]{1,4}", request.GET['date'])
                second_result = re.match("[\d]{1,2}%2F[\d]{1,2}%2F[\d]{1,4}", request.GET['date'])
                print(request.GET['date'])

                if result:
                    print('first here')
                    split_date = request.GET['date'].split('/', 3)
                    day = int(split_date[0])
                    month = int(split_date[1])
                    year = int(split_date[2])

                    if \
                            not day <= 31 or \
                            not day > 0 or \
                            not month <= 12 or \
                            not month > 0 or \
                            not year >= 1900 or \
                            not year <= datetime.now().year:
                        print('not valid')
                        return JsonResponse(
                            dict(
                                set_attributes=dict(
                                    isDateValid=False
                                ),
                                messages=[]
                            )
                        )

                if second_result:
                    print('second here!')
                    split_date = request.GET['date'].split('%2F', 3)
                    print(request.GET['date'])
                    print(split_date)
                    day = int(split_date[0])
                    month = int(split_date[1])
                    year = int(split_date[2])
                    print(day, month, year)

                if result or second_result:
                    return JsonResponse(
                        dict(
                            set_attributes=dict(
                                isDateValid=True,
                                parentDOB=parse(request.GET['date'])
                            ),
                            messages=[]
                        )
                    )
                else:
                    print('not match')
                    return JsonResponse(
                        dict(
                            set_attributes=dict(
                                isDateValid=False
                            ),
                            messages=[]
                        )
                    )

        except Exception as e:
            return JsonResponse(
                dict(
                    set_attributes=dict(
                        isDateValid=False
                    ),
                    messages=[]
                )
            )

@csrf_exempt
def validates_kids_date(request):

    print(request)

    if request.method == 'GET':
        try:
            if request.GET['date']:
                result = re.match("[\d]{1,2}/[\d]{1,2}/[\d]{1,4}", request.GET['date'])
                second_result = re.match("[\d]{1,2}%2F[\d]{1,2}%2F[\d]{1,4}", request.GET['date'])
                print(request.GET['date'])

                if result:
                    print('first here')
                    split_date = request.GET['date'].split('/', 3)
                    day = int(split_date[0])
                    month = int(split_date[1])
                    year = int(split_date[2])

                    if \
                            not day <= 31 or \
                            not day > 0 or \
                            not month <= 12 or \
                            not month > 0 or \
                            not year >= datetime.now().year - 7 or \
                            not year <= datetime.now().year:
                        print('not valid')
                        return JsonResponse(
                            dict(
                                set_attributes=dict(
                                    isDateValid=False
                                ),
                                messages=[]
                            )
                        )

                if second_result:
                    print('second here!')
                    split_date = request.GET['date'].split('%2F', 3)
                    print(request.GET['date'])
                    print(split_date)
                    day = int(split_date[0])
                    month = int(split_date[1])
                    year = int(split_date[2])
                    print(day, month, year)

                if result or second_result:
                    return JsonResponse(
                        dict(
                            set_attributes=dict(
                                isDateValid=True,
                                childDOB=parse(request.GET['date'])
                            ),
                            messages=[]
                        )
                    )
                else:
                    print('not match')
                    return JsonResponse(
                        dict(
                            set_attributes=dict(
                                isDateValid=False
                            ),
                            messages=[]
                        )
                    )

        except Exception as e:
            return JsonResponse(
                dict(
                    set_attributes=dict(
                        isDateValid=False
                    ),
                    messages=[]
                )
            )

