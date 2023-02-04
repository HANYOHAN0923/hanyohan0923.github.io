---
title: Flutter POMODORO App 만들기 (1) - Flutter 앱 시작화면/스플래시 스크린 만들기
author: gksdygks2124
date: 2023-02-04 17:01:00 +0900
categories: [Flutter, POMODORO]
tags: [flutter, flutter_splash_native, flutter splash screen, flutter 시작화면]
lastmode: 2023-02-04 17:01:00
sitemap:
  changefreq: daily
  priority : 1.0
---
> UI Designed by Omar Sherif(https://www.behance.net/iomarsherif)
> Project UIKIT: https://www.behance.net/gallery/98918603/POMO-UIKIT?tracking_source=search_projects%7Cpomo+uikit

<br>
<br>

## <b>스플래시 스크린은 꼭 필요할까?</b>
![flutter_splash_screen](https://user-images.githubusercontent.com/92556048/216756893-988e7e0b-98d0-4db0-8a47-ce64387abffe.gif)
<br>
아직 내가 회사 같은 곳에서 전문적으로 마켓팅팀, 개발팀, 디자인팀 등 여러부서와 함께 고민하며 앱을 개발하는 것이 아니고 학부생이기 때문에 명확하게 알지는 못하지만, 내가 생각하는 스플래쉬 스크린의 목적은 두가지가 있다.

1) <b>UX</b>: SNS의 앱에 비교해서 설명을 하겠다. 사용자 간의 소통을 위해 개발된 SNS앱들은 앱에서 보이는 광고, 친구목록, 채팅내역 모든 정보들은 절대로 기기 로컬에 저장되는 것이 아니라, 서버에서 불러오는 것이다. 즉 서버로부터 불러오는 시간이 요구되기 때문에 딜레이가 생긴다. 그렇다면 앱을 실행하고 서버로부터 정보를 받아와 화면에 표시하는 동안 사용자는 빈화면을 보면서 기다려야하는 것이다. 이것은 아마 대다수의 사람에게 불쾌한 경험일 것이다. 그렇다고 로딩되는 로딩화면을 넣자니 비록 짧은 시간이라도 사용자들은 로딩시간이 길게 느껴질 수 있기 때문에 이런 스플래쉬 스크린을 통해 해결을 한 것이라고 생각한다.

2) <b>브랜딩</b>: 적어도 내가 지금까지 써온 앱들에서는 스플래쉬 스크린이 안 들어간 앱을 본적이 없다. 보통은 스플래쉬 스크린에 브랜드 이미지를 장식하는 경우가 많은데, 비록 스플래쉬 스크린이 보이는 시간은 1~2초 정도의 짧은 시간이지만 사용자는 매번 앱을 사용할 때마다 스플래쉬 스크린을 보게 된다. 따라서 1~2초 정도의 시간의 축적은 사용자에게 브랜드 로고나 추구하는 이미지 혹은 방향성을 각인시키는데 충분하다고 생각한다. 즉 `마켓팅의 하나의 수단`으로 사용되는 것이다.

<br>
<br>

## <b>Flutter에서 스플래쉬 스크린 구현하기</b>
Flutter에서 스플래쉬 스크린을 구현하기 위해서는 직접 만들 수 있지만, 이미 좋은 서드 파트 패키지가 있다. 언제나처럼 <a href="https://pub.dev/packages/flutter_native_splash">flutter_native_splash</a>를 pubspec.yaml에 설치해주면 된다.

<br>

