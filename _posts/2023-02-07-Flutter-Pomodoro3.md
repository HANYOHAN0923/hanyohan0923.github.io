---
title: Flutter POMODORO App 만들기 (3) - Flutter Light/Dark Theme (다크모드, 라이트모드 만들기)
author: gksdygks2124
date: 2023-02-07 23:58:00 +0900
categories: [Flutter, POMODORO]
tags: [flutter, light mode, dark mode, light dark mode toggle, theme change, ValueListenableBuilder, ValueNotifier]
lastmode: 2023-02-07 23:58:00
sitemap:
  changefreq: daily
  priority : 1.0
---
> UI Designed by Omar Sherif(https://www.behance.net/iomarsherif)  
> Project UIKIT: https://www.behance.net/gallery/98918603/POMO-UIKIT?tracking_source=search_projects%7Cpomo+uikit

<br>

# <b>Flutter Light / Dark Theme 만들기</b>
우선 Light / Dark Theme을 구분하는 기능을 만들기 전에 먼저 정해야할 것이 있다.
- 앱의 ThemeMode(Light, Dark)는 자동적으로 System의 ThemeMode를 채택함.
- System의 ThemeMode와 상관 없이, 유저가 직접 앱의 ThemeMode를 채택함

<br>

## <b>main.dart에서 Theme설정하기</b>
아래 코드와 같이 `MaterialApp()` 내부에 `theme()`과 `darkTheme()`를 만들어준다.
```dart
 @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        brightness: Brightness.light,
        scaffoldBackgroundColor: const Color(0xFFE7626C),
        textTheme: const TextTheme(
          displayLarge: TextStyle(
            color: Color(0xFF232B55),
          ),
          displaySmall: TextStyle(
            color: Color(0xFF232B55),
          ),
        ),
        cardColor: const Color(0xFFF4EDDB),
      ),
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(
          0xFF232B55,
        ),
        cardColor: const Color(0xFFF4EDDB),
        textTheme: const TextTheme(
          displayLarge: TextStyle(
            color: Color(0xFFE7626C),
          ),
          displaySmall: TextStyle(
            color: Colors.white,
          ),
        ),
      ),
      home: firstRun ? GuideMainScreen() : const HomeScreen(),
    );
  }
```

<br>

### <b>앱의 themeMode를 시스템 설정의 themeMode에 맞추기</b>
`MaterialApp()` 내부에 `theme`과 `darkTheme`을 만든 것처럼 밑에 `themeMode`를 추가하면 된다.
```dart
themeMode: ThemeMode.system, // system themeMode를 사용
themeMode: ThemeMode.light, // MaterialApp(theme())을 사용
themeMode: ThemeMode.dart, // MaterialApp(darkTheme())을 사용
```

<br>

### <b>유저가 앱의 themeMode를 설정하는 toggle 버튼 만들기</b>
![flutter_theme_toggle](https://user-images.githubusercontent.com/92556048/217755444-a8b14f6a-09a6-4241-8800-3fa0c4d8ecd9.gif)


<br>

#### <b>main.dart</b>
우선 main.dart의 `build()`가 직접 `GuideHomeScreen()`이나 `HomeScreen()`을 <span style="color:purple">return</span>하도록 코드를 수정한다. `MaterialApp()`에 있던 theme은 나중에 다시 쓸 것이다.
```dart
import 'package:flutter/material.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';
import 'package:pomodoro_app/screen/guide_main_screen.dart';
import 'package:pomodoro_app/screen/home_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  // OPTIONAL!!!
  // Pass the preserve() method the value returned from WidgetsFlutterBinding.ensureInitialized() to keep the splash on screen.
  WidgetsBinding widgetsBinding = WidgetsFlutterBinding.ensureInitialized();
  FlutterNativeSplash.preserve(widgetsBinding: widgetsBinding);
  runApp(const MyApp());
  // when app has initialized, make a call to remove() to remove the splash screen.
  FlutterNativeSplash.remove();
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late SharedPreferences prefs;
  bool firstRun = true;

  void initPrefs() async {
    prefs = await SharedPreferences.getInstance();
    final isFirstRun = prefs.getBool('isFirstRun');
    if (isFirstRun == false) {
      setState(
        () {
          firstRun = false;
        },
      );
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    initPrefs();
  }

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    if (firstRun) {
      return GuideMainScreen();
    }
    return const HomeScreen();
  }
}
```

<br>

#### <b>HomeScreen</b>
```dart
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:pomodoro_app/widget/sidebar_widget.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  static final ValueNotifier<ThemeMode> themeNotifier =
      ValueNotifier(ThemeMode.dark);

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: themeNotifier,
      builder: (_, ThemeMode currentMode, __) {
        return MaterialApp(
          title: 'Flutter Demo',
          debugShowCheckedModeBanner: false,
          theme: ThemeData(
            brightness: Brightness.light,
            scaffoldBackgroundColor: const Color(0xFFE7626C),
            textTheme: const TextTheme(
              displayLarge: TextStyle(
                color: Color(0xFF232B55),
              ),
              displaySmall: TextStyle(
                color: Color(0xFF232B55),
              ),
            ),
            cardColor: const Color(0xFFF4EDDB),
          ),
          darkTheme: ThemeData(
            brightness: Brightness.dark,
            scaffoldBackgroundColor: const Color(
              0xFF232B55,
            ),
            cardColor: const Color(0xFFF4EDDB),
            textTheme: const TextTheme(
              displayLarge: TextStyle(
                color: Color(0xFFE7626C),
              ),
              displaySmall: TextStyle(
                color: Colors.white,
              ),
            ),
          ),
          themeMode: currentMode,
          home: Builder(
            builder: (context) {
              return Scaffold(
                appBar: AppBar(
                  backgroundColor: Theme.of(context).scaffoldBackgroundColor,
                  elevation: 0,
                  actions: [
                    IconButton(
                      icon: Icon(themeNotifier.value == ThemeMode.light
                          ? Icons.dark_mode
                          : Icons.light_mode),
                      onPressed: () {
                        themeNotifier.value =
                            themeNotifier.value == ThemeMode.light
                                ? ThemeMode.dark
                                : ThemeMode.light;
                      },
                    ),
                  ],
                ),
                backgroundColor: Theme.of(context).scaffoldBackgroundColor,
                body: Center(
                  child: Text(
                    "themeMode",
                  ),
                ),
        );
      },
    );
  }
}

```

<br>

#### <b>ValueNotifier</b>
위의 코드에서 나온 `ValueNotifier`과 `ValueListenableBuilder`에 대해서 설명해보겠다.
> ValueNotifier{: .filepath }은 ChangeNotifier를 상속받는 setState()없이 state 관리를 하는 클래스이다.
{: .prompt-tip }

`ValueNotifier`는 `ValueListenableBuilder()` 안에서 작동을 한다.

- [ValueNotifier DOCS](https://api.flutter.dev/flutter/foundation/ValueNotifier-class.html)
- [ValueListenableBuilder DOCS](https://api.flutter.dev/flutter/widgets/ValueListenableBuilder-class.html)