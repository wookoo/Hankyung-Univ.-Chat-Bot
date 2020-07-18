from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from bot import library
from bot import button
import json
import re

# Create your views here.

@csrf_exempt
def message(request):

    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    command = return_json_str['userRequest']['utterance']
    command = command.strip()
    command = command.replace(" ","")
    if command == "도서검색":
        bookName = return_json_str['action']['params']['bookName']
        return library.Search(bookName)



    elif command == "오늘의학식":
        restaurant = return_json_str['action']['params']['restaurant']
        print(restaurant)
        return JsonResponse({
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "오늘의학식은.."
                }
            }
        ],
        'quickReplies':button.simpleTextquickReplies,
    },
    })





    else:

        return JsonResponse({
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "지원하지 않는 명령어에요"
                }
            }
        ],
        'quickReplies':button.simpleTextquickReplies,
    },

})

@csrf_exempt
def check(request,value):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    command = return_json_str['utterance']
    command = command.strip()
    isTrue = True

    if value == 'name':
        isTrue = bool(re.match('^[가-힣]{2,4}$', command))

        return JsonResponse({
        "status": "FAIL",
        "message" : text})
    elif value == 'restaurant':
        isTrue = bool(re.match('^학생회관 식단|교직원 식당$',command))


    if isTrue:
        return JsonResponse({
        "status": "SUCCESS"})
    return JsonResponse({"status": "FAIL",
    'quickReplies': [{
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]})
