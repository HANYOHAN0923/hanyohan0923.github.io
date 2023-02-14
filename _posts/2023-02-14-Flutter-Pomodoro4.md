---
title: Flutter POMODORO App 만들기 (4) - Scaffold(drawer:) 활용해서 앱 메뉴(사이드)바 만들기
author: gksdygks2124
date: 2023-02-14 12:51:00 +0900
categories: [Flutter, POMODORO]
tags: [Flutter, POMODORO, flutter menubar,scaffold drawer,flutter sidebar, sidebar widget]
lastmode: 2023-02-14 12:51:00
sitemap:
  changefreq: daily
  priority : 1.0
---
home_screen.dart의 scafforld의 drawer에 추가하면된다.
![flutter_drawer](https://user-images.githubusercontent.com/92556048/218658946-1028354b-f44c-4a29-892e-53490b1d5821.gif)
 
<br>
 
### <b>sidebar_widget.dart</b>

### <b>home_screen.dart</b>
```dart
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
                    // added
                    leading: Builder(
                      builder: (context) => IconButton(
                        onPressed: () => Scaffold.of(context).openDrawer(),
                        icon: const Icon(
                          Icons.menu_rounded,
                          color: Color(0xFFF4EDDB),
                        ),
                      ),
                    ),
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
                  // added
                  drawer: const SideBar(),
                  backgroundColor: Theme.of(context).scaffoldBackgroundColor,
                  body: const Center(
                    child: Text("Hello World"),
                  ),
              );
            },
          ),
        );
      },
    );
  }
}

```
