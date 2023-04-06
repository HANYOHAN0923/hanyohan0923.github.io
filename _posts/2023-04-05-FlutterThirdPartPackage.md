---
title: 유용한 다트 / 플러터 패키지 모음
author: gksdygks2124
date: 2023-04-06 09:52:00 +0900
categories: [Flutter, ETC]
tags: [Flutter, Dart, 패키지, 라이브러리, 유용한 라이브러리]
lastmode: 2023-04-06 09:52:00
sitemap:
  changefreq: daily
  priority : 1.0
---
> 라이브러리 순서는 Dart -> Flutter, 알파벳 내림차순으로 정리했습니다.  
> 계속해서 추가될 예정
{: .prompt-tip }  

<br>
<br>
<br>

# <b>Dart Package</b>
- [collection]()

<br>

-[http](https://pub.dev/packages/http)  
http요청을 쉽게 할 수 있게 도와주는 `Future`기반 라이브러리

<br>

- [intl](https://pub.dev/packages/intl)
다국어, 통화, 성별, 날짜, 숫자를 지역이나 국가 혹은 특정 형식에 맞춰 변환을 시켜주는 기능을 제공합니다


<br>
<br>

# <b>Flutter Package</b>
- [auto_size_text](https://pub.dev/packages/auto_size_text)  
줄 수에 맞춰서 화면에 렌더링 되는 폰트 사이즈를 자동으로 조절하는 기능을 제공합니다.

<br>

- [badges](https://pub.dev/packages/badges)
앱 내부에서 배지 숫자를 표시하는 기능을 제공합니다.

<br>

- [countup](https://pub.dev/packages/countup)
텍스트(숫자)를 생동감 있게 카운트 업하는 기능을 제공합니다.

<br>
  
- [flutter_local_notifications](https://pub.dev/packages/flutter_local_notifications)
앱이 백그라운드에서 실행되면서 유저에게 다양한 알림 기능을 제공합니다. (기기의 바탕화면에서 앱을 볼 때 배지 알림 개수에 따라 배지 숫자가 보이는 것, 알림 팝업 따위)
  - [좋은 참고 글](https://doitduri.tistory.com/25)

<br>

- [flutter_native_splash](https://pub.dev/packages/flutter_native_splash)  
앱을 실행했을 때 스플래시 화면(흔히 앱을 실행했을 때 브랜드 로고 이미지 혹은 에니메이션과 함께 로딩을 하는 화면)을 제공합니다.
  - 번외) [animated_splash_screen](https://pub.dev/packages/animated_splash_screen) 스플래시 화면에 에니메이션을 적용할 수 있는 화면(단순 에니메이션)

<br>

- [flutter_Screenutil](https://pub.dev/packages/flutter_screenutil)  
다양한 사이즈를 같는 디바이스에 UI가 적절한 레이아웃을 렌더링할 수 있도록 화면과 폰트 사이즈의 조정 기능을 제공합니다.

<br>

- [fluttertoast](https://pub.dev/packages/fluttertoast)  
함수를 통해 토스트 메시지를 통해 사용자에게 간단한 정보를 전달하는 팝업 기능을 제공합니다.

<br>

- [image_picker](https://pub.dev/packages/image_picker)  
갤러리에 접근해서 이미지 혹은 동영상 파일을 가져오거나, 카메라에 직접 접근해서 촬영 후 해당 파일을 가져오는 기능을 제공합니다.

<br>

- [shared_preferences](https://pub.dev/packages/shared_preferences)  
굳이 DB에 저장할 필요 없는 간단하거나, 사소한 설정 값을 앱 내부 파일에 읽고, 저장하고, 수정하고, 삭제할 수 있는 기능을 제공합니다. 다만 앱 캐시를 삭제하거나, 앱을 재설치하면 기존의 정보들은 유지되지 않습니다.

<br>

- [slide_countdown](https://pub.dev/packages/slide_countdown)
카운트다운 기능 및 다양한 카운트다운 UI를 제공합니다.

<br>

- [sliding_up_panel](https://pub.dev/packages/sliding_up_panel)  
드래그 업해서 볼 수 있는 패널, 매인화면을 터치하거나 다시 드래그 다운해서 닫을 수 있는 패널을 제공합니다.

<br>

- [url_launcher](https://pub.dev/packages/url_launcher)  
전화, 문자, 이메일, 하이퍼링크, 시스템 파일 등 다양한 URL처리 기능을 제공합니다.