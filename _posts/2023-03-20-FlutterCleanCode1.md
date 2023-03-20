---
title: Flutter Clean Code(1) - 위젯트리를 어떻게 분리할 것인가? [위젯과 메서드]
author: gksdygks2124
date: 2023-03-20 15:53:00 +0900
categories: [Flutter, Clean Code]
tags: [Flutter, Flutter Clean Code, Flutter 클린코드, Flutter WidgetTree split, Flutter 위젯트리 분리 분할 ]
lastmode: 2023-03-20 15:53:00
sitemap:
  changefreq: daily
  priority : 1.0
---

# <b>위젯을 어떻게 분리할 것인가?</b>
처음 Flutter를 배우고 나서, 문득 이런 궁금증이 생겼다. 위젯을 위젯 트리에서 분리할 때(혹은 커스텀 위젯을 만들 때), `Widget을 반환하는 함수형`으로 분리하는 것과, `위젯(클래스)`로 분리하는 것의 차이점이 궁금했다. 이것에 대한 답변은 build()의 특징을 다시 한번 생각해보는 것을 통해 해결할 수 있었다.

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MaterialApp(home: MyApp()));
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text("$_count"),
            ElevatedButton(
                onPressed: () => setState(() {
                      _count += 1;
                    }),
                child: const Text("Add"))
          ],
        ),
      ),
    );
  }
}
```

<br>

## <b>Widget을 반환하는 함수로 분리</b>  

결론부터 말하자면 이 방법은 <span style="color:red">안티패턴</span>, 즉 좋지 않은 방법이다. 버튼이 눌려서 setState()가 실행될 때마다 플루터 프레임워크는 build()를 다시 호출 한다. 그런데 _buildText()는 위젯이 아닌 메서드이기 때문에 build()가 호출될 때마다 같이 반복해서 호출이 된다는 것이다. 사실상 _buildText()가 반환하는 위젯은 변경점이 없기 때문에 상태관리가 필요 없어서, 한번의 빌드로도 충분한데 말이다. Stateful Widget은 상태가 변경된 UI만 따로 빌드하는 장점을 갖는데, 이것을 무의미하게 만드는 방법인 것이다. 즉 CPU 자원만 낭비하는 셈이 된다. 여기에 쓰인 예제 코드는 정말 단순한 예제 앱의 코드이기 때문에 큰 상관이 없지만, 프로젝트와 같은 규모가 큰 앱에서는 큰 영향을 미친다.
```dart
class _MyAppState extends State<MyApp> {
  int _count = 0;

  Widget _buildText() {
    return const Text('add');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              "$_count",
            ),
            ElevatedButton(
              onPressed: () => setState(() {
                _count += 1;
              }),
              child: _buildText(),
            ),
          ],
        ),
      ),
    );
  }
}
```

<br>

## <b>Widget을 상속받는 위젯(클래스)로 분리</b> 
이렇게 Widget으로 분리하면 상태 관리가 필요 없는 정적 위젯트리를 다시 빌드하지 않아도 된다. 따라서 Flutter 앱의 성능을 최적화하는 기본적인 방식 중 하나이다. 

```dart
class _MyAppState extends State<MyApp> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              "$_count",
            ),
            ElevatedButton(
              onPressed: () => setState(() {
                _count += 1;
              }),
              child: const CustomText(),
            ),
          ],
        ),
      ),
    );
  }
}

class CustomText extends StatelessWidget {
  const CustomText({super.key});

  @override
  Widget build(BuildContext context) {
    return const Text("add");
  }
}
```

<br>

# <b>Today's CleanCode Conclusion</b>
위젯트리를 Widget을 반환하는 여러개의 작은 메서드로 분리하는 것은 CPU 사이클 낭비를 가져온다. 따라서 stless widget으로 분리하는 것을 통해 Flutter의 성능을 최적화할 수 있다.