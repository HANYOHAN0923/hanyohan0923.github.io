---
title: RIOT API를 사용해서 디스코드 봇에 롤/롤체 전적검색 명렁어 추가하기
author: gksdygks2124
date: 2023-01-25 22:17:00 +0900
categories: [Python, Discord Bot]
tags: [RIOT API, 롤전적검색, 디스코드 봇, TFT전적검색]
---

## RIOT API 사용하기
우선 <a href="https://developer.riotgames.com/">라이엇 개발자 사이트</a>에 로그인을 해서 API를 사용하기 위한 키를 받아야할 뿐만 아니라, 개발에 있어서 중요한 Documents까지 읽어볼 수 있다. 로그인을 하고나면 비영구/영구적 API KEY를 받을 수 있다. 비영구적 API KEY는 24시간의 유효성을 갖고 있으며, 영구적 API KEY를 받기 위해서는 <span style="color:red">REGISTER PRODUCT</span>를 통해 자신이 키를 사용하기 위한 목적을 RIOT에 제출을 해야한다. (번거로울 뿐이지, 쉽게 허가해준다)