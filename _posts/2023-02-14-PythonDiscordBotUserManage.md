---
title: 디스코드 봇에 유저 회원가입 기능 추가하기
author: gksdygks2124
date: 2023-02-13 09:14:00 +0900
categories: [Python, Discord Bot]
tags: [discord.py, 디스코드 봇, 디스코드 봇 회원가입, 디스코드 봇 유저]
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

# <b>Google Firebase 사용하기</b>
<a href="https://console.firebase.google.com/?hl=ko">구글 파이어베이스 콘솔 페이지</a>에 접속하여 새로운 Firebase프로젝트를 생성하거나 추가해야한다. 프로젝트 생성(혹은 추가) 후에 작업은 아래와 같다.
- 프로젝트 이름 설정: 본인이 원하는 이름 혹은 디스코드 봇 이름을 사용해도 된다.
- Firebase 프로젝트를 위한 Google 애널리틱스: 해도 안 해도 상관 없다. 대신 사용 선택을 하면 'Google 애널리틱스 구성' 계정을 선택해야한다.

<br>

STEP1. 프로젝트를 생성하고나면 콘솔페이지로 넘어갈 수 있다. 프로젝트 페이지 왼쪽에 사이드바에서 Firestore Database를 클릭해서 DB를 생성한다.
<br>
<img width="244" alt="Screenshot 2023-02-14 at 9 24 54 AM" src="https://user-images.githubusercontent.com/92556048/218607051-bc709700-b1ac-4bd7-9230-ef2f46ecdf71.png">

<br>

STEP2. 프로덕션 모드 선택
<br>
<img width="813" alt="Screenshot 2023-02-14 at 9 25 19 AM" src="https://user-images.githubusercontent.com/92556048/218607057-310d24fa-fc60-4d66-a876-38a39b95e92a.png">

<br>

STEP3. Cloud Firestore위치 설정
<br>
<img width="807" alt="Screenshot 2023-02-14 at 9 25 46 AM" src="https://user-images.githubusercontent.com/92556048/218607064-3821f558-6fa9-4825-b2ed-1d809b5014ef.png">

<br>

STEP4. Cloud Firesotre위치 설정에서 오류 발생한 경우  
콘솔에서 톱니바퀴 버튼 클릭 후 프로젝트 설정 > 일반 > 기본 GCP 리로스 위치를 업데이트 후에 다시 하면 된다.
<img width="599" alt="Screenshot 2023-02-14 at 9 27 44 AM" src="https://user-images.githubusercontent.com/92556048/218607113-3989ea02-076d-45df-b463-cda7dd2d25b6.png">

<br>

