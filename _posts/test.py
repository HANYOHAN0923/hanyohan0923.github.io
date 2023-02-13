import requests
import json

RIOT_API_KET = "RGAPI-424504cf-e316-45a5-bfec-7352e2dc8147"

def search_lol_userInfo(arg, RIOT_TOKEN):
    userInfoUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + arg
    res = requests.get(userInfoUrl, headers={"X-Riot-Token":RIOT_TOKEN})
    resjs = json.loads(res.text)
    print(resjs)

    if res.status_code == 200:
        UserIconUrl = "http://ddragon.leagueoflegends.com/cdn/11.3.1/img/profileicon/{}.png"
        title=f"플레이어 {resjs['name']} 님의 정보"
        description=f"**{resjs['summonerLevel']} LEVEL**"

        UserInfoUrl_2 = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + resjs["id"]
        res_2 = requests.get(UserInfoUrl_2, headers={"X-Riot-Token":RIOT_TOKEN})
        res_2js = json.loads(res_2.text)

        if res_2js == []: # User Unranked
            unranked = f"{resjs['name']} 님은 언랭크입니다. **언랭크 유저의 정보는 출력하지 않습니다.**"
            print(title)
            print(description)
            print(unranked)

        else: # User Ranked
            for rank in res_2js:
                if rank["queueType"] == "RANKED_SOLO_5x5":
                    solo = f"솔로랭크: **티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                    match = f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**"
                    print(title)
                    print(description)
                    print(solo)
                    print(match)
                    print(UserIconUrl)

                else:
                    flex = f"자유랭크 **티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                    match = f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**"
                    print(title)
                    print(description)
                    print(flex)
                    print(match)

    else: # Nonexist User
        print("존재하지 않는 소환사명입니다.\n다시 한번 확인해주세요.")

search_lol_userInfo("Hide on bush", RIOT_API_KET)