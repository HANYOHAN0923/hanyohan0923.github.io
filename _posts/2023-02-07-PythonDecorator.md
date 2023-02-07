---
title: Python 데코레이터
author: gksdygks2124
date: 2023-02-07 09:55:00 +0900
categories: [Python]
tags: [python decorator, decorator, 파이썬 데코레이터]
lastmode: 2023-02-07 09:55:00
sitemap:
  changefreq: daily
  priority : 1.0
---
> https://dojang.io/mod/page/view.php?id=2428

## <b>@decorator 사용, 미사용의 차이</b>

<br>

### <b>@decorator 미사용</b>

```python
def trace(func):
    def wrapper():
        print(func.__name__, 'START')
        func()
        print(func.__name__, 'END')
    return wrapper

def hello():
    print('hello')
def world():
    print('world')

trace_hello = trace(hello)
trace_world = trace(world)

'''result
hello START
hello
hello END
world START
world
world END
'''
```

<br>

### <b>@decorator 사용</b>

```python
def trace(func):
    def wrapper():
        print(func.__name__, 'START')
        func()
        print(func.__name__, 'END')
    return wrapper

@trace
def hello():
    print('hello')
@trace
def world():
    print('world')

trace_hello = trace(hello)
trace_world = trace(world)
'''result
hello START
hello
hello END
world START
world
world END
'''
```

## <b>매개변수와 반환값을 처리하는 @decorator</b>

<br>

### <b>매개변수와 반환값을 처리하는 @decorator</b>
```python
def trace(func):          # 호출할 함수를 매개변수로 받음
    def wrapper(a, b):    # 호출할 함수 add(a, b)의 매개변수와 똑같이 지정
        r = func(a, b)    # func에 매개변수 a, b를 넣어서 호출하고 반환값을 변수에 저장
        print('{0}(a={1}, b={2}) -> {3}'.format(func.__name__, a, b, r))  # 매개변수와 반환값 출력
        return r          # func의 반환값을 반환
    return wrapper        # wrapper 함수 반환
 
@trace              # @데코레이터
def add(a, b):      # 매개변수는 두 개
    return a + b    # 매개변수 두 개를 더해서 반환
 
print(add(10, 20))
'''result
add(a=10, b=20) -> 30
30
'''
```

<br>

### <b>가변 함수 인수 @decorator</b>
```python
def trace(func):                     # 호출할 함수를 매개변수로 받음
    def wrapper(*args, **kwargs):    # 가변 인수 함수로 만듦
        r = func(*args, **kwargs)    # func에 args, kwargs를 언패킹하여 넣어줌
        print('{0}(args={1}, kwargs={2}) -> {3}'.format(func.__name__, args, kwargs, r))
                                     # 매개변수와 반환값 출력
        return r                     # func의 반환값을 반환
    return wrapper                   # wrapper 함수 반환
 
@trace                   # @데코레이터
def get_max(*args):      # 위치 인수를 사용하는 가변 인수 함수
    return max(args)
 
@trace                   # @데코레이터
def get_min(**kwargs):   # 키워드 인수를 사용하는 가변 인수 함수
    return min(kwargs.values())
 
print(get_max(10, 20))
print(get_min(x=10, y=20, z=30))
'''result
get_max(args=(10, 20), kwargs={}) -> 20
20
get_min(args=(), kwargs={'x': 10, 'y': 20, 'z': 30}) -> 10
10
'''
```

<br>

## <b>매개변수가 있는 @decorator</b>
매개변수가 있는 데코레이터는 내부에 함수를 더 만들어야한다.
```python
def is_multiple(x):              # 데코레이터가 사용할 매개변수를 지정
    def real_decorator(func):    # 호출할 함수를 매개변수로 받음
        def wrapper(a, b):       # 호출할 함수의 매개변수와 똑같이 지정
            r = func(a, b)       # func를 호출하고 반환값을 변수에 저장
            if r % x == 0:       # func의 반환값이 x의 배수인지 확인
                print('{0}의 반환값은 {1}의 배수입니다.'.format(func.__name__, x))
            else:
                print('{0}의 반환값은 {1}의 배수가 아닙니다.'.format(func.__name__, x))
            return r             # func의 반환값을 반환
        return wrapper           # wrapper 함수 반환
    return real_decorator        # real_decorator 함수 반환
 
@is_multiple(3)     # @데코레이터(인수)
def add(a, b):
    return a + b
 
print(add(10, 20))
print(add(2, 5))
'''result
add의 반환값은 3의 배수입니다.
30
add의 반환값은 3의 배수가 아닙니다.
7
'''
```