---
title: discord.py 라이브러리로 디스코드 봇 만들기
author: gksdygks2124
date: 2023-01-25 14:55:00 +0900
categories: [Python, Discord Bot]
tags: [discord.py, 디스코드 봇]
lastmode: 2023-01-25 14:55:00
sitemap:
  changefreq: daily
  priority : 1.0
---
## <b>프로젝트 계획</b>
디스코드 서버에서 유저들의 교류 및 활동을 더 활발하게 하고, 편의성을 제공하기 위해서 디스코드 내부에 명령어를 수행하는 봇을 제작.  
<br>
<br>

## <b>기능</b>
- LOL / TFT 전적검색
- LOL 챔피언 정보(스팩, 룬, 빌드...) 검색
- 디스코드 내에 미니 RPG 게임 서비스 제공(레벨, 코인, 낚시, 도박 등 다양한 콘텐츠 제공)
- 추후 다른 컨텐츠도 업데이트 예정...
<br>
<br>

## <b>STEP1. 코드 실행 환경</b>
우선 디스코드 봇을 만들면, 24시간 코드를 실행시켜줄 수 있는 방법을 찾아야한다. 

<br>
<br>

## <b>STEP2. DataBase</b>
라이엇에 관련된 정보를 제공하는 기능과 달리 디스코드 서버 내부 자체 미니 RPG 게임을 서비스 제공하기 위해서는 디스코드 서버 내에서 미니 RPG 게임에 새롭게 참여하는 유저들의 정보와 플레이 중인 유저들의 정보를 기록하고, 수정하고, 삭제하는 작업을 필요로 한다. 따라서 이러한 정보들을 기록 또는 저장할 수 있는 공간이 필요하다. 여기서 크게 두가지 방법이 있다.  
<br>

### <b>1) Excel</b>
openpyxl(파이썬 외장 라이브러리)를 사용해서, 데이터를 엑셀에 기록을 하는 방법이다. 대중적인 DB들과 다르게 비교적 더 간단하게 구현이 가능하지만, 코드를 관리하는 서버(나의 PC)와 코드를 24시간 실행하는 호스팅 서버 간의 데이터가 동시에 기록이 안된다는 단점이 있다. 즉 코드를 24시간 실행하는 호스팅 서버의 엑셀 파일에서는 실시간으로 유저 정보들이 기록이 되는 반면, 내 컴퓨터에서는 안 되기 때문에 코드를 보수하거나 업데이트할 경우, 매번 서버에서 코드 실행 중지를 하고, GitGub 원격 저장소로 엑셀의 변경 사항을 push한 다음, 코드 수정과 업데이트가 끝날 때까지 봇이 서버에서 죽어있어야한 다는 단점이 있다.
<br>

### <b>2) Google Firebase</b>
구글에서 제공하는 No-SQL DB이다. 대중적인 오라클과 같은 DB는 유료이면서, 어렵진 않지만 SQL을 할 줄 알아야한다. 그렇지만 구글에서 제공하는 Firebase DB는 SQL이 필요 없이 GUI로 해결이 가능한 동시에, 일정 사용량 안에서는 무료라는 큰 장점이 있다. 내가 만드는 봇이 대형디스코드채널에서 사용될 것도 아니고, 20명 정도가 사용하는 디스코드채널이기 때문에 무료형 프로모션으로도 충분히 진행 가능했다. 아무래도 No-SQL이 가져오는 몇개의 단점이 존재하지만, 장점이 더 뚜렷했다.

<br>
<br>
<br>

## <b>main.py 기본 코드 구조</b>
<br>

아래 코드는 main.py, 즉 서버에서 24시간 실행할 코드들의 메인 파일이다. 실제 이 main.py에 작성된 코드는 이것보다 길지만 일단 구조를 설명하기 위해 짧게 생략하였다. main.py의 구조는 크게 5부분으로 나눌 수 있다.
```python
import discord.ext import commands
import discord
import tomllib


#Custom Python LiBrary
from lib.search_lol_userInfo import search_lol_userInfo
from lib.search_tft_userInfo import search_tft_userInfo


with open("config.toml", mode="rb") as file:
    data = tomllib.load(file)

    DISCORD_TOKEN = data["DISCORD_API_KEY"]["DISCORD_TOKEN"]
    RIOT_LOL_TOKEN = data["RIOT_API_KEY"]["RIOT_LOL_TOKEN"]
    RIOT_TFT_TOKEN = data["RIOT_API_KEY"]["RIOT_TFT_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} online!')


# ================== Commands ==================
@bot.command(name = '롤전적검색')
async def cmd6(ctx, arg):
    await ctx.send(embed = search_lol_userInfo(arg, RIOT_LOL_TOKEN))

@bot.command(name = "롤체전적검색")
async def cmd7(ctx, arg):
    await ctx.send(embed = search_tft_userInfo(arg, RIOT_TFT_TOKEN))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass


bot.run(DISCORD_TOKEN)
```
<br>

1) <span style="color:purple">import</span>(line1~8): 이 부분의 코드도 디스코드 라이브러리(디스코드 서버와 관련된 모든 작업을 담당)와 커스텀 라이브러리(디스코드를 통해 명령어 호출시 파이썬에서 수행되는 작업을 담당) 두 부분으로 나눌 수 있다.

<br>

2) <span style="color:purple">with</span>(line11~16): 이 부분은 디스코드 봇을 만들 때 사용된 API_KEY들이 있는데, 이것을 GitHub에 그대로 올리면 안 된다. 따라서 위에서 import한 tomllib 외장 라이브러리로 config.toml에 API_KEY를 담고, .gitignore에 해당 파일을 등록하는 형식으로 외부에 API_KEY를 노출하는 것을 방지하는 코드이다. &nbsp; ```var = data['TAG_NAME']['KEY_NAME']```형태로 config.toml파일에서 키값을 불러올 수 있다.
```toml
# config.toml 작성하는 방법
[tag_name]
key_name = 'value'

# Example(가짜 키값입니다)
[RIOT_API_KEY]
RIOT_TFT_TOKEN = "RGAPI-0a53azz5-9a8u-4x7f-882f-9464109ad52x"
```
<br>

3) <span style="color:purple">intent</span>(line19~21): discord.dev에서 설정한 디스코드 봇의 <a href="https://discordpy-ko.github.io/intents.html">intent</a>(기본적으로 봇이 특정 버킷이나 이벤트를 받도록 해주는 기능)와 상호작용 하는 코드
    - 여기서 사용되는 매개변수가 있는 <span style="color:skyblue">@데코레이터</span>에 관한 설명은 <a href="https://dojang.io/mod/page/view.php?id=2429">링크</a>를 참조

<br>

4) <span style="color:skyblue">@bot_event</span>(line24~26, line44): 봇 토큰을 토대로 봇을 최종적으로 실행하는 코드(last line), 봇이 정상적으로 실행되면 실행되는 코드(여기서는 콘솔에 print하는 코드를 작성했지만, 다른 작업을 해도 된다)
    - 여기서 사용되는 <span style="color:skyblue">@데코레이터</span>에 관한 설명은 <a href="https://hanyohan0923.github.io/posts/PythonDecorator/">링크</a>를 참조

<br>

5) <span style="color:green"># Commands</span>(주석부분): 디스코드 텍스트 채팅 채널에서 특정 명렁어를 감지했을 때 수행하는 작업을 담당하는 코드