### <b>스플래쉬 스크린 설정하기</b>
스플래쉬 스크린에 대한 설정은 dart파일이 아닌, yaml파일에서 작성한다. `pubspec.yaml` 가장 아래에 계속해서 작성하거나, 아니면 루트디렉토리에 `flutter_native_splash.yaml`파일을 새로 작성한다. 공식 문서에서 제공하는 설정들은 아래와 같다.
```yaml
flutter_native_splash:
  # This package generates native code to customize Flutter's default white native splash screen
  # with background color and splash image.
  # Customize the parameters below, and run the following command in the terminal:
  # flutter pub run flutter_native_splash:create
  # To restore Flutter's default white splash screen, run the following command in the terminal:
  # flutter pub run flutter_native_splash:remove

  # color or background_image is the only required parameter.  Use color to set the background
  # of your splash screen to a solid color.  Use background_image to set the background of your
  # splash screen to a png image.  This is useful for gradients. The image will be stretch to the
  # size of the app. Only one parameter can be used, color and background_image cannot both be set.
  color: "#42a5f5"
  #background_image: "assets/background.png"

  # Optional parameters are listed below.  To enable a parameter, uncomment the line by removing
  # the leading # character.

  # The image parameter allows you to specify an image used in the splash screen.  It must be a
  # png file and should be sized for 4x pixel density.
  #image: assets/splash.png

  # The branding property allows you to specify an image used as branding in the splash screen.
  # It must be a png file. It is supported for Android, iOS and the Web.  For Android 12,
  # see the Android 12 section below.
  #branding: assets/dart.png

  # To position the branding image at the bottom of the screen you can use bottom, bottomRight,
  # and bottomLeft. The default values is bottom if not specified or specified something else.
  #branding_mode: bottom

  # The color_dark, background_image_dark, image_dark, branding_dark are parameters that set the background
  # and image when the device is in dark mode. If they are not specified, the app will use the
  # parameters from above. If the image_dark parameter is specified, color_dark or
  # background_image_dark must be specified.  color_dark and background_image_dark cannot both be
  # set.
  #color_dark: "#042a49"
  #background_image_dark: "assets/dark-background.png"
  #image_dark: assets/splash-invert.png
  #branding_dark: assets/dart_dark.png

  # Android 12 handles the splash screen differently than previous versions.  Please visit
  # https://developer.android.com/guide/topics/ui/splash-screen
  # Following are Android 12 specific parameter.
  android_12:
    # The image parameter sets the splash screen icon image.  If this parameter is not specified,
    # the app's launcher icon will be used instead.
    # Please note that the splash screen will be clipped to a circle on the center of the screen.
    # App icon with an icon background: This should be 960×960 pixels, and fit within a circle
    # 640 pixels in diameter.
    # App icon without an icon background: This should be 1152×1152 pixels, and fit within a circle
    # 768 pixels in diameter.
    #image: assets/android12splash.png

    # Splash screen background color.
    #color: "#42a5f5"

    # App icon background color.
    #icon_background_color: "#111111"

    # The branding property allows you to specify an image used as branding in the splash screen.
    #branding: assets/dart.png

    # The image_dark, color_dark, icon_background_color_dark, and branding_dark set values that
    # apply when the device is in dark mode. If they are not specified, the app will use the
    # parameters from above.
    #image_dark: assets/android12splash-invert.png
    #color_dark: "#042a49"
    #icon_background_color_dark: "#eeeeee"

  # The android, ios and web parameters can be used to disable generating a splash screen on a given
  # platform.
  #android: false
  #ios: false
  #web: false

  # Platform specific images can be specified with the following parameters, which will override
  # the respective parameter.  You may specify all, selected, or none of these parameters:
  #color_android: "#42a5f5"
  #color_dark_android: "#042a49"
  #color_ios: "#42a5f5"
  #color_dark_ios: "#042a49"
  #color_web: "#42a5f5"
  #color_dark_web: "#042a49"
  #image_android: assets/splash-android.png
  #image_dark_android: assets/splash-invert-android.png
  #image_ios: assets/splash-ios.png
  #image_dark_ios: assets/splash-invert-ios.png
  #image_web: assets/splash-web.png
  #image_dark_web: assets/splash-invert-web.png
  #background_image_android: "assets/background-android.png"
  #background_image_dark_android: "assets/dark-background-android.png"
  #background_image_ios: "assets/background-ios.png"
  #background_image_dark_ios: "assets/dark-background-ios.png"
  #background_image_web: "assets/background-web.png"
  #background_image_dark_web: "assets/dark-background-web.png"
  #branding_android: assets/brand-android.png
  #branding_dark_android: assets/dart_dark-android.png
  #branding_ios: assets/brand-ios.png
  #branding_dark_ios: assets/dart_dark-ios.png

  # The position of the splash image can be set with android_gravity, ios_content_mode, and
  # web_image_mode parameters.  All default to center.
  #
  # android_gravity can be one of the following Android Gravity (see
  # https://developer.android.com/reference/android/view/Gravity): bottom, center,
  # center_horizontal, center_vertical, clip_horizontal, clip_vertical, end, fill, fill_horizontal,
  # fill_vertical, left, right, start, or top.
  #android_gravity: center
  #
  # ios_content_mode can be one of the following iOS UIView.ContentMode (see
  # https://developer.apple.com/documentation/uikit/uiview/contentmode): scaleToFill,
  # scaleAspectFit, scaleAspectFill, center, top, bottom, left, right, topLeft, topRight,
  # bottomLeft, or bottomRight.
  #ios_content_mode: center
  #
  # web_image_mode can be one of the following modes: center, contain, stretch, and cover.
  #web_image_mode: center

  # The screen orientation can be set in Android with the android_screen_orientation parameter.
  # Valid parameters can be found here:
  # https://developer.android.com/guide/topics/manifest/activity-element#screen
  #android_screen_orientation: sensorLandscape

  # To hide the notification bar, use the fullscreen parameter.  Has no effect in web since web
  # has no notification bar.  Defaults to false.
  # NOTE: Unlike Android, iOS will not automatically show the notification bar when the app loads.
  #       To show the notification bar, add the following code to your Flutter app:
  #       WidgetsFlutterBinding.ensureInitialized();
  #       SystemChrome.setEnabledSystemUIOverlays([SystemUiOverlay.bottom, SystemUiOverlay.top]);
  #fullscreen: true

  # If you have changed the name(s) of your info.plist file(s), you can specify the filename(s)
  # with the info_plist_files parameter.  Remove only the # characters in the three lines below,
  # do not remove any spaces:
  #info_plist_files:
  #  - 'ios/Runner/Info-Debug.plist'
  #  - 'ios/Runner/Info-Release.plist'
```

