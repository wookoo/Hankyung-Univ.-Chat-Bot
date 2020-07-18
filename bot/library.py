import requests
import json
from urllib import parse
#from django.http import JsonResponse
def Search(bookName):
    url = 'https://lib.hknu.ac.kr/pyxis-api/1/collections/1/search?all=k%7Ca%7C'+parse.quote(bookName)+'&abc='
    d = requests.get(url)
    response = json.loads(d.text)
    try:
        total = response['data']['totalCount']
        print(response['data'])
        result = {
      "contents": [
        {
          "type": "card.list",
          "cards": [
            {
              "listItems": [
                {
                    "type": "title",
                    "imageUrl": "",
                    "title": "%s에 대한 검색 결과"%bookName,
                    "linkUrl": {
                      "type": "OS",
                        "webUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "moUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "pcUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "pcCustomScheme": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "macCustomScheme": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "iosUrl": "melonios://",
                        "iosStoreUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "androidUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "androidStoreUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264"
                    }
                },
                {
                    "type": "item",
                    "imageUrl": "https://i1.sndcdn.com/artworks-000193195536-fm8ibf-t500x500.jpg",
                    "title": "Shape of you",
                    "description": "Ed Sheeran",
                    "linkUrl": {
                      "type": "OS",
                        "webUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "moUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "pcUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "pcCustomScheme": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "macCustomScheme": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "iosUrl": "melonios://",
                        "iosStoreUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "androidUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "androidStoreUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264"
                    }
                },
                {
                    "type": "item",
                    "imageUrl": "https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18013515_1931895380356183_3704335724305186816_n.jpg",
                    "title": "We Don't Talk Anymore & I Hate U I Love U ",
                    "description": "The Chainsmokers",
                    "linkUrl": {
                      "type": "OS",
                        "webUrl": "",
                        "moUrl": "",
                        "pcUrl": "",
                        "pcCustomScheme": "",
                        "macCustomScheme": "",
                        "iosUrl": "melonios://",
                        "iosStoreUrl": "",
                        "androidUrl": "",
                        "androidStoreUrl": ""
                    }
                },
                {
                    "type": "item",
                    "imageUrl": "https://scontent-amt2-1.cdninstagram.com/t51.2885-15/e35/15803631_1786282854978804_1757317222419660800_n.jpg?ig_cache_key=MTQxODAzNDE1OTcyMTI3MTA2Nw%3D%3D.2&se=7",
                    "title": "Despacito",
                    "description": "Luis Fonsi ",
                    "linkUrl": {
                      "type": "OS",
                        "webUrl": "http://www.naver.com",
                    }
                },
                {
                    "type": "item",
                    "imageUrl": "https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/15056533_1759227474339700_3101894925281656832_n.jpg",
                    "title": "Don't Let Me Down",
                    "description": "The Chainsmokers",
                    "linkUrl": {
                      "type": "OS",
                        "webUrl": "",
                        "moUrl": "",
                        "pcUrl": "",
                        "pcCustomScheme": "",
                        "macCustomScheme": "",
                        "iosUrl": "melonios://",
                        "iosStoreUrl": "",
                        "androidUrl": "",
                        "androidStoreUrl": ""
                    }
                }
              ],
              "buttons": [
                {
                  "type": "link",
                  "label": "검색결과 %d개 모두보기"%total,
                  "data":
                    {
                       "webUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "moUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "pcUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "pcCustomScheme": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "macCustomScheme": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "iosUrl": "melonios://",
                        "iosStoreUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "androidUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264",
                        "androidStoreUrl": "http://www.melon.com/artist/timeline.htm?artistId=729264"
                    }

                }
              ]
            }
          ]
        }
      ],

    }
        #return JsonResponse(result)
    except:
        pass
        #return JsonResponse(result)

Search("고기")
