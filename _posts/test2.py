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
        embed = discord.Embed(title=f"소환사 {result_json['name']}님의 정보", description=f"**{result_json['summonerLevel']} LEVEL**", color=0xAEE3D4)

        userRankInfo = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + result_json["id"]
        resultRank = requests.get(userRankInfo, headers={"X-Riot-Token":RIOT_TOKEN})
        resultRank_json = json.loads(resultRank.text)

        if resultRank_json == []:
            embed.add_field(name=f"해당 유저는 언랭크입니다.", value="**언랭크 유저의 정보는 출력하지 않습니다.**", inline=False)
        else:
            for rank in resultRank_json:
                if rank["queueType"] == "RANKED_SOLO_5x5":
                    embed.add_field(name="솔로랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                           f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)
                else:
                    embed.add_field(name="자유랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                            f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)
        embed.set_author(name=result_json['name'], url=f"http://fow.kr/find/{arg.replace(' ', '')}", icon_url=userIconUrl.format(result_json['profileIconId']))
        return embed
    else:
        error = discord.Embed(title="오류가 발생했습니다.", description="소환사 이름이 존재하지 않거나, 통신에 오류가 있습니다.", color=0xEF5A68)
        return error
       

search_lol_userInfo("Hide on bush", RIOT_API_KET)