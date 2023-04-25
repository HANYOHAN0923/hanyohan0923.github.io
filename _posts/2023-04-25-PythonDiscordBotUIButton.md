---
title: 디스코드 봇에 버튼 기능 추가하기
author: gksdygks2124
date: 2023-04-25 23:18:00 +0900
categories: [Python, Discord Bot]
tags: [discord.py, discord_ui.py, discord.py buttons, discord bot button]
lastmode: 2023-04-25 23:18:00 +0900
sitemap:
  changefreq: daily
  priority : 1.0
---
> Button Style Doc: https://discord.com/developers/docs/interactions/message-components#buttons


```python
class ButtonView(discord.ui.View):
    isClicked : bool = None

    # 버튼 비활성화 함수
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    # 버튼 입력 시간 제한 함수
    async def on_timeout(self) -> None:
        await self.disable_all_items()

    # 버튼 1
    @discord.ui.button(label="Pass", style=discord.ButtonStyle.success)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.send_message("Pass") # 텍스트 뿐만 아니라 send_message()의 인자로 embed = embed를 통해서 임베드도 전송이 가능하다.
        self.isClicked = True
        self.stop()

    # 버튼 2
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.send_message("Deny")
        self.isClicked = False
        self.stop()


@bot.command()
async def 버튼(ctx):
    view = ButtonView(timeout=5) # 5초 지나면 타임아웃 활성화
    message = await ctx.send(view=view)
    view.message = message # 클래스에서 self를 통해 message인수를 받아오기 위함
    await view.wait() # 버튼 응답 처리
    await view.disable_all_items() # 타임아웃 뿐만 아니라, 버튼이 한번 클릭되고 나서 다른 버튼이 눌리는 것을 방지하기 위해서, 모든 버튼 비활성화
    
    if view.isClicked is None:
        await ctx.send("No input. TimeOut")
    elif view.isClicked is True:
        await ctx.send("Clicked Pass")
    else:
        await ctx.send("Clicked Deny")

```