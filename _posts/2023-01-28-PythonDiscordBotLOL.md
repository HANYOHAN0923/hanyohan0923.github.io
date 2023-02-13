---
title: RIOT API를 사용해서 디스코드 봇에 롤/롤체 전적검색 명렁어 추가하기
author: gksdygks2124
date: 2023-01-25 22:17:00 +0900
categories: [Python, Discord Bot]
tags: [RIOT API, 롤전적검색, 디스코드 봇, TFT전적검색]
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
<img width="944" alt="Screenshot 2023-02-13 at 3 33 38 PM" src="https://user-images.githubusercontent.com/92556048/218392833-4278cf6c-8f78-4762-8bbb-baec1fe45da6.png">
<img width="580" alt="Screenshot 2023-02-13 at 3 35 37 PM" src="https://user-images.githubusercontent.com/92556048/218392849-ba31d704-f077-4485-8501-ae059fdcb1a4.png">
<img width="577" alt="Screenshot 2023-02-13 at 3 35 58 PM" src="https://user-images.githubusercontent.com/92556048/218392876-e5df6b2f-dcb7-414d-8e6d-518b8da04282.png">
<img width="578" alt="Screenshot 2023-02-13 at 3 37 01 PM" src="https://user-images.githubusercontent.com/92556048/218392893-b3af3548-0383-4c54-9222-e7b73e5b5773.png">
<img width="1105" alt="Screenshot 2023-02-13 at 3 54 49 PM" src="https://user-images.githubusercontent.com/92556048/218392898-e42d619d-06ba-4487-adf9-c8e9d82b8414.png">
<img width="737" alt="Screenshot 2023-02-13 at 3 55 40 PM" src="https://user-images.githubusercontent.com/92556048/218392906-fe8aca99-f393-40ab-94f0-a1e397367c3c.png">
<img width="737" alt="Screenshot 2023-02-13 at 3 59 00 PM" src="https://user-images.githubusercontent.com/92556048/218392930-6043b3fe-b7c5-417b-9b6b-1f4555effda2.png">
<img width="736" alt="Screenshot 2023-02-13 at 3 59 16 PM" src="https://user-images.githubusercontent.com/92556048/218392943-0110c108-5b55-496c-9f70-f2972ec77356.png">


