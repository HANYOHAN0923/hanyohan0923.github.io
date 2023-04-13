---
title: Flutter Home화면 Widet 만들기 (iOS / Android)
author: gksdygks2124
date: 2023-04-13 15:19:00 +0900
categories: [Flutter, ETC]
tags: [Flutter, Widget, Home화면 위젯]
lastmode: 2023-04-13 15:19:00
sitemap:
  changefreq: daily
  priority : 1.0
---

> defendencies: [flutter_widgetkit](https://pub.dev/packages/flutter_widgetkit)  
> ref: https://www.youtube.com/watch?v=NoTc1D26HAo

<br>

### <b>알아두어야할 점</b>
1) 홈 위젯의 이름은 앱 이름과 동일합니다.
2) ios - 앱 외부 홈화면에서 빌드되는 위젯과 14pro 이상의 모델에서 지원하는 다이나믹 아일랜드를 구현하려면 확실하게 iOS의 native(Swift)를 어느 정도 알고 있어야 합니다.
3) Andorid - 이 운영체제 또한 Android의 native(kotlin or Java)에 대한 지식이 필요합니다.  
![Screen Recording 2023-04-13 at 4 04 19 PM_1-min](https://user-images.githubusercontent.com/92556048/231695636-d50fea44-cff7-4468-8b59-71d3eb86d132.gif)
![2-min](https://user-images.githubusercontent.com/92556048/231685097-621c0a2f-04cd-4b4c-8cd3-438950c60e54.gif)

<br>
<br>

# <b>iOS</b>
## <b>Flutter - main.dart</b>  

```dart
import 'dart:convert';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_widgetkit/flutter_widgetkit.dart';

void main() {
  runApp(const MaterialApp(home: TextPage()));
}

class TextPage extends StatefulWidget {
  const TextPage({super.key});

  @override
  State<TextPage> createState() => _TextPageState();
}

class _TextPageState extends State<TextPage> {
  String text = DUMMY_DATA[Random().nextInt(4)];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(text),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  text = DUMMY_DATA[Random().nextInt(4)];
                });
                WidgetKit.setItem(
                  'widgetData',
                  jsonEncode(WidgetData(text)),
                  'group.flutterioswidget',  // 중요!!! 설정하고 기억하라고 한 그룹이름 작성 (아래 Xcode설정에서 나옴)
                );
                WidgetKit.reloadAllTimelines();
              },
              child: const Text('Change'),
            )
          ],
        ),
      ),
    );
  }
}

class WidgetData {
  final String text;
  WidgetData(this.text);

  WidgetData.fromJson(Map<String, dynamic> json) : text = json['text'];
  Map<String, dynamic> toJson() => {'text': text};
}

const List<String> DUMMY_DATA = ["apple", "banana", "samsung?", "dogdrip"];
```

## <b>Xcode - Swift</b>
- <b>STEP1. flutter 프로젝트 안 ios디렉토리를 Xcode로 열고 하단의 "+"버튼 혹은 File > New > Target 클릭</b>
<img src="https://i.imgur.com/JJHKm5H.png">

<br>

- <b>STEP2. Widget Extension을 New Target으로 지정</b>
<img width="736" alt="Screenshot 2023-04-13 at 3 28 13 PM" src="https://user-images.githubusercontent.com/92556048/231675129-14377773-52d6-4e21-a152-9c8c68a6947b.png">

<br>

- <b>STEP3. Product Name 설정, 나머지 설정은 보이는 그대로 하고 Finish</b>
<img width="736" alt="Screenshot 2023-04-13 at 3 28 34 PM" src="https://user-images.githubusercontent.com/92556048/231675139-80f70147-839b-40a4-a97a-78c6bd50979f.png">

<br>

- <b>STEP4. 좌측 TARGETS탭에 방금 만든 extension widget을 선택 > Signing & Capabilities탭에서 "+ Capacity"선택 > "App Groups" 검색 및 선택</b>
<img width="906" alt="Screenshot 2023-04-13 at 3 28 52 PM" src="https://user-images.githubusercontent.com/92556048/231675143-88b53c0c-c14e-479e-972a-8193754dc83f.png">

<br>

- <b>STEP5. 그룹이름 설정 > "group."으로 시작하기 > 이름 기억해야함</b>
<img width="735" alt="Screenshot 2023-04-13 at 3 29 13 PM" src="https://user-images.githubusercontent.com/92556048/231675147-cc2171d8-2e9e-428b-a7df-6538c2b411e8.png">

<br>

- <b>STEP6. TARGETS탭 Runner에서 동일한 작업 진행</b>
<img width="868" alt="Screenshot 2023-04-13 at 3 29 26 PM" src="https://user-images.githubusercontent.com/92556048/231675150-48eb814e-503c-4f51-9ee4-edfe680ba82a.png">
<img width="724" alt="Screenshot 2023-04-13 at 3 29 33 PM" src="https://user-images.githubusercontent.com/92556048/231675154-fb6038b9-15d4-4908-b96a-ea7460b5f95d.png">

<br>

- <b>STEP7. 가장 좌측 프로젝트 디렉토리에 위에서 만든 확장 위젯 디렉토리가 생겼는데 Bundle이 "안" 적힌 Swift파일 선택 및 수정 후 앱 재실행</b>  

<img width="260" alt="Screenshot 2023-04-13 at 3 30 41 PM" src="https://user-images.githubusercontent.com/92556048/231675157-695d63f4-277f-4da3-b322-7902cad8fb9c.png">

<br>

```swift
//
//  ios_widget_flutter.swift
//  ios widget flutter
//
//  Created by John Han on 2023/04/13.
//

import WidgetKit
import SwiftUI
import Intents

struct WidgetData: Decodable, Hashable {
    let text: String
}

struct FlutterEntry: TimelineEntry {
    let date: Date
    let widgetData: WidgetData?
}

struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> FlutterEntry {
        FlutterEntry(date: Date(), widgetData: WidgetData(text: "Flutter IOS Widget"))
    }
    
    func getSnapshot(in context: Context, completion: @escaping (FlutterEntry) -> ()) {
        let entry = FlutterEntry(date: Date(), widgetData: WidgetData(text: "Flutter IOS Widget"))
        completion(entry)
    }
    
    func getTimeline(in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        let shareDefaults = UserDefaults.init(suiteName: "group.flutterioswidget") // 중요!!! 설정하고 기억하라고 한 그룹이름 작성
        let flutterData = try? JSONDecoder().decode(WidgetData.self, from: (shareDefaults?.string(forKey: "widgetData")?.data(using: .utf8)) ?? Data())
        
        let entryDate = Calendar.current.date(byAdding: .hour, value: 24, to: Date())!
        let entry = FlutterEntry(date: entryDate, widgetData: flutterData)
        
        let timeline = Timeline(entries: [entry], policy: .atEnd)
        completion(timeline)
    }
}

struct ios_widget_flutter: Widget {
    let kind: String = "ios_widget_flutter"
    
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) {
            entry in iosWidgetView(entry: entry)
        }
    }
}

struct iosWidgetView: View {
    var entry: Provider.Entry
    
    var body: some View {
        Text(entry.widgetData?.text ?? "Pressed the button in App");
    }
}

```

<br>
<br>
<br>

# <b>Android</b>
추후 추가 예정
