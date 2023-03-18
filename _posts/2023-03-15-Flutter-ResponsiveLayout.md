---
title: Flutter Responsive Layout - 반응형 디자인
author: gksdygks2124
date: 2023-03-15 09:53:00 +0900
categories: [Flutter, Responsive Layout]
tags: [Flutter, Responsive Layout, Responsive UI, 반응형 디자인, MediaQuery, LayoutBuilder(), Platform, Landscape, Portrait]
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


## <b>쉽고 빠른 방법(1) - `MediaQuery`를 통해 디바이스의 스크린 정보(비율, 폭과 넓이) 가져오기</b>  
다음과 같이 직접적으로 스크린의 넓이과 높이를 계산해서 반응하는 화면을 구성할 수 있다.
```dart
MediaQueryData queryData = MediaQuery.of(context);

// get Device Screen's width and height
final screenWidth = queryData.size.width;
final screenHeight = queryData.size.height;

// get text scale factor
final txtsFactor = queryData.textScaleFactor
```

<br>

## <b>쉽고 빠른 방법(2) - `AspectRatio()`를 통해 부모 위젯의 사이즈에서 특정 비율만큼 공간 가져오기</b>  
AspectRatio클래스를 통해서 자신을 감싸고 있는 부모 위젯이 갖을 수 있는 최대 사이즈에서 인수`aspectRatio`로 전달하는 비율만큼 자식 위젯의 사이즈를 정해주는 위젯이다.

즉 아래 예제를 코드와 결과 화면을 보면알 수 있다. `AspectRatio()`의 부모 위젯은 `Center()`이다. `Center()`는 자식을 화면의 가장 가운데에 위치시키는 속성만 갖고 있고, 넓이와 높이에 대한 제한을 두지 않는다. 따라서 `Center()`의 자식이 갖을 수 있는 최대 넓이와 높이는 디바이스의 높넓이와 동일하다. `AspectRatio()`의 aspectRatio는 자식 위젯의 비율을 1대1로 하기 위해 1 /1을 인수로 받았다. 따라서 `AspectRatio()`의 자식 `Container()`의 크기는 디바이스의 높넓이의 1대1비율(높이 = 넓이, 정사각형)만큼 갖게 된다.  


```dart
Center(
 child: AspectRatio(
  aspectRatio: 1 / 1,
  child: Container(
    decoration: BoxDecoration(
      shape: BoxShape.rectangle,
      color: Colors.orange,
      )
    ),
  ),
),
```

<br>

## <b>복잡하지만 디테일하면서 구조적인 방법</b>  
`LayoutBuilder()`는 부모 위젯의 여유 높넓이를 <span style="color:Aquamarine">constraints</span>로 반환을 한다. 따라서 `build()`하는 위젯 트리의 최상위 부모 위젯이 `LayoutBuilder()`일 경우에 <span style="color:Aquamarine">constraints</span>는 당연히 디바이스의 최대 높넓이를 갖게 된다. 따라서 아래와 같이 모바일, 테블린, PC에 따로따로 맞춤 UI를 제작을 따로하여서, 그에 맞는 화면을 빌드하는 방법을 선택할 수도 있다.   

```dart
const int mobileMaxSize = 400;
const int tabletMaxSize = 1200;

class ResponsiveHomeLayout extends StatelessWidget {
  final Widget mobileHomeLayout;
  final Widget tabletHomeLayout;
  final Widget desktopHomeLayout;

  ResponsiveHomeLayout({
    required this.mobileHomeLayout,
    required tabletHomeLayout,
    required this.desktopHomeLayout,
    super.key,
  })

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth) <= mobileMaxSize{
          return mobileHomeLayout;
        } else if (constraints.maxWidth < tabletMaxSize) {
          return tabletHomeLayout;
        } else {
          return desktopHomeLayout;
        }
      }
    );
  }
}

```

<br>
<br>
<br>

> Reference
{: .prompt-tip }  
- [MediaQuery.of(context).size](https://stackoverflow.com/questions/49704497/how-to-make-flutter-app-responsive-according-to-different-screen-size?rq=1)
- [LayoutBuilder()](https://api.flutter.dev/flutter/widgets/LayoutBuilder-class.html)