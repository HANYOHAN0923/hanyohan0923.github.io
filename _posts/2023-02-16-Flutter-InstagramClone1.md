---
title: Flutter Instagram Clone(1)
author: gksdygks2124
date: 2023-02-16 10:10:00 +0900
categories: [Flutter, Instagram]
tags: [Flutter, Instagram Clone, 인스타그램 클론, Firebase로그인, Flutter Sign In, Flutter Sign Up, Flutter 회원가입, Flutter 로그인]
lastmode: 2023-02-16 10:10:00
sitemap:
  changefreq: daily
  priority : 1.0
---

# Firebase Authentication 로그인  

# sign_in_screen.dart
좀 더 중앙화해서 코딩하기, extract widget가능해 보이는 부분은 최대한 진행하고
```dart
import 'package:flutter/material.dart';
import 'package:flutter_application_1/widget/account_field_widget.dart';

class SignInScreen extends StatefulWidget {
  const SignInScreen({super.key});

  @override
  State<SignInScreen> createState() => _SignInScreenState();
}

class _SignInScreenState extends State<SignInScreen> {
  final TextEditingController _emailTextController = TextEditingController();
  final TextEditingController _passwordTextController = TextEditingController();

  void greeting() {
    print("hello world");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          Padding(
            padding: const EdgeInsets.only(
              bottom: 30,
            ),
            child: SizedBox(
              width: 180,
              child: Image.asset("assets/images/instagram.png"),
            ),
          ),
          accountTextField("email", false, _emailTextController),
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 5),
          ),
          passwordTextField("password", true, _passwordTextController),
          Padding(
            padding: const EdgeInsets.only(top: 20, bottom: 40),
            child: Row(
              children: [
                const Padding(
                  padding: EdgeInsets.symmetric(
                    horizontal: 145,
                  ),
                ),
                InkWell(
                  onTap: () {},
                  child: const Text(
                    "Forgot password?",
                    style: TextStyle(
                      color: Colors.blueAccent,
                    ),
                  ),
                )
              ],
            ),
          ),
          signButton("Sign In", greeting),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 40),
            child: Text(
              'OR',
              style: TextStyle(
                color: Colors.black.withOpacity(0.5),
                fontSize: 15,
              ),
            ),
          ),
          SizedBox(
            width: 200,
            child: InkWell(
              onTap: () {},
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Icon(Icons.abc),
                  Text(
                    'Log in with Facebook',
                    style: TextStyle(
                      color: Colors.blue,
                      fontSize: 15,
                    ),
                  ),
                ],
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(top: 200, bottom: 30),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  "Don't have an account?",
                  style: TextStyle(
                    color: Colors.black.withOpacity(0.5),
                  ),
                ),
                const SizedBox(
                  width: 5,
                ),
                InkWell(
                  onTap: () {},
                  child: const Text(
                    'Sign Up.',
                    style: TextStyle(
                      color: Colors.blueAccent,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

```

# sign_up_screen.dart

낚시, 도박 -> 크롤링 파이썬 디스코드봇 게시글 추가