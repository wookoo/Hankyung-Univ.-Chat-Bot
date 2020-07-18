import requests
import json
from urllib import parse
from django.http import JsonResponse
from bot import button
from bs4 import BeautifulSoup
import time
import re


def student():
    #data = requests.get('https://www.hknu.ac.kr/kor/176/subview.do')
    now = time.localtime()
    today = now.tm_wday
    #today = 0
    if (today >=5):
        return noData()
    data = requests.get('https://www.hknu.ac.kr/kor/176/subview.do')
    #data = requests.get('https://www.hknu.ac.kr/kor/176/subview.do?enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtvciUyRjIlMkZ2aWV3LmRvJTNGbW9uZGF5JTNEMjAyMC4wMi4yNCUyNndlZWslM0RwcmUlMjY%3D')
    soup = BeautifulSoup(data.text,"html.parser")

    today = today * 4
    body = soup.select('#viewForm > table > tbody ')
    body = str(body[0])
    body = body.split("<tr>")[1:]
    result = "====================\n"
    for i in range(today,today+4):
        line = body[i].strip()
        line = re.sub("(<br>)|(<br/>)","\n",line)
        line = re.sub("</tr>","",line)
        line = re.sub("\d+\.\d+\.\d+","",line)
        line = re.sub("\( (월|화|수|목|금) \)","",line)
        line = re.sub("<t[d|h] rowspan=\"\d+\">","",line)
        line = re.sub("<|/|t[d|h]|br|>","",line)
        line = re.sub("!-- colspan=\"\d+\"--","",line)
        line = re.sub("&(gt;)|(&lt;)","==",line)
        line = re.sub("&amp;","&",line)
        line = line.strip()
        result += line+"\n====================\n"

    return JsonResponse({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result,
                    }
                }
            ],
            'quickReplies':button.simpleTextquickReplies,
        },
        })

def teacher():
    #data = requests.get('https://www.hknu.ac.kr/kor/177/subview.do')
    now = time.localtime()
    today = now.tm_wday
    return noData()
    if (today >=5):
        return noData()
        
    data = requests.get('https://www.hknu.ac.kr/kor/177/subview.do')
    #data = requests.get('https://www.hknu.ac.kr/kor/177/subview.do?enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtvciUyRjMlMkZ2aWV3LmRvJTNGbW9uZGF5JTNEMjAxOS4xMi4zMCUyNndlZWslM0RwcmUlMjY%3D')
    soup = BeautifulSoup(data.text,"html.parser")

    today = (today * 2)
    body = soup.select('#viewForm > table > tbody ')
    body = str(body[0])
    body = body.split("<tr>")[1:]

    result = "====================\n"

    for i in range(today,today+2):
        line = body[i].strip()
        line = re.sub("(<br>)|(<br/>)","\n",line)
        line = re.sub("</tr>","",line)
        line = re.sub("\d+\.\d+\.\d+","",line)
        line = re.sub("\( (월|화|수|목|금) \)","",line)
        line = re.sub("<t[d|h] rowspan=\"\d+\">","",line)
        line = re.sub("<|/|t[d|h]|br|>","",line)
        line = re.sub("!-- colspan=\"\d+\"--","",line)
        line = re.sub("&(gt;)|(&lt;)","==",line)
        line = re.sub("&amp;","&",line)
        line = line.strip()
        result += line+"\n====================\n"

        return JsonResponse({
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": result,
                }
            }
        ],
        'quickReplies':button.simpleTextquickReplies,
    },
    })

def noData():
    return JsonResponse({
"version": "2.0",
"template": {
    "outputs": [
        {
            "simpleText": {
                "text": "오늘은 학식이 없습니다!"
            }
        }
    ],
    'quickReplies':button.simpleTextquickReplies,
},
})

def Search(restaurant):
    if restaurant == "학생회관 식단":
        return student()
    else:
        return teacher()
