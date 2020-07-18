import requests
import json
from urllib import parse
from django.http import JsonResponse
from bot import button

def Search(bookName):
    url = 'https://lib.hknu.ac.kr/pyxis-api/1/collections/1/search?all=k%7Ca%7C'+parse.quote(bookName)+'&abc='

    d = requests.get(url)
    response = json.loads(d.text)
    try:
        total = response['data']['totalCount']
        listItems = [{
            "type": "title",
            "imageUrl": "",
            "title": "%s에 대한 검색 결과"%bookName,
            "linkUrl": {
              "type": "OS",
                "webUrl": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
            }
        }]





        for line in response['data']['list']:
            try:
                name = line['titleStatement']
                bookURL = line['id']
                thumbnailUrl = line['thumbnailUrl']
                place  = line['branchVolumes'][0]['name']
                status = line['branchVolumes'][0]['cState']
                format = {
                    "type": "item",
                    "imageUrl": thumbnailUrl,
                    "title": name,
                    "description": "%s/%s"%(place,status),
                    "linkUrl": {
                      "type": "OS",
                        "webUrl": "https://lib.hknu.ac.kr/#/search/detail/%s"%bookURL,

                    }
                }

                listItems.append(format)
                if(len(listItems) == 5):
                    break
            except:
                pass



        result = {
      "contents": [
        {
          "type": "card.list",
          "cards": [
            {
              "listItems": listItems,
              "buttons": [
                {
                  "type": "link",
                  "label": "검색결과 %d개 보기"%total,
                  "data":
                    {
                    "type": "OS",
                       "webUrl": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
                        "moUrl": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
                        "pcUrl": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
                        "pcCustomScheme": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
                        "macCustomScheme": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
                        "iosUrl": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
                        "iosStoreUrl": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
                        "androidUrl": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
                        "androidStoreUrl": 'https://lib.hknu.ac.kr/#/search/si?all=1%7Ck%7Ca%7C'+parse.quote(bookName)+'&mashup=PYXIS',
                    }

                }
              ]
            }
          ]
        }
      ],
      'quickReplies': button.quickReplies,

    }

        return JsonResponse(result)
    except:
        return JsonResponse({
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": bookName + "에 대한 검색 결과가 없어요."
                }
            }
        ],
        'quickReplies' : button.simpleTextquickReplies,
    }

})