STEP5. Cloud Firestore > 규칙 코드 수정하기 (<a href="https://firebase.google.com/docs/rules/rules-language?hl=ko">공식사이트</a>)
```shell
# 이 코드는 보안상의 취약점이 존재합니다. 만약 보안을 중요시 여겨야 한는 대형 서버에서 사용할 DB라면 따로 코드를 작성해야합니다.
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

STEP6. 프로젝트 설정 > 서비스 계정 > Firebase Admin SDK > Admin SDK 구성 스니펫: Python 선택 > 새 비공개 키 생성(JSON이 설치 됨)
<img width="1062" alt="Screenshot 2023-02-14 at 9 28 18 AM" src="https://user-images.githubusercontent.com/92556048/218607119-8e10b08c-d8e2-475d-8bc1-de607ac5e8d5.png">

<br>

STEP7. Google Firestore Initializing > 설치된 JSON파일을 Python 프로젝트 폴더로 이동 후 import  

<br>

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

# <b>Python에서 Google Firebase 접근하기</b>
## <b>Google Firebase DB 구조</b>
아래 사진과 user.py코드를 같이 보면 더 쉽게 이해할 수 있다.
Collection(users)는 여러 개의 Document(Bajirak Karlcux, John Han, Movin_Gun)을 갖고 있고, 각 Document는 여러 개의 필드 값을 갖을 수 있다. 필드 값은 정수, 실수, 배열, 객체, 문자열, 불리언 다양한 값을 값으로 갖을 수 있다. JSON을 직관화해서 보는 것이라고 생각할 수 있다.  

<img width="669" alt="Screenshot 2023-02-14 at 10 15 33 AM" src="https://user-images.githubusercontent.com/92556048/218613102-d235b950-5be5-44aa-b305-195756f46d6d.png">

<br>

## <b>회원가입 기능 구현하기</b>
### <b>user.py</b>
- `db.collection(u'collectionName').document(u'documentName')`로 컬렉션과 문서에 접근할 수 있다.
- `.get().to_dict()['key']`로 단일 문서의 필드를 딕셔너리 객체로 반환 후, 키를 통해 필드 값을 읽을 수 있다.
- `exists`는 db.collection('colName').document(u'docName')가 참조하는 위치에 문서가 없으면 false, 있으면 true를 반환한다. (아래 예제 코드에서는 db.collection('colName').document(u'docName')는 find_user이다.)
- `.set({})`로 문서에 접근 후, 새로운 필드를 추가할 수 있다.  

<br>
 
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
    try:
        find_user_ref = db.collection(u'users').document(_name)
        find_user = find_user_ref.get()

        if find_user.exists:
            return True
         # 디스코드에서는 닉네임이 같을 수 있다. 그렇지만 이런 경우 개인의 고유 id를 통해 다른 유저임을 식별한다. 따라서 디스코드 닉네임은 같을 때, id비교를 안 하면 오류가 발생하기 때문에 닉네임은 갖고, id는 서로 다른 유저를 구별하해야한다
        elif _id == find_user.to_dict()['id']:
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

<br>
<br>

## <b>돈 기능 추가</b>
유저끼리 서로 돈을 송금하고, 자기 자신의 자신과 레벨을 확인할 수 있는 정보를 볼 수 있는 명령어(돈은 나중에 도박, 낚시, 코인, 아이템구매 등... 미니게임에 사용됩니다)
### <b>user.py</b>
기존에 있던 파일에 추가로 작성하면 됩니다.  

```python
# 유저 정보를 가져오는 함수
def userInfo(_name):
    user_info = db.collection(u'users').document(_name).get().to_dict()

    _lvl = user_info["level"]
    _exp = user_info["exp"]
    _money = user_info["money"]

    return _lvl, _exp, _money

# 현재 자산을 조회하는 함수
def getMoney(_name):
    result = db.collection(u'users').document(_name).get().to_dict()["money"]
    return result

# 돈을 수정하는 함수
def modifyMoney(_target, _amount):
    money = db.collection(u'users').document(_target).get().to_dict()["money"]
    db.collection(u'users').document(_target).update({u'money': money + _amount})

# 송금 기능 담당하는 함수
def remit(sender, receiver, _amount):
    modifyMoney(receiver,  int(_amount))
    modifyMoney(sender,  -int(_amount))
