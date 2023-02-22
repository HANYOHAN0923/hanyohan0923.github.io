---
title: Flutter Instagram Clone(1) - 로그인 및 회원가입 기능 구현하기(Firebase Authentication)
author: gksdygks2124
date: 2023-02-22 14:54:00 +0900
categories: [Flutter, Instagram]
tags: [Flutter, Instagram Clone, 인스타그램 클론, Firebase로그인, Flutter Sign In, Flutter Sign Up, Flutter 회원가입, Flutter 로그인, Flutter Custome Icons, Flutter Firebase Auth Exceptions Handling, Flutter Firebase Auth Error Handling, Flutter Firebase 인증 예외처리, Flutter showDialog(), Flutter AlertDialog()]
lastmode: 2023-02-22 14:54:00
sitemap:
  changefreq: daily
  priority : 1.0
---
> Github Repo: https://github.com/HANYOHAN0923/instagram_clone   
> Docs: https://firebase.google.com/docs/auth/admin/errors?hl=ko  
> Docs: https://firebase.google.com/docs/auth/flutter/errors?hl=ko  
> Docs: https://firebase.google.com/docs/auth/flutter/start?hl=ko  
> Ref: https://medium.com/flutter-community/firebase-auth-exceptions-handling-flutter-54ab59c2853d
{: .prompt-tip }

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
  Firebase 초기화는 비동기로 이루어지기 때문에 사용해야 한다 */
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
![psObscure-min](https://user-images.githubusercontent.com/92556048/220538096-805598db-86f2-4487-868f-e87d674b5f68.gif)

<br>
<br>

## <b>main_page.dart</b>  

```dart
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_application_1/screen/home_screen.dart';
import 'package:flutter_application_1/screen/sign_in_screen.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: StreamBuilder<User?>(
        // stream을 통해서 현재 인증 상태를 실시간으로 확인할 수 있다
        // stream이란 데이터의 흐름, 통로로 볼 수 있다
        stream: FirebaseAuth.instance.authStateChanges(),
        // 로그인 혹은 로그아웃으로 변경된 인증상태를 Stream을 통해 클라이언트에게 전송해준다. 그리고 변경되었을 때 마다 스냅샷이 이를 인식하여 값을 알려주게 된다. 
        // 따라서 로그인이 되면 snapshot이 데이터를 갖게 됨으로, snapshot의 상태를 통해 홈화면과 로그인화면 중 렌더링할 화면을 결졍하게 된다
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return const HomeScreen();
          } else {
            return const SignInScreen();
          }
        },
      ),
    );
  }
}
```

<br>
<br>

## <b>home_screen.dart</b>
간단하게 로그인 했을 때 유저의 정보 중 일부를 출력하고, 로그아웃 버튼을 갖은 화면을 만들었다.  

<br>

```dart
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_application_1/model/firebase_auth_exception_handling.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // 현재 로그인된 유저
  final user = FirebaseAuth.instance.currentUser!;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Signed in as ${user.email!}',
            ),
            MaterialButton(
              onPressed: () {
                // 밑에서 작성 예정
              },
              child: const Text(
                'Sign out',
              ),
            )
          ],
        ),
      ),
    );
  }
}
```

<br>
<br>

## <b>sign_in_screen.dart</b>

<br>

```dart
import 'package:flutter/material.dart';
import 'package:flutter_application_1/common/custome_icon.dart';
import 'package:flutter_application_1/main_page.dart';
import 'package:flutter_application_1/model/firebase_auth_handling.dart';
import 'package:flutter_application_1/screen/sign_up_screen.dart';
import 'package:flutter_application_1/widget/account_field_widget.dart';

class SignInScreen extends StatefulWidget {
  const SignInScreen({super.key});

  @override
  State<SignInScreen> createState() => _SignInScreenState();
}

class _SignInScreenState extends State<SignInScreen> {
  final TextEditingController _emailTextController = TextEditingController();
  final TextEditingController _passwordTextController = TextEditingController();
  bool toggle = true;

  Future signIn() async {
    // 밑에서 작성할 예정
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
          // code 밑부분에 Extract Widget 했음
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
              // 비밀번호 가리기 혹은 보기 버튼
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
          // code 밑부분에 Extract Widget 했음
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
          // 커스텀 버튼
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

SizedBox accountTextField(
    String text, bool isPassword, TextEditingController controller) {
  return SizedBox(
    width: 380,
    child: TextField(
      controller: controller,
      obscureText: isPassword,
      enableSuggestions: isPassword,
      autocorrect: isPassword,
      cursorColor: Colors.white,
      keyboardType: isPassword
          ? TextInputType.visiblePassword
          : TextInputType.emailAddress,
      decoration: InputDecoration(
        labelText: text,
        labelStyle: TextStyle(
          color: Colors.black.withOpacity(0.5),
        ),
        filled: true,
        floatingLabelBehavior: FloatingLabelBehavior.never,
        fillColor: Colors.white.withOpacity(0.3),
        border: const OutlineInputBorder(),
      ),
    ),
  );
}

ElevatedButton signButton(String text, Function onPressed) {
  return ElevatedButton(
    style: ElevatedButton.styleFrom(
      backgroundColor: Colors.blueAccent,
    ),
    child: SizedBox(
      width: 350,
      height: 50,
      child: Center(
        child: Text(
          text,
          style: const TextStyle(
            color: Colors.white,
          ),
        ),
      ),
    ),
    onPressed: () {
      onPressed();
    },
  );
}
```

<br>

### <b>커스텀 아이콘 삽입</b>
페이스북 아이콘을 넣기 위해서, 커스텀 아이콘을 삽입하였다. 커스텀 아이콘은 <a href="https://www.fluttericon.com/">여기</a>에서 얻을 수 있다. 마음에 드는 아이콘을 zip파일로 설치 후, ttf파일은 따로 프로젝트 루트 디렉토리에 fonts 디렉토리를 만들어서 이동하고, dart파일은 lib 디렉토리에 옮기면 된다. config파일은 당장 필요 없다. 아마 설치받으면 MyFlutterApp.dart/.ttf 이런 식의 이름일텐데 본인이 알아서 이름은 수정하면 된다.

<br>

#### <b>pubspec.yaml 수정</b>
```yaml
  fonts:
    - family: CustomIcons # 원하는 family이름 작성
      fonts:
        - asset: fonts/FacebookIcon.ttf # 프로젝트 내부 ttf파일 위치
```

<br>

#### <b>.dart 수정</b>
```dart
import 'package:flutter/widgets.dart';

class CustomIcons {
  CustomIcons._();
  
  // pubspec.yaml에서 family에 작성한 이름과 똑같이 작성
  static const _kFontFam = 'CustomIcons';

  // 변수 이름이 곧 아이콘 이름
  static const IconData facebook_squared = IconData(
    0xf308,
    fontFamily: _kFontFam,
  );
}
```

<br>
<br>

## <b>sign_up_screen.dart</b>
기본적으로 sign_in_screen.dart와 비슷하다. 약간의 수정만 있을 뿐

<br>

```dart
import 'package:flutter/material.dart';
import 'package:flutter_application_1/model/firebase_auth_handling.dart';
import 'package:flutter_application_1/screen/sign_in_screen.dart';
import 'package:flutter_application_1/widget/account_field_widget.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final TextEditingController _emailTextController = TextEditingController();
  final TextEditingController _passwordTextController = TextEditingController();
  bool toggle = true;

  // 
  @override
  void dispose() {
    _emailTextController.dispose();
    _passwordTextController.dispose();
    super.dispose();
  }

  Future signUp() async {
    // 밑에서 다시 작성할 예정
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
          signButton(
            "Sign Up",
            signUp,
          ),
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
                  "Are you alreaady have an account?",
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
                        builder: (context) => const SignInScreen(),
                      ),
                    );
                  },
                  child: const Text(
                    'Sign In.',
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
<br>

# <b>로그인, 회원가입, 예외처리 기능 추가하기</b>
본격적으로 로그인, 회원가입 기능을 제대로 사용하기 앞서서 프로젝트 콘솔에서 마지막으로 작업을 해야한다. 생성한 Firebase 프로젝트에서 Authentication > Sign-in Method 탭에서 로그인 제공업체 이메일/비밀번호을 추가해준다. 

<br>

## <b>firebase_auth_handler.dart</b>
- `FirebaseAuth.instance.createUserWithEmailAndPassword(email, pass)`: 전달 받은 이email, pass를 통해 유저 id, password를 만드는 firebase_auth로부터 제공되는 함수
- `FirebaseAuth.instance.signInUserWithEmailAndPassword(email, pass)`: 전달 받은 이email, pass를 통해 로그인을 진행하는 firebase_auth로부터 제공되는 함수
- `FirebaseAuth.instance.signOut()`: 현재 로그인된 유저를 로그아웃하는 firebase_auth로부터 제공되는 함수

<br>

```dart
import 'package:firebase_auth/firebase_auth.dart';

// 예외처리: 회원가입 시에 아이디가 중복이거나 로그인 시에 비밀번호가 틀리는 경우와 같은 예외를 처리합니다
enum AuthResultStatus {
  successful,
  emailAlreadyExists,
  wrongPassword,
  invalidEmail,
  userNotFound,
  weakPassword,
  undefined
}

class AuthExceptionHandler {
  static handleException(e) {
    AuthResultStatus status;
    switch (e.code) {
      case "email-already-in-use":
        status = AuthResultStatus.emailAlreadyExists;
        break;
      case "invalid-email":
        status = AuthResultStatus.invalidEmail;
        break;
      case "user-not-found":
        status = AuthResultStatus.userNotFound;
        break;
      case "wrong-password":
        status = AuthResultStatus.wrongPassword;
        break;
      case "weak-password":
        status = AuthResultStatus.weakPassword;
        break;
      default:
        status = AuthResultStatus.undefined;
    }
    return status;
  }

  static generateExceptionMessage(exceptionCode) {
    String errorMessage;
    switch (exceptionCode) {
      case AuthResultStatus.invalidEmail:
        errorMessage = "Your email address appears to be malformed.";
        break;
      case AuthResultStatus.wrongPassword:
        errorMessage = "Your password is wrong.";
        break;
      case AuthResultStatus.userNotFound:
        errorMessage = "User with this email doesn't exist.";
        break;
      case AuthResultStatus.emailAlreadyExists:
        errorMessage = "The email has already been registered.";
        break;
      case AuthResultStatus.weakPassword:
        errorMessage = "Password should be at least 6 characters";
        break;
      default:
        errorMessage = "An undefined Error happened.";
    }

    return errorMessage;
  }
}


class FirebaseAuthHelper {
  // 로그인에 관련된 함수 createUserWithEmailAndPassword(), signInWithEmailAndPassword(),logout()를 편하게 불러서 사용하기 위해 객체 초기화
  static final _auth = FirebaseAuth.instance;
  // 예외가 발생했을 경우 해당 예외 경우를 유저에게 설명하기 위해 함수에서 에러를 담을 변수 선언 (초기화는 함수에서 진행)
  late AuthResultStatus _status;

  // 계정생성
  Future<AuthResultStatus> createAccount({email, pass}) async {
    try {
      UserCredential authResult = await _auth.createUserWithEmailAndPassword(
          email: email, password: pass);
      if (authResult.user != null) {
        _status = AuthResultStatus.successful;
      } else {
        _status = AuthResultStatus.undefined;
      }
    } catch (e) {
      _status = AuthExceptionHandler.handleException(e);
    }
    return _status;
  }

  // 로그인
  Future<AuthResultStatus> login({email, pass}) async {
    try {
      final authResult =
          await _auth.signInWithEmailAndPassword(email: email, password: pass);

      if (authResult.user != null) {
        _status = AuthResultStatus.successful;
      } else {
        _status = AuthResultStatus.undefined;
      }
    } catch (e) {
      _status = AuthExceptionHandler.handleException(e);
    }
    return _status;
  }

  // 로그아웃
  static logout() {
    _auth.signOut();
  }
}
```

## <b>sign_in_screen.dart</b>
아까 위에서 비워두었던 함수를 아래와 같이 작성한다.  

`// ignore: use_build_context_synchronously` => 오류 방지용 주석

<br>

```dart
  Future signIn() async {
    // firebase_auth_handler.dart에서 불러온 함수
    final status = await FirebaseAuthHelper().login(
      email: _emailTextController.text.trim(),
      pass: _passwordTextController.text.trim(),
    );
    if (status == AuthResultStatus.successful) {
      // 로그인 성공시 MainPage()로 넘어가는데, MainPage()는 authStateChanges()를 통해 로그인된 상태면 HomeScreen()을 렌더링함
      // ignore: use_build_context_synchronously
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => const MainPage(),
        ),
      );
    } else {
      // 로그인에서 예외가 발생했을 때 예외(오류)애 대한 설명 팝업을 뛰운다
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
```

## <b>sign_up_screen.dart</b>

<br>

```dart
  Future signUp() async {
    final status = await FirebaseAuthHelper().createAccount(
      email: _emailTextController.text.trim(),
      pass: _passwordTextController.text.trim(),
    );
    if (status == AuthResultStatus.successful) {
      // ignore: use_build_context_synchronously
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => const SignInScreen(),
        ),
      );
    } else {
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
                onPressed: () => Navigator.pop(context),
                child: const Text("Okay"),
              ),
            ],
          );
        },
      );
    }
  }
```