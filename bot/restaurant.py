import requests
import json
from urllib import parse
#from django.http import JsonResponse
#from bot import button
from bs4 import BeautifulSoup
import time
import re


def student():
    #data = requests.get('https://www.hknu.ac.kr/kor/176/subview.do')
    data = requests.get('https://www.hknu.ac.kr/kor/176/subview.do?enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtvciUyRjIlMkZ2aWV3LmRvJTNGbW9uZGF5JTNEMjAyMC4wMi4yNCUyNndlZWslM0RwcmUlMjY%3D')
    soup = BeautifulSoup(data.text,"html.parser")
    now = time.localtime()
    today = now.tm_wday
    if (today >=5):
        print("없엉")
    today = (2*4)#(today * 2)+1
    body = soup.select('#viewForm > table > tbody ')
    body = str(body[0])
    body = body.split("<tr>")[1:]
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
        print(line,end="\n======================\n")

def teacher():
    #data = requests.get('https://www.hknu.ac.kr/kor/177/subview.do')
    data = requests.get('https://www.hknu.ac.kr/kor/177/subview.do?enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtvciUyRjMlMkZ2aWV3LmRvJTNGbW9uZGF5JTNEMjAxOS4xMi4zMCUyNndlZWslM0RwcmUlMjY%3D')
    soup = BeautifulSoup(data.text,"html.parser")
    now = time.localtime()
    today = now.tm_wday
    if (today >=5):
        print("없엉")
    today = (0*2)#(today * 2)+1
    body = soup.select('#viewForm > table > tbody ')
    body = str(body[0])
    body = body.split("<tr>")[1:]

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

        print(line,end="\n======================\n")

#t = "<br>삼색콩밥<br/>윽"
#line = re.sub("(<br>)|(<br/>)","\n",t)
student()
teacher()
