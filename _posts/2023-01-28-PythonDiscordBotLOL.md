---
title: RIOT API를 사용해서 디스코드 봇에 롤/롤체 전적검색 명렁어 추가하기
author: gksdygks2124
date: 2023-01-25 22:17:00 +0900
categories: [Python, Discord Bot]
tags: [RIOT API, 롤전적검색, 디스코드 봇, TFT전적검색, discord.py]
lastmode: 2023-01-25 22:17:00
sitemap:
  changefreq: daily
  priority : 1.0
---
> Reference1: <a>https://developer.riotgames.com/apis</a>  
> Reference2: <a>https://developer.riotgames.com/docs/portal</a>  
> Reference3: <a>https://developer.riotgames.com/docs/lol</a>  
{: .prompt-tip }

## <b>RIOT API 사용하기</b>
우선 <a href="https://developer.riotgames.com/">라이엇 개발자 사이트</a>에 로그인을 해서 API를 사용하기 위한 키를 받아야할 뿐만 아니라, 개발에 있어서 중요한 Documents까지 읽어볼 수 있다. 로그인을 하고나면 비영구/영구적 API KEY를 받을 수 있다. 비영구적 API KEY는 24시간의 유효성을 갖고 있으며, 영구적 API KEY를 받기 위해서는 <span style="color:red">REGISTER PRODUCT</span>를 통해 자신이 키를 사용하기 위한 목적을 RIOT에 제출을 해야한다. (번거로울 뿐이지, 쉽게 허가해준다)

<br>

### <b>JSON</b>
RIOT API로부터 받는 모든 데이터들은 JSON형태로 받는다. JSON을 모른다고 걱정할 필요가 없다. 서버와 클라이언트가 통신할 때 오고가는 복잡한 대량의 데이터들을 가독성 향샹을 위해 특정 형식을 갖춰서 정리하는 방식이다. 대표적으로 JSON, 그 외에 CSV, XML과 YAML이 있다.

JSON의 데이터 저장방식은 Object라고 불리는 {} 안에&nbsp; ```key: value```형태로 저장한다. value에는 문자열, 정수, 배열 등 다양한 자료형이 저장될 수 있다.
```JSON
{
    "name": "John"
    "age": 23,
    "married": false
}
```
<br>

#### <b>Python Json라이브러리로 JSON관리하기</b>
- JSON Encoding: <span style="color:#cbac69">json.dumps()</span>  
파이썬 객체를 직렬화된 <b>json 문자열</b>로 변환합니다.  

```python
import json

json_encoding = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
print(json_encoding)        # ["foo", {"bar": ["baz", null, 1.0, 2]}]
print(type(json_encoding))  # <class 'str'>
```

<br>

- JSON Decoding: <span style="color:#cbac69">json.loads()</span>  
json 문자열을 파싱해서 파이썬 객체로 변환시킵니다.  

```python
import json

json_encoding = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
json_decoding = json.loads(json_encoding)
print(json_decoding)        # ["foo", {"bar": ["baz", null, 1.0, 2]}]
print(type(json_decoding))  # <class 'list'>
```

<br>

#### <b>dump()와 dumps, load()와 loads() 차이</b>
- dump()는 파이썬 객체를 스트림 객체로 변환, dumps()는 json 문자열로 변환.
- load()는 스트림 객체를 파이썬 객체로 변환, loads()는 json 문자열을 파이썬 객체로 변환.

<br>

### <b>소환사 기본 정보 가져오기</b>

#### <b>STEP1. RIOT DEVELOPER > APIS > SUMMONER-V4 > Get a summoner by summoner name.(3번째) 선택</b>
소환사의 닉네임을 통해 소환사 정보를 얻을 것이니까 위와 같이 선택.
<img width="944" alt="Screenshot 2023-02-13 at 3 33 38 PM" src="https://user-images.githubusercontent.com/92556048/218392833-4278cf6c-8f78-4762-8bbb-baec1fe45da6.png">

#### <b>STEP2. PATH PARAMETERS 작성</b>
- summonerName: 소환사 닉네임
- SELECT REGION TO EXECUTE AGAINST: KR(한국서버)
- SELECT APP TO EXECUTE AGAUNST: 우선 Development API KEY 선택
- INCLUDE API KEY: Header Param
  - Query Param: 웹에서 디버깅에 좋다. 그렇지만 API_KEY가 URL에 그대로 노출 된다.
  - Header Param: API_KEY 값이 REQUEST HEADERS에 숨겨진다.
