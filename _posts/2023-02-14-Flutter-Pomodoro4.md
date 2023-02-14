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

### <b>sidebar_widget.dart</b>
```dart
import 'package:flutter/material.dart';
import 'package:pomodoro_app/screen/guide_main_screen.dart';
import 'package:pomodoro_app/widget/sidebar_text_widget.dart';
import 'package:url_launcher/url_launcher.dart';

class SideBar extends StatelessWidget {
  const SideBar({super.key});

  onTextTap() async {
    final Uri url = Uri.parse("http://johnhan0923.dothome.co.kr/");
    await launchUrl(url);
  }

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          UserAccountsDrawerHeader(
            currentAccountPicture: const CircleAvatar(
              backgroundImage: AssetImage('images/johnhan.jpeg'),
              backgroundColor: Colors.white,
            ),
            accountName: const Text("John Han"),
            accountEmail: const Text("gksdygks2124@gmail.com"),
            onDetailsPressed: () {
              print("Pressed");
            },
            decoration: BoxDecoration(
              color: Theme.of(context)
                  .scaffoldBackgroundColor, //Color(0xFF232b55),
              /* borderRadius: BorderRadius.only(
                bottomLeft: Radius.circular(40.0),
                bottomRight: Radius.circular(40.0),
              ), */
            ),
          ),
          const sbText(text: "SETTINGS"),
          const sbText(text: "STATS"),
          const sbText(text: "RATE"),
          InkWell(
            onTap: onTextTap,
            child: const Padding(
              padding: EdgeInsets.all(30.0),
              child: Text(
                "CONTACE US",
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 15,
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(
              left: 30,
              top: 250,
            ),
            child: InkWell(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => GuideMainScreen(),
                  ),
                );
              },
              child: Row(
                children: <Widget>[
                  Icon(
                    Icons.info_outline,
                    color: Theme.of(context).textTheme.displaySmall!.color,
                  ),
                  Text(
                    'App Guide',
                    style: TextStyle(
                      color: Theme.of(context).textTheme.displaySmall!.color,
                    ),
                  )
                ],
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(
              left: 30,
              top: 15,
            ),
            child: InkWell(
              onTap: () {},
              child: Row(
                children: const <Widget>[
                  Icon(
                    Icons.logout_outlined,
                    color: Color(0xFFE7626C),
                  ),
                  Text(
                    "LOGOUT",
                    style: TextStyle(
                      color: Color(0xFFE7626C),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

```