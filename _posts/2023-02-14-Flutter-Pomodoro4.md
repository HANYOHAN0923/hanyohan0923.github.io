---
title: Flutter POMODORO App 만들기 (4) - Scaffold(drawer:) 활용해서 앱 메뉴(사이드)바 만들기 (커스텀 버튼으로 Drawer열기) + 이미지 불러오기
author: gksdygks2124
date: 2023-02-14 12:51:00 +0900
categories: [Flutter, POMODORO]
tags: [Flutter, POMODORO, flutter menubar,scaffold drawer,flutter sidebar, sidebar widget, flutter image, image_picker]
lastmode: 2023-02-14 12:51:00
sitemap:
  changefreq: daily
  priority : 1.0
---
> 참고 영상  
> https://th-biglight.tistory.com/26  
> 참고 게시글  
> https://th-biglight.tistory.com/26
{: .prompt-tip }

### <b>커스텀 Drawer()</b>
![flutter_drawer](https://user-images.githubusercontent.com/92556048/218658946-1028354b-f44c-4a29-892e-53490b1d5821.gif) 

<br>

### <b>image_picker로 갤러리에서 사진을 가져와 프로필 사진 변경</b>
![image_picker](https://user-images.githubusercontent.com/92556048/218675866-d378cd05-1940-40a7-87bf-927177201fe3.gif)

 
<br>

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
                    // leading: AppBar() 왼쪽 버튼
                    leading: Builder(
                      builder: (context) => IconButton(
                        onPressed: () => Scaffold.of(context).openDrawer(),
                        icon: const Icon(
                          Icons.menu_rounded,
                          color: Color(0xFFF4EDDB),
                        ),
                      ),
                    ),
                    // actions: AppBar() 오른쪽 버튼
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

<br>
 
### <b>sidebar_widget.dart</b>
```dart
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:pomodoro_app/screen/guide_main_screen.dart';
import 'package:pomodoro_app/widget/sidebar_text_widget.dart';
import 'package:url_launcher/url_launcher.dart';

class SideBar extends StatefulWidget {
  const SideBar({super.key});

  @override
  State<SideBar> createState() => _SideBarState();
}

class _SideBarState extends State<SideBar> {
  onTextTap() async {
    final Uri url = Uri.parse("http://johnhan0923.dothome.co.kr/");
    await launchUrl(url);
  }

  late final ImagePicker _picker = ImagePicker();
  late PickedFile? _image;

  Future _getImage() async {
    PickedFile? image = await (_picker.getImage(source: ImageSource.gallery));
    setState(() {
      _image = image;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          UserAccountsDrawerHeader(
            currentAccountPicture: InkWell(
              onTap: _getImage,
              child: CircleAvatar(
                backgroundImage: _image == null
                    ? const AssetImage('images/johnhan.jpeg')
                    : AssetImage(_image!.path),
                backgroundColor: Colors.white,
              ),
            ),
            accountName: const Text("John Han"),
            accountEmail: const Text("gksdygks2124@gmail.com"),
            onDetailsPressed: () {},
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
                    builder: (context) => const GuideMainScreen(),
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
