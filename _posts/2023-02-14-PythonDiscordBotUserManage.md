---
title: 디스코드 봇에 유저 회원가입 기능 추가하기
author: gksdygks2124
date: 2023-02-13 09:14:00 +0900
categories: [Python]
tags: [python decorator, decorator, 파이썬 데코레이터]
lastmode: 2023-02-13 09:14:00
sitemap:
  changefreq: daily
  priority : 1.0
---
> 참고한 공식문서  
> https://firebase.google.com/docs/firestore/query-data/get-data?hl=ko
{: .prompt-tip }

<br>
<br>

## <b>Google Firebase 사용하기</b>
<a href="https://console.firebase.google.com/?hl=ko">구글 파이어베이스 콘솔 페이지</a>에 접속하여 새로운 Firebase프로젝트를 생성하거나 추가해야한다. 프로젝트 생성(혹은 추가) 후에 작업은 아래와 같다.
- 프로젝트 이름 설정: 본인이 원하는 이름 혹은 디스코드 봇 이름을 사용해도 된다.
- Firebase 프로젝트를 위한 Google 애널리틱스: 해도 안 해도 상관 없다. 대신 사용 선택을 하면 'Google 애널리틱스 구성' 계정을 선택해야한다.

<br>

1. 프로젝트를 생성하고나면 콘솔페이지로 넘어갈 수 있다. 프로젝트 페이지 왼쪽에 사이드바에서 Firestore Database를 클릭해서 DB를 생성한다.
<br>
<img width="244" alt="Screenshot 2023-02-14 at 9 24 54 AM" src="https://user-images.githubusercontent.com/92556048/218607051-bc709700-b1ac-4bd7-9230-ef2f46ecdf71.png">

<br>

2. 프로덕션 모드 선택
<br>
<img width="813" alt="Screenshot 2023-02-14 at 9 25 19 AM" src="https://user-images.githubusercontent.com/92556048/218607057-310d24fa-fc60-4d66-a876-38a39b95e92a.png">

<br>

3. Cloud Firestore위치 설정
<br>
<img width="807" alt="Screenshot 2023-02-14 at 9 25 46 AM" src="https://user-images.githubusercontent.com/92556048/218607064-3821f558-6fa9-4825-b2ed-1d809b5014ef.png">

<br>

4. Cloud Firesotre위치 설정에서 오류 발생한 경우  
콘솔에서 톱니바퀴 버튼 클릭 후 프로젝트 설정 > 일반 > 기본 GCP 리로스 위치를 업데이트 후에 다시 하면 된다.
<img width="599" alt="Screenshot 2023-02-14 at 9 27 44 AM" src="https://user-images.githubusercontent.com/92556048/218607113-3989ea02-076d-45df-b463-cda7dd2d25b6.png">

<br>

5. Cloud Firestore > 규칙 코드 수정하기 (<a href="https://firebase.google.com/docs/rules/rules-language?hl=ko">공식사이트</a>)
```json
// 이 코드는 보안상의 취약점이 존재합니다. 만약 보안을 중요시 여겨야 한는 대형 서버에서 사용할 DB라면 따로 코드를 작성해야합니다.
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write if true;
    }
  }
}
```

<br>

6. 프로젝트 설정 > 서비스 계정 > Firebase Admin SDK > Admin SDK 구성 스니펫: Python 선택 > 새 비공개 키 생성(JSON이 설치 됨)
<img width="1062" alt="Screenshot 2023-02-14 at 9 28 18 AM" src="https://user-images.githubusercontent.com/92556048/218607119-8e10b08c-d8e2-475d-8bc1-de607ac5e8d5.png">

<br>

7. Google Firestore Initializing > 설치된 JSON파일을 Python 프로젝트 폴더로 이동 후 import
```python
import firebase_admin
from firebase_admin import credentials

# ./json/ => 절대경로(최상위 디렉토리에 위치한 json 디렉토리
# discordbot-firebase-adminsdk-mn0p0-xxxxxxxxxx.json => 설치된 JSON 파일 이름과 확장자
cred = credentials.Certificate("./json/discordbot-firebase-adminsdk-mn0p0-xxxxxxxxxx.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
```
이 단계까지 끝나면 Python에서 Firestore에 접근할 준비가 끝났다.

<br>
<br>

## <b>Python에서 Google Firebase 접근하기</b>
### <b>Google Firebase DB 구조</b>
ss
<img width="669" alt="Screenshot 2023-02-14 at 10 15 33 AM" src="https://user-images.githubusercontent.com/92556048/218613102-d235b950-5be5-44aa-b305-195756f46d6d.png">

<br>

### <b>user.py</b>
```python
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./json/discordbot-firebase-adminsdk-mn0p0-xxxxxxxxxx.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

#=========================Account==================================
# 회원가입을 할 경우 중복가입을 막기 위해 존재하는 유저인지 확인
def checkUserExist(_name, _id):
    print("user.py - checkUser()")
    # DB에 없는 유저는 NameError가 발생합니다
    try:
        # db에서 _name(디스코드 닉네임)과 일치하는 항목이 있는지 확인
        find_user = db.collection(u'users').document(_name)
        # 디스코드에서는 닉네임이 같을 수 있다. 그렇지만 이런 경우 개인의 고유 id를 통해 다른 유저임을 식별한다.
        # 따라서 디스코드 닉네임은 같을 때, id비교를 안 하면 오류가 발생하기 때문에 닉네임은 갖고, id는 다른 서로 다른 유저의 회원가입을 진행하기 위한 코드
        if _id == find_user.get().to_dict()['id']:
            return True
        else:
            return False
    except:
        return False

def signUp(_name, _id):
    print("user.py - signUp()")
    if checkUserExist(_name,_id):
        message = "이미 가입된 유저입니다"
        return message
    else: 
        doc_ref = db.collection(u'users').document(_name)
        doc_ref.set({
            u'id' : _id,
            u'money' : 30000000,
            u'loss' : 0,
            u'level' : 0,
            u'exp' : 0,
            # foreignCurrency
            u'dollar' : 0,
            u'yen' : 0,
            u'yuan' : 0,
            u'euro' : 0,
            u'pound' : 0,
            u'real' : 0,
            u'ruble' : 0,
            u'rupee' : 0,
            # coin
            u'waves' : 0,
            u'btc' : 0,
            u'eth' : 0,
            u'doge' : 0,
            u'ltc' : 0,
            u'etc' : 0,
            u'lunc' : 0,
            u'sand' : 0,
            u'bnb' : 0,
            u'xrp' : 0,
            # item
            u'bait' : 0,
            u'graps' : 0,
            u'wisky' : 0,
            u'vitamin' : 0,
            u'bk' : 0,
            u'kc' : 0,
            u'rkc' : 0,
            u'ostrich' : 0
            })
        message = "회원가입 성공, 환영합니다."
        return message
```

<br>

### <b>main.py</b>
```python
from lib.user_manage import *

'''
나머지 코드는 생략
'''

@bot.command()
async def 회원가입(ctx):
  message = signUp(ctx.author.name, ctx.author.id)
  await ctx.send(message)
```
