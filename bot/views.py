from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from bot import library
from bot import button
import json

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
