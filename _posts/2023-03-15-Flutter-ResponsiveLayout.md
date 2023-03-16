---
title: Flutter Responsive Layout - 반응형 디자인
author: gksdygks2124
date: 2023-03-15 09:53:00 +0900
categories: [Flutter, Responsive Layout]
tags: [Flutter, Responsive Layout, Responsive UI, 반응형 디자인]
lastmode: 2023-03-15 09:53:00
sitemap:
  changefreq: daily
  priority : 1.0
---

# <b>화면회전 반응 디자인</b>
## <b>앱 자체를 Portrait(세로), Landscape(가로)로 화면 고정하기</b>
앱을 만들 때 굳이 처음부터 가로 혹은 세로 화면 중 하나만을 선택해서 디자인하는 것도 하나의 방법 중에 하나이다. 앱 전체적으로 하나 방향의 화면만을 사용할 때는 main.dart에서 다음과 같이 코드를 작성하면 된다.  

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    // 선틱1) Portrait Screen만 사용
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,

    // 선택2) Landscape Screen만 사용
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]).then((value) => runApp(const MyApp()));
  runApp(const MyApp());
}
```

<br>

### <b>특정 화면에서 화면 방향을 고정하기</b>
특정 화면에서는 화면 전환 기능을 막거나, 비활성화가 필요할 때 사용하는 방법이다. `initState()`와 `dispose()`를 통해 구현한다.  

```dart
import 'package:flutter/services.dart';

...omit...

// In stful class (특정 스크린에서 landscape만 허용하기)
void initState() {
  super.initState();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeRight,
    DeviceOrientation.landscapeLeft,
  ]);
}


@override
dispose() {
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeRight,
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  super.dispose();
}
```  

<br>

## <b>화면 방향에 맞게 코드 작성하기</b>
Flutter 내부 MediaQuery객체`MediaQuery.of(context).orientation`를 통해 디바이스의 현재 방향을 가져올 수 있다. 가져온 디바이스 방향을 토대로 삼항연산자 혹은 `List<Widget>` 안에서는 if문을 통해, 각 화면 방향에 따라 맞춤 위젯설정을 할 수 있다.

```dart
  @override
  Widget build(BuildContext context) {
    final bool isLandScape = MediaQuery.of(context).orientation == Orientation.landscape;
    
    return Scaffold(
        body: Column(
            children: <Widget>[
                // 삼항 연산자 사용
                isLandScape 
                    ? Text("LandScape")        
                    : Text("Portrait"),
                // List<Widget>에서는 if 사용이 가능하다
                // if의 조건이 충족할 때 즉 Landscape일 때에 Text(), portrait에서는 아무것도 없다
                if(isLandScape)
                    Text("LandScape"),
        ]) //삼함 연산자랑 if문
    );
  }
```

<br>
<br>

# <b>OS 반응형 디자인</b>
긴혹 `Switch()` 같은 위젯은 `.adaptive` 같은 프로퍼티를 통해 OS에 맞춰서 대응이 가능하지만 모든 위젯이 그런 것은 아니다. 가장 좋은 방법은 Flutter(Andoird)의 표준인 Meterial Design과 IOS의 표준인 Cupertino Design이 다르기 때문에 같은 버튼이라도 해도, 화면에 표시되는 것은 다르다. 따라서 같은 앱의 UI를 제공하더라도 Android를 사용하는 사람들에게 사소한 버튼 하나라도 친Android적인 디자인을, IOS에는 친IOS적인 디자인을 채택하는 것이 이질감이 없을 것이다.  

## <b>각 OS의 디자인 표준을 다양하게 부각시키고 싶을 때 (즉 서로 다른점을 많이 두고 싶을 때)</b>
앱의 가장 기초적인 디자인 표준을 정하는 main.dart에서 IOS와 Android 디바이스에 따라 각각 테마를 재정의하는 것이다. 다만 MaterialApp()의 Scaffold()와 CupertinoApp()의 CupertinoPageScaffold()가 취급하는 위젯은 같지만 명칭은 서로 다르다는 것을 기억해야한다. 따라서 번거로운 부분이 있다.  

```dart 
import 'dart:io';

...omit...

  @override
  Widget build(BuildContext context) {
    return Platform.isIOS? CupertinoApp(): MaterialApp();
}
```

<br>

## <b>적은 소수의 특정 부분만 각 OS의 디자인 표준을 살리고 싶을 때</b>  
이런식으로 'dart:io'에서 불러온 Platform객체의 프로퍼티를 통해 실행된 디바이스의 OS 정보와 삼항연산자로 각 OS 별 빌드할 위젯을 다르게 정의할 수 있다.
```dart
import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

Widget appBar() {
  return Platform.isIOS ? const CupertinoNavigationBar() : AppBar();
}
```

<br>
<br>

# <b>기기 사이즈 반응형 디자인</b>
기기 사이즈마다 일괄된 디자인을 적용하기 위한 반응형 디자인을 하기 위해서는 앱이 빌드될 때 기기의 사이즈를 가져와서 계산해서 화면에 그리는 것이 가장 효과적인 방법이다. 이것 역시 `MediaQuery.of(context).size.height/width`를 통해 가져올 수 있다. 간혹 위젯의 사이즈를 가져와서 계산해야하는 경우 `LayoutBuilder()`의 constraints를 통해 알 수 있다. 크기를 계산해야하는 위젯을 `LayoutBuilder()`로 wrapping해주면 된다.  



- [MediaQuery.of(context).size](https://stackoverflow.com/questions/49704497/how-to-make-flutter-app-responsive-according-to-different-screen-size?rq=1)
- [LayoutBuilder()](https://api.flutter.dev/flutter/widgets/LayoutBuilder-class.html)