<img width="580" alt="Screenshot 2023-02-13 at 3 35 37 PM" src="https://user-images.githubusercontent.com/92556048/218392849-ba31d704-f077-4485-8501-ae059fdcb1a4.png">

#### <b>STEP3: RESPONSE 확인하기</b>
- 소환사 정보를 요청할 API URL 주소와 요청자(나)의 정보 전달
<img width="577" alt="Screenshot 2023-02-13 at 3 35 58 PM" src="https://user-images.githubusercontent.com/92556048/218392876-e5df6b2f-dcb7-414d-8e6d-518b8da04282.png">
- RESPONSE BODY(JSON)
여기서 Error가 발생하면 status_code를 참조해야한다. 여기서 우리에게 필요한 정보는 `id`, `name`, `profileIconId`와 `summonerLevel`이다.
<img width="578" alt="Screenshot 2023-02-13 at 3 37 01 PM" src="https://user-images.githubusercontent.com/92556048/218392893-b3af3548-0383-4c54-9222-e7b73e5b5773.png">

#### <b>STEP4: 코드로 옮기기</b>
우선 API_KEY를 Query, Header 2가지 방식 중에 Header 방식으로 진행할 것이다.
```python
import requests # Web API에 headers를 전달하여 정보를 요청하기 위해
import json # JSON을 다루기 위해

RIOT_API_KET = "INPUT_YOUR_API_KEY"

# 유저 닉네임과 API_KEY를 인자로 받는다
def search_lol_userInfo(arg, RIOT_TOKEN):
    # 위의 사진에서 REQUEST URL부분을 그대로 가져온다. by-name/ 뒤에 부분에는 소환사 닉네임이 들어가야해서 지우고, 우리가 받아올 소환사 닉네임으로 대체한다.
    userInfoUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + arg
    # 위의 사진에서 REQUEST HEADERS부분을 보면 "X-Riot-Token"에 RIOT_API_KEY를 필요로 한다.
    result = requests.get(userInfoUrl, headers={"X-Riot-Token":RIOT_TOKEN})
    # 요청한 정보를 loads()를 통해 파이썬 객체로 디코딩
    result_json = json.loads(result.text)

    print(result) # <Response [200]>
    print(result_json) # {'id': 'QvUSIe3HICgbqiQkGgpskgdDI7vpE433Q9Sa4mWBjRGs-A', 'accountId': '359v-ZtEXQNNmDFydtXurKqD2TeIPHN56r5-lV95w1zj', 'puuid': 'p9rIFJISvcNMfA7fyoIkh8Tw5j2lrQnC2LO-py9k2140K6RwSMFPpxuhooUwk_l36qV8MubPys1v-Q', 'name': 'Hide on bush', 'profileIconId': 6, 'revisionDate': 1676271384091, 'summonerLevel': 630}

    # 소환사 검색에 성공했을 경우
    if result.status_code == 200:
        print(result_json['id']) # QvUSIe3HICgbqiQkGgpskgdDI7vpE433Q9Sa4mWBjRGs-A
        print(result_json['name']) # Hide on bush
        print(result_json['profileIconId']) # 6
        print(result_json['summonerLevel']) # 630
    else:
        print("존재하지 않는 소환사명입니다.\n다시 한번 확인해주세요.")

search_lol_userInfo("Hide on bush", RIOT_API_KET)
```

<br>
<br>

### <b>소환사 전적 가져오기</b>
#### <b>STEP1</b>
소환사 전적 또한 위와 동일한 방법으로 진행하면 된다. 여기서 Get league entries in all queues for a given summoner ID(2번째) 선택
<img width="1105" alt="Screenshot 2023-02-13 at 3 54 49 PM" src="https://user-images.githubusercontent.com/92556048/218392898-e42d619d-06ba-4487-adf9-c8e9d82b8414.png">

#### <b>STEP2</b>
encryptedSummonerId를 인자로 필요로 한다. 이때 이 값은 위에 소환사 정보에서 가져온 `result_json['id']`을 넣어주면 된다.
<img width="737" alt="Screenshot 2023-02-13 at 3 55 40 PM" src="https://user-images.githubusercontent.com/92556048/218392906-fe8aca99-f393-40ab-94f0-a1e397367c3c.png">

#### <b>STEP3</b>
<img width="737" alt="Screenshot 2023-02-13 at 3 59 00 PM" src="https://user-images.githubusercontent.com/92556048/218392930-6043b3fe-b7c5-417b-9b6b-1f4555effda2.png">
<img width="736" alt="Screenshot 2023-02-13 at 3 59 16 PM" src="https://user-images.githubusercontent.com/92556048/218392943-0110c108-5b55-496c-9f70-f2972ec77356.png">