```

<br>

### <b>main.py</b>
기존에 있던 파일에 추가로 작성하면 됩니다.  

```python
@bot.command()
async def 내정보(ctx):
    userStatus = checkUserExist(ctx.author.name, ctx.author.id)

    if not userStatus:
        await ctx.send("회원가입 후 자신의 정보를 확인할 수 있습니다.")
    else:
        level, exp, money = userInfo(ctx.author.name)
        exp_amount_to_up = level*level + 6*level
        boxes = int(exp/exp_amount_to_up*20)
        embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x62D0F6)
        embed.add_field(name = ":crossed_swords: 레벨", value = level)
        embed.add_field(name = "XP: " + str(exp) + "/" + str(exp_amount_to_up), value = boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.add_field(name = "=========================보유 자산=========================", value="=======================================================", inline = False)
        embed.add_field(name = ":moneybag: 원화", value = format(int(money),','), inline = True)

        await ctx.send(embed=embed)

@bot.command()
async def 송금(ctx, user: discord.User, money):
    if int(money) <= 0:
        await ctx.send("송금 불가능 단위")
        return 0
        
    # 입금 대상, 출금 대상 유저가 존재하는 유저인지 확인
    senderStatus = checkUserExist(ctx.author.name, ctx.author.id)
    receiverStatus = checkUserExist(user.name, user.id)

    # 출금 대상이 없을 때
    if not senderStatus:
        await ctx.send("회원가입 후 송금이 가능합니다.")
    # 입금 대상이 없을 때
    elif not receiverStatus:
        await ctx.send(user.name  + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        s_money = getMoney(ctx.author.name) # 출금계좌 보유 원화 가져오기
        r_money = getMoney(user.name) # 송금계좌 보유 원화 가져오기

        if s_money >= int(money) and int(money) != 0:
            remit(ctx.author.name, user.name, money)

            embed = discord.Embed(title="송금 완료", description = "송금된 돈: " + money, color = 0x77ff00)
            embed.add_field(name = "보낸 사람: " + ctx.author.name, value = "현재 자산: " + str(format(int(getMoney(ctx.author.name)),',')))
            embed.add_field(name = "→", value = ":moneybag:")
            embed.add_field(name="받은 사람: " + user.name, value="현재 자산: " + str(format(int(getMoney(user.name)),',')))
                    
            await ctx.send(embed=embed)

        elif int(money) == 0:
            await ctx.send("0원은 송금 가능 금액이 아닙니다")
        # 출금계좌에 잔액이 부족한 경우
        else:
            await ctx.send("돈이 충분하지 않습니다. 현재 자산: " + str(s_money))

        print("------------------------------\n")
```

<br>
<br>

## <b>레벨 기능 구현하기</b>
경험치를 얻는 방법은 간단합니다. 디스코드 채팅 채널에서 명령어든 텍스트든 입력할 때마다
<br>

### <b>user.py</b>
기존에 있던 파일에 추가로 작성하면 됩니다.  

```python
# 유저가 레벨업 여부를 확인하고, 레벨업 조건 충족시 레벨업을 담당하는 함수
def levelUpCheck(_name):
    name = _name
    # Google Firebase(DB)로부터 유저의 경험치와 레벨 값 읽어오기
    exp = db.collection(u'users').document(_name).get().to_dict()["exp"]
    lvl = db.collection(u'users').document(_name).get().to_dict()["level"]

    # 레벨업시 요구되는 경험치 => 마인크래프트 0~16레벨업 공식입니다.
    exp_amount_to_up = lvl^2 + lvl*6

    # 레벨업 조건 충족 (경험치exp가 다음 레벨 요구 경험치exp_amount_to_up보다 큼)
    if exp >= exp_amount_to_up:
        # 경험치 획득량이 많아서 한번에 2레벨을 업할 수 있어서 반복문 사용
        while(exp >= exp_amount_to_up and exp >= 0):
            # DB level 값에 1을 더해서 업데이트
            db.collection(u'users').document(_name).update({u'level': lvl + 1})
            # DB exp 값에 레벨업을 위해 소모된 exp를 차감
            db.collection(u'users').document(_name).update({u'exp': exp - exp_amount_to_up})

            # Google Firebase(DB)로부터 반복문을 돌기 위해 유저의 변경된 경험치와 레벨 값 읽어오기
            exp = db.collection(u'users').document(_name).get().to_dict()["exp"]
            lvl = db.collection(u'users').document(_name).get().to_dict()["level"]
            # 레벨업을 해서 다음 레벨업에 요구되는 경험치 총량도 달라진다
            exp_amount_to_up = lvl*lvl + 6*lvl
        return True, lvl
    else:
        return False, lvl

# 유저가 채팅할 때마다 경험치를 주기 위한 텍스트
def modifyExp(_name, _amount):
    name = _name
    exp = db.collection(u'users').document(_name).get().to_dict()["exp"]
    db.collection(u'users').document(_name).update({u'exp': exp + _amount})
```

<br>

### <b>main.py</b>
기존에 있던 파일에 추가로 작성하면 됩니다.  

```python
from random import randint

@bot.event
async def on_message(message):
    # 채팅한게 유저가 아니고 봇일 경우 이벤트 종료
    if message.author == bot.user:
        return
    # 채팅한게 유저가 맞을 경우
    else:
        # 회원가입 안 한 디스코드 유저가 채팅했을 경우는 그대로 이벤트 종료
        userStatus = checkUserExist(message.author.name, message.author.id)
        channel = message.channel
        if userStatus:
            levelUp, lvl = levelUpCheck(message.author.name)
            if levelUp:
                # 레벨업 보상금 지급
                modifyMoney(message.author.name, int(lvl)*100000)
                # 레벨업 축하 임베드 작성
                embed = discord.Embed(title = "레벨업", description = None, color = 0x00A260)
                embed.set_footer(text = f"홀리 쉿~! {message.author.name} {str(lvl)} 레벨 달성!!!")
                await channel.send(embed=embed)
            else:
                # 채팅했을 때 1~10 exp를 랜덤으로 지급
                modifyExp(message.author.name, randint(1,10))

        await bot.process_commands(message)
```