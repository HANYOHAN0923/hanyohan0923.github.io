---
title: Flutter POMODORO App 만들기 (3) - Flutter Light/Dark Theme (다크모드, 라이트모드 만들기)
author: gksdygks2124
date: 2023-02-05 10:48:00 +0900
categories: [Flutter, POMODORO]
tags: [flutter, light mode, dark mode, light dark mode toggle, theme chage]
lastmode: 2023-02-05 10:48:00
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

### <b></b>