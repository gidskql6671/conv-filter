# Cpp로 이미지 필터링

설정하는게 제일 힘들었다...

# openCV 설정관련
[Visual Studio Code에서 CMake 사용하여 OpenCV 코드 컴파일 하기](https://webnautes.tistory.com/933)

# 프로그램 흐름
1. opencv로 이미지 파일을 불러온다.
2. filter를 적용한다.
3. filter가 적용된 이미지를 파일에 저장한다.

위 3가지 과정을 병렬로 빠르게 해보자.

# 시간측정 결과
| 파일 크기 | load image 시간 | apply filter 시간 | save image 시간 |
|---|---|---|---|
|500KB|0.007|0.208|0.011|
|39.1MB|0.795|24.649|4.087|

시간은 초단위이다.
filter 적용하는게 압도적으로 많은 시간을 차지한다.