#### <b>STEP4</b>
```python
import requests
import json

RIOT_API_KET ="INPUT_YOUR_KEY"

def search_lol_userInfo(arg, RIOT_TOKEN):
    userInfoUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + arg
    result = requests.get(userInfoUrl, headers={"X-Riot-Token":RIOT_TOKEN})
    result_json = json.loads(result.text)

    if result.status_code == 200:
        print(result_json['id'])
        print(result_json['name'])
        print(result_json['profileIconId'])
        print(result_json['summonerLevel'])

        # ====================== 소환사 전적 가져오기 (added) ====================== 
        userRankInfo = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + result_json["id"]
        resultRank = requests.get(userRankInfo, headers={"X-Riot-Token":RIOT_TOKEN})
        resultRank_json = json.loads(resultRank.text)

        # Unranked
        if resultRank_json == []:
            print("언랭크 유저입니다.")
        # Ranked Solo / Flexed
        else:
            for rank in resultRank_json:
                # Solo Rank
                if rank["queueType"] == "RANKED_SOLO_5x5":
                    print("Solo Queue")
                    print(rank['tier']) # GRANDMASTER
                    print(rank['rank']) # I
                    print(rank['leaguePoints']) # 427
                    print(rank['wins']) # 76
                    print(rank['losses']) # 62
                # Flex Rank
                else:
                    print("Flex Queue")
                    print(rank['tier'])
                    print(rank['rank'])
                    print(rank['leaguePoints'])
                    print(rank['wins'])
                    print(rank['losses'])

    else:
        print("존재하지 않는 소환사명입니다.\n다시 한번 확인해주세요.")

search_lol_userInfo("Hide on bush", RIOT_API_KET)
```

<br>

## <b>Discord에 Embed로 결과 출력하기</b>
### <b>main.py</b>
나는 main.py는 최대한 깔끔하게 작성하는 걸 좋아해서, `search_lol_userInfo()`를 main.py외부 py파일에 작성하고 import를 해서 사용했다.

```python
from lib.search_lol_userInfo import search_lol_userInfo

'''
중간 코드 생략
'''

@bot.command(name="롤전적검색")
async def search_lol(ctx, arg):
  await ctx.send(embed = search_lol_userInfo(arg))
```

<br>

### <b>search_lol_userInfo.py</b>
```python
import requests
import json
import discord

RIOT_API_KET ="INPUT_YOUR_KEY"

def search_lol_userInfo(arg, RIOT_TOKEN):
    userInfoUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + arg
    result = requests.get(userInfoUrl, headers={"X-Riot-Token":RIOT_TOKEN})
    result_json = json.loads(result.text)

    if result.status_code == 200:
        userIconUrl = "http://ddragon.leagueoflegends.com/cdn/11.3.1/img/profileicon/{}.png"
        # Embed Head (*required)
        embed = discord.Embed(title=f"소환사 {result_json['name']}님의 정보", description=f"**{result_json['summonerLevel']} LEVEL**", color=0xAEE3D4)

        userRankInfo = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + result_json["id"]
        resultRank = requests.get(userRankInfo, headers={"X-Riot-Token":RIOT_TOKEN})
        resultRank_json = json.loads(resultRank.text)

        if resultRank_json == []:
            # Embed Body
            embed.add_field(name=f"해당 유저는 언랭크입니다.", value="**언랭크 유저의 정보는 출력하지 않습니다.**", inline=False)
        else:
            for rank in resultRank_json:
                if rank["queueType"] == "RANKED_SOLO_5x5":
                    embed.add_field(name="솔로랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                           f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)
                else:
                    embed.add_field(name="자유랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                            f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)
        # Embed Footer
        embed.set_author(name=result_json['name'], url=f"http://fow.kr/find/{arg.replace(' ', '')}", icon_url=userIconUrl.format(result_json['profileIconId']))
        return embed
    else:
        error = discord.Embed(title="오류가 발생했습니다.", description="소환사 이름이 존재하지 않거나, 통신에 오류가 있습니다.", color=0xEF5A68)
        return error
       

search_lol_userInfo("Hide on bush", RIOT_API_KET)
```

<br>
결과화면
<img width="253" alt="Screenshot 2023-02-13 at 7 27 02 PM" src="https://user-images.githubusercontent.com/92556048/218434828-f8a0a576-934b-4466-a5ce-3229795f94a5.png">

<br>
<br>
<br>

RIOT API를 사용하는 다른 기능도 같은 방법으로 다 할 수 있다.