이 글 위에서 보였던 스플래쉬 스크린 작동 영상의 화면은 아래와 같이 간단하게 설정했다.
```yaml
# pubspec.yaml
flutter_native_splash:
  image: images/pomodoro-clock.png
  color: "F4EDDB"
```

<br>

### <b>패키지 실행하기</b>
설정이 끝났으면 다른 서드 파트 패키지와 다르게 따로 터미널에서 명렁어로 해당 패키지를 실행시켜서 프로젝트 내부에서 활성화를 필요로 한다. 위 명령어를 입력 후 터미널에서 오류 없이 잘 실행했으면 별다른 설정 없이 앱을 실행했을 때 스플래쉬 화면이 등장하는 것을 볼 수 있다. 기본적으로 Flutter Framework에서 첫 프레임을 화면에 그릴 때 스플래쉬 스크린은 자동적으로 제거된다.

pubspec.yaml에 작성 / root디렉토리에 yaml파일 생성 했을 경우:
```shell
flutter pub run flutter_native_splash:create
```

yaml파일을 특정 위치에 저장했을 경우
```shell
flutter pub run flutter_native_splash:create --path=path/to/my/file.yaml
```

<br>

### <b>앱 초기화 설정하기</b>
앱을 실행했을 때 서버로부터 받아올 것이 없거나, 적어서 처리속도가 매우 빨라서 그저 브랜딩 목적의 스플래쉬 스크린이라면 위의 설정만으로도 충분하지만, 서버로부터 받아오는 양이 많아 스플래쉬 스크린이이 앱이 초기화될 때까지 유지되야다면 `preserve()`와 `remove()`를 main.dart의 메인함수에서 사용함으로써 스플래쉬 화면을 수동 유지 및 제거할 수 있다.
```Dart
import 'package:flutter_native_splash/flutter_native_splash.dart';

void main() {
    // Pass the preserve() method the value returned from WidgetsFlutterBinding.ensureInitialized() to keep the splash on screen.
    WidgetsBinding widgetsBinding = WidgetsFlutterBinding.ensureInitialized();
    FlutterNativeSplash.preserve(widgetsBinding: widgetsBinding);

    runApp(const MyApp());

    // when app has initialized, make a call to remove() to remove the splash screen.
    FlutterNativeSplash.remove();
}
```

<br>

### <b>마무리</b>
yaml파일에서 splash screen을 설정하는 것에 있어서 backgroundimage 같은 일부 기능은 android ver12 이후로는 지원을 안 하는 등 여러 이슈에 관한 업데이트와 많은 사람들이 겪는 오류들은 <a href="https://pub.dev/packages/flutter_native_splash">공식 사이트</a>에서 찾아볼 수 있다.