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

> defendencies: [flutter_widgetket](https://pub.dev/packages/flutter_widgetkit)  
> ref: https://www.youtube.com/watch?v=NoTc1D26HAo

<br>

## <b>알아두어야할 점</b>
앱 외부 홈화면에서 빌드되는 위젯과 14pro 이상의 모델에서 지원하는 다이나믹 아일랜드를 구현하려면 확실하게 iOS의 native(Swift)를 어느 정도 알고 있어야 합니다.

<br>
<br>

# <b>Flutter - main.dart</b>  

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
                  'group.flutterioswidget',
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

# <b>Xcode - Swift</b>

```Swift
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
        let shareDefaults = UserDefaults.init(suiteName: "group.flutterioswidget")
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