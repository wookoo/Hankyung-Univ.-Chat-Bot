from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from bot import library
from bot import button
from bot import restaurant
import json
import re
import sqlite3

# Create your views here.

BEST_FRIEND_DB = "bot/bestFriend.db"

@csrf_exempt
def message(request):

    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    command = return_json_str['userRequest']['utterance']
    command = command.strip()
    bot_user_key = (return_json_str['userRequest']['user']['properties']['bot_user_key'])
    if command == "도서 검색":
        bookName = return_json_str['action']['params']['bookName']
        return library.Search(bookName)



    elif command == "오늘의 학식":
        res = return_json_str['action']['params']['restaurant']
        return restaurant.Search(res)

    elif command == "베프팅 신청":
        return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': "매칭 종료로 신청 불가"
                        }
                    }],
                    'quickReplies': button.bestFriendquickReplies
                }
            })
        try:
            con = sqlite3.connect(BEST_FRIEND_DB)
            cur = con.cursor()
            phoneNumber = return_json_str['action']['params']['phoneNumber']
            gender = return_json_str['action']['params']['gender']
            nickName = return_json_str['action']['params']['nickName']
            addmissionYear = return_json_str['action']['params']['addmissionYear']
            subject = return_json_str['action']['params']['subject']
            interest1 = return_json_str['action']['params']['interest1']
            interest2 = return_json_str['action']['params']['interest2']
            assert interest1 != interest2
            cur.execute("insert into user values(?,?,?,?,?,?,?,?)",(bot_user_key,nickName,phoneNumber,addmissionYear,subject,gender,interest1,interest2))
            con.commit()
            text = "신청 완료.\n"
            text += "----신청 정보----\n"
            text += "닉네임 : %s\n"%nickName
            text += "연락처 : %s\n"%phoneNumber
            text += "학번 : %s\n"%addmissionYear[2:]
            text += "학과 : %s\n"%subject
            text += "성별 : %s성\n"%gender
            text += "관심사 1 : %s\n"%interest1
            text += "관심사 2 : %s\n==============="%interest2
            text += "\n베프팅 신청 상태 를 눌러 정상신청됬는지 확인부탁드립니다."

        except AssertionError:
            text = "신청에 실패했습니다.\n첫번째 관심사와 두번째 관심사는 다르게 설정해주세요."

        except sqlite3.IntegrityError:
            cur.execute("select * from user where bot_user_key = '%s'"%bot_user_key)
            _,nickName,phoneNumber,addmissionYear,subject,gender,interest1,interest2 = cur.fetchone()
            text = "이미 신청되어 있습니다!\n"
            text += "----사전 신청 정보----\n"
            text += "닉네임 : %s\n"%nickName
            text += "연락처 : %s\n"%phoneNumber
            text += "학번 : %s\n"%addmissionYear[2:]
            text += "학과 : %s\n"%subject
            text += "성별 : %s성\n"%gender
            text += "관심사 1 : %s\n"%interest1
            text += "관심사 2 : %s\n==============="%interest2


        except Exception as ex:
            text = "예상치 못한 오류가 발생했습니다. \n다시 신청해주세요..\n오류명 : "
            text += str(ex)
        finally:
            con.close()
        return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': text
                        }
                    }],
                    'quickReplies': button.bestFriendquickReplies
                }
            })
    elif command == "베프팅 신청 상태":
        con = sqlite3.connect(BEST_FRIEND_DB)
        cur = con.cursor()
        try:
            sql = "select * from user where bot_user_key == '%s'"%bot_user_key
            cur.execute(sql)
            data = cur.fetchone()
            _,nickName,phoneNumber,addmissionYear,subject,gender,interest1,interest2 = data
            text = "----신청 정보----\n"
            text += "닉네임 : %s\n"%nickName
            text += "연락처 : %s\n"%phoneNumber
            text += "학번 : %s\n"%addmissionYear[2:]
            text += "학과 : %s\n"%subject
            text += "성별 : %s성\n"%gender
            text += "관심사 1 : %s\n"%interest1
            text += "관심사 2 : %s"%interest2
        except Exception as ex:
            text = "신청 정보가 없습니다."
        finally:
            con.close()

        return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': text
                        }
                    }],
                    'quickReplies': button.bestFriendquickReplies
                }
            })
    elif command == "베프팅 신청 취소":
        return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': "매칭 종료로 취소 불가"
                        }
                    }],
                    'quickReplies': button.bestFriendquickReplies
                }
            })
        cancel = return_json_str['action']['params']['cancel']
        if cancel == "네":
            con = sqlite3.connect(BEST_FRIEND_DB)
            cur = con.cursor()
            try:
                sql = "select * from user where bot_user_key == '%s'"%bot_user_key
                cur.execute(sql)
                data = cur.fetchone()
                _,nickName,phoneNumber,addmissionYear,subject,gender,interest1,interest2 = data
                cur.execute("delete from user where bot_user_key == '%s'"%bot_user_key)
                con.commit()
                text = "신청이 취소되었습니다\n"
                text += "----취소 정보----\n"
                text += "닉네임 : %s\n"%nickName
                text += "연락처 : %s\n"%phoneNumber
                text += "학번 : %s\n"%addmissionYear[2:]
                text += "학과 : %s\n"%subject
                text += "성별 : %s성\n"%gender
                text += "관심사 1 : %s\n"%interest1
                text += "관심사 2 : %s\n----------"%interest2
                text += "\n베프팅 신청 상태 를 눌러 정상취소됬는지 확인부탁드립니다."
            except Exception as ex:
                text = "취소할 정보가 없습니다!"
            finally:
                con.close()
        else:
            text = "알겠습니다."

        return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': text
                        }
                    }],
                    'quickReplies': button.bestFriendquickReplies
                }
            })
    elif command == "베프팅 매칭 결과":
        try:

            con = sqlite3.connect(BEST_FRIEND_DB)
            cur = con.cursor()
            sql = "select * from result where bot_user_key = '%s'"%bot_user_key
            cur.execute(sql)
            matches = cur.fetchall()
            assert len(matches) != 0
            text = "---- 매칭결과 ----\n"

            for match in matches:
                _,nickName,phoneNumber,addmissionYear,subject,gender,interest1,interest2 = match
                text += "닉네임 : %s\n"%nickName
                text += "연락처 : %s\n"%phoneNumber
                text += "학번 : %s\n"%addmissionYear[2:]
                text += "학과 : %s\n"%subject
                text += "성별 : %s성\n"%gender
                text += "관심사 1 : %s\n"%interest1
                text += "관심사 2 : %s\n===============\n"%interest2
            text += "총 %d분이 매칭 되었어요.\n"%len(matches)
            text += "해당 결과는 8월 1일 23:59까지 공개되요."
            #text = "아직 매칭되지 않았어요.\n매칭결과는 7월 20일 점심쯤에 나와요."
        except Exception as ex:

            text = "신청하신 정보가 없거나 매칭되지 않았습니다.\n신청 상태를 확인해주세요.\n신청 결과가 있는데 조회가 안되시면,다시 매칭결과 확인 부탁드려요.\n"
            text += "그래도 조회가 안되시면 문의하기로 아래 메세지와 함께 전화번호 남겨주세요.\n"
            text += "ERROR : " + str(ex)
        finally:
            con.close()

        return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': text
                        }
                    }],
                    'quickReplies': button.bestFriendquickReplies
                }
            })

        return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': "개발중!"
                        }
                    }],
                    'quickReplies': button.bestFriendquickReplies
                }
            })

    elif command == "베프팅":
        return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': "베프팅 항목이에요.\n아래에서 목록을 선택해주세요."
                        }
                    }],
                    'quickReplies': button.bestFriendquickReplies
                }
            })

    elif command == "처음으로":
        return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': "처음으로 돌아갑니다"
                        }
                    }],
                    'quickReplies': button.simpleTextquickReplies
                }
            })

    elif command == "문의하기":
        return JsonResponse({
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "basicCard": {
          "title": "문의하기",
          "description": "문희는 베프팅이 좋은데",
          "thumbnail": {
            "imageUrl": "https://cdn.clien.net/web/api/file/F03/8892457/3402e4fb5e03e7.jpg?w=500&h=1000&gif=true"
          },
          "profile": {
            "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4BJ9LU4Ikr_EvZLmijfcjzQKMRCJ2bO3A8SVKNuQ78zu2KOqM",
            "nickname": "보물상자"
          },

          "buttons": [
            {
              "action": "webLink",
              "label": "개발자 오픈카톡 열기",
              "webLinkUrl": "https://open.kakao.com/o/sOa7wlmc"
            },
          ]
        }
      }
    ],
    'quickReplies': button.simpleTextquickReplies
  }
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

    elif value == 'addmissionYear':
        isTrue = bool(re.match('^20\d\d$', command))

    elif value == 'phoneNumber':
        isTrue = bool(re.match('^010\d{8}$', command))

    elif value == 'gender':
        isTrue = bool(re.match('^(남|여)$', command))

    elif value == 'cancel':
        isTrue = bool(re.match('^(네|아니요)$',command))

    elif value == 'interest1':
        interest1 = ["영화", "음악", "게임", "넷플릭스(TV)", "여행", "술", "스타일링(옷,화장)", "요리(음식)","스포츠", "카페","운동","학교주변"]
        isTrue = False
        for i in interest1:
            if (i == command):
                isTrue = True
                break
        if not isTrue:
            text ="""목록을 정확히 입력해주세요
ex ) 스타일링 X , 스타일링(옷,화장) O
-------------
영화
음악
게임
넷플릭스(TV)
여행
술
스타일링(옷,화장)
요리(음식)
스포츠
카페
운동
학교주변
-----------
"""
            return JsonResponse({
            "status": "FAIL",
            "message" : text})
    elif value == "interest2":
        interest2 = ["영화", "음악", "게임", "넷플릭스(TV)", "여행", "술", "스타일링(옷,화장)", "요리(음식)","스포츠", "카페","운동","학교주변","없음"]
        isTrue = False
        for i in interest2:
            if (i == command):
                isTrue = True
                break
        if not isTrue:
            text ="""목록을 정확히 입력해주세요
ex ) 스타일링 X , 스타일링(옷,화장) O
-------------
영화
음악
게임
넷플릭스(TV)
여행
술
스타일링(옷,화장)
요리(음식)
스포츠
카페
운동
학교주변
없음
-----------
"""
            return JsonResponse({
            "status": "FAIL",
            "message" : text})

    elif value == 'subject':
        subject = """ICT로봇공학전공
ICT로봇기계공학부
건설환경공학부
건축공학전공
경영학전공
공공행정전공
기계공학전공
동물생명융합학부
동물자원과학전공
디자인건축융합학부
디자인전공
문예창작미디어콘텐츠홍보전공
법경영학부
법학전공
사회안전시스템공학부
생명공학부
생물산업응용전공
소프트웨어&서비스컴퓨팅전공
소프트웨어융합전공
식물생명환경전공
식품생명공학전공
식품생명화학공학부
식품영양학전공
아동가족복지학전공
안전시스템공학전공
영미언어문화전공
원예생명공학전공
웰니스산업융합학부
웰니스스포츠과학전공
응용생명공학전공
응용수학전공
응용자원환경학부
의류산업학전공
인문융합공공인재학부
전기공학전공
전자공학전공
전자전기공학부
조경학전공
지역시스템공학전공
컴퓨터응용수학부
토목공학전공
화학공학전공
환경공학전공"""
        subjects = subject.split()
        isSubject = False
        for i in subjects:
            if i.strip() == command:
                isSubject = True
                break

        if isSubject:
            return JsonResponse({
            "status": "SUCCESS"})


        text = """전공 이름을 정확히 입력해주세요
과가 있으시면 과를 우선으로, 없으면 학부로 선택해주세요
ICT로봇공학전공 및 ICT로봇기계공학부는 꼭 it 대문자로 입력!
소프트웨어&서비스컴퓨팅전공 는 &를 꼭 입력해주세요.
==전공목록(ㄱ 순)==
%s
"""%subject

        return JsonResponse({
        "status": "FAIL",
        "message" : text})


    if isTrue:
        return JsonResponse({
        "status": "SUCCESS"})
    return JsonResponse({"status": "FAIL",
    'quickReplies': [{
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]})
