---
title: Flutter Instagram Clone(1) - 로그인 및 회원가입 기능 구현하기(Firebase Authentication)
author: gksdygks2124
date: 2023-02-22 14:54:00 +0900
categories: [Flutter, Instagram]
tags: [Flutter, Instagram Clone, 인스타그램 클론, Firebase로그인, Flutter Sign In, Flutter Sign Up, Flutter 회원가입, Flutter 로그인, Flutter Custome Icons]
lastmode: 2023-02-22 14:54:00
sitemap:
  changefreq: daily
  priority : 1.0
---
> Github Repo: 

<br>
<br>

# <b>Firebase 프로젝트 생성하고, Flutter Project와 연결하기</b>
## <b> STEP1. <a href="https://console.firebase.google.com/?hl=ko">공홈</a>에서 프로젝트 생성하고, 콘솔창에서 앱 추가(ios 선택) </b>
<img width="411" alt="Screenshot 2023-02-21 at 3 21 33 PM" src="https://user-images.githubusercontent.com/92556048/220535652-4188b25d-cda2-4fd8-92b4-bdb1d7d96bb5.png">

<br>

## <b> STEP2. Apple 번들 ID 작성</b>
Flutter Project Root Dir > ios Dir 우클릭 후 XCODE로 열기, X Code에서 좌측 상단 Runner 클릭 후 Identity에서 Bundle Identifier 확인 가능

<br>

<img width="492" alt="Screenshot 2023-02-21 at 3 22 55 PM" src="https://user-images.githubusercontent.com/92556048/220535732-0a13eebb-9aec-45fc-baee-b6301146a846.png">
<img width="375" alt="Screenshot 2023-02-21 at 3 22 23 PM" src="https://user-images.githubusercontent.com/92556048/220535825-6f07d87c-51c2-4352-8795-143a43fe1ce9.png">
<img width="263" alt="Screenshot 2023-02-21 at 3 23 23 PM" src="https://user-images.githubusercontent.com/92556048/220536510-e6be2558-3c41-4cff-af10-318bb544b100.png">
<img width="597" alt="Screenshot 2023-02-21 at 3 23 34 PM" src="https://user-images.githubusercontent.com/92556048/220536524-0a2ccdd6-5c4e-48ff-bc5e-1d0485fc1fea.png">


## <b> STEP3. 구성 파일(.plist) 설치 후 Runner Dir에 추가</b>
<img width="718" alt="Screenshot 2023-02-21 at 3 26 46 PM" src="https://user-images.githubusercontent.com/92556048/220536757-ad8b31e1-fad6-420d-a90b-f546655d3a5d.png">
<img width="254" alt="Screenshot 2023-02-22 at 3 05 23 PM" src="https://user-images.githubusercontent.com/92556048/220536894-43ce75a6-539c-43b3-bb44-e32528dc9eea.png">

<br>

## <b> STEP4. main.dart 수정 후 플러터 프로젝트 종료 후 재실행</b>
재실행 했을 때 오류 없이 앱이 정상적으로 빌드되면 성공적으로 연결됨. 안 되는 경우 에러 메시지 참조  

### <b>main.dart</b>
```dart
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter_application_1/main_page.dart';

void main() async {
  /* 이 함수는 다음에 호출되는 함수의 모든 작업이 끝날 때까지 대기를 명령하는 명령어이다.
  Firebase 초기화는 비동기로 이루어지기 때문에 사용해야 한다.*/
  WidgetsFlutterBinding.ensureInitialized();
  // 앱에서 Firebase 초기화
  await Firebase.initializeApp();
  runApp(const MyWidget());
}

class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      // MainPage()는 일단 아무렇게나 작성
      home: MainPage(),
    );
  }
}
```

<br>
<br>

# <b>Instagram 로그인, 회원가입 UI 구현</b>
## <b>sign_in_screen.dart</b>

```dart
import 'package:flutter/material.dart';
import 'package:flutter_application_1/common/custome_icon.dart';
import 'package:flutter_application_1/main_page.dart';
import 'package:flutter_application_1/model/firebase_auth_exception_handling.dart';
import 'package:flutter_application_1/screen/sign_up_screen.dart';
import 'package:flutter_application_1/widget/account_field_widget.dart';

class SignInScreen extends StatefulWidget {
  const SignInScreen({super.key});

  @override
  State<SignInScreen> createState() => _SignInScreenState();
}

class _SignInScreenState extends State<SignInScreen> {
  // TextField
  final TextEditingController _emailTextController = TextEditingController();
  final TextEditingController _passwordTextController = TextEditingController();
  // password obscure toggle
  bool toggle = true;

  // 로그인 함수
  Future signIn() async {
    final status = await FirebaseAuthHelper().login(
      email: _emailTextController.text.trim(),
      pass: _passwordTextController.text.trim(),
    );
    // 로그인이 성공했을 때
    if (status == AuthResultStatus.successful) {
      // ignore: use_build_context_synchronously
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => const MainPage(),
        ),
      );
    } else {  // 예외가 발생했을 경우
      final errorMsg = AuthExceptionHandler.generateExceptionMessage(status);
      // ignore: use_build_context_synchronously
      showDialog(
        context: context,
        barrierDismissible: true,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text("Caution!"),
            content: Text(
              errorMsg.toString(),
            ),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                child: const Text("Okay"),
              ),
            ],
          );
        },
      );
    }
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
          // passwordTextField
          SizedBox(
            width: 380,
            child: TextField(
              controller: _passwordTextController,
              obscureText: toggle,
              enableSuggestions: true,
              autocorrect: true,
              cursorColor: Colors.white,
              keyboardType: TextInputType.visiblePassword,
              decoration: InputDecoration(
                suffixIcon: IconButton(
                  onPressed: () {
                    setState(() {
                      toggle = !toggle;
                    });
                  },
                  icon: toggle
                      ? const Icon(
                          Icons.remove_red_eye,
                        )
                      : const Icon(
                          Icons.remove_red_eye_outlined,
                        ),
                ),
                labelText: "password",
                labelStyle: TextStyle(
                  color: Colors.black.withOpacity(0.5),
                ),
                filled: true,
                floatingLabelBehavior: FloatingLabelBehavior.never,
                fillColor: Colors.white.withOpacity(0.3),
                border: const OutlineInputBorder(),
              ),
            ),
          ),
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
          signButton("Sign In", signIn),
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
            child: GestureDetector(
              onTap: () {},
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Icon(
                    CustomIcons.facebook_squared,
                    color: Colors.blue,
                  ),
                  Text(
                    ' Log in with Facebook',
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
                GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const SignUpScreen(),
                      ),
                    );
                  },
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

<br>

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
