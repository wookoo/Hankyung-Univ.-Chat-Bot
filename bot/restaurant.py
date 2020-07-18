import requests
import json
from urllib import parse
#from django.http import JsonResponse
#from bot import button
from bs4 import BeautifulSoup
import time
def Search(restaurant):
    data = requests.get('https://www.hknu.ac.kr/kor/176/subview.do')
    soup = BeautifulSoup(data.text,"html.parser")
    now = time.localtime()
    today = now.tm_wday
    if (today >=5):
        print("없엉")
    today = (0*2)#(today * 2)+1

    body = soup.select('#viewForm > table > tbody ')
    body = str(body[0])
    body = body.split("<tr>")[1:]
    for i in range(today,today+4):
        print(body[i])
    

Search(123)
