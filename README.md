# Convolutional filter(s) for images

## 개발 환경
- OS : Window10
- gcc & g++ : MSYS2 사용
  - mingw64 8.0 버전이 `filesystem` 모듈과 버그를 일으켜 MSYS2를 사용함
- cpp standard : cpp+17
- cmake 사용
  

## Usage
1. 컴파일
  1. `cmake . -G "MinGW Makefiles"`
  2. `make`
2. 실행
  - `./main.exe ./images/color ./result_images < ./configs/filter.txt`
  - `./images/color`는 input 이미지들이 담긴 폴더. 없을 경우 프로그램 종료
  - `./result_images`는 결과 이미지가 담길 폴더. 없을 경우 만들어줌

## 프로그램 플로우
1. opencv로 이미지 파일을 불러온다.
2. filter를 적용한다.
3. filter가 적용된 이미지를 파일에 저장한다.

위 3가지 과정을 병렬로 빠르게 해보자.

---

## 시간측정 결과
### 한개의 스레드로 순차실행한 결과
| 파일 크기 | load image 시간 | apply filter 시간 | save image 시간 |
|---|---|---|---|
|500KB|0.007|0.208|0.011|
|39.1MB|0.795|24.649|1.350|

시간은 초단위이다.
filter 적용하는게 압도적으로 많은 시간을 차지한다.  
생산자-소비자 패턴을 적용하고, 생산자를 파일 입력 스레드로 하나 내지 두개를 두고, 소비자를 필터 및 파일 저장으로 두는게 좋을거같다.  

큰 이미지는 쪼개서 여러개의 스레드가 처리하도록 하자. 구현의 편의를 위해 해당 이미지를 받은 스레드가 추가적으로 스레드를 더 호출한 후, join하는 식으로 구현해보자  


### 12개의 스레드로 병렬실행한 결과
| 파일 크기 | load image 시간 | apply filter + save image 시간 |
|---|---|---|
|500KB|0.007|0.216|
|39.1MB|0.805|4.016|
|25개, 총 207MB|7.068|21.828|


512x512 크기의 이미지로 나누어서 병렬처리한 후, 결과를 다시 합쳐 저장하는 방식으로 구현하였다.  
가로, 세로 모두 512 pixel을 넘지않는 이미지의 경우 한개의 스레드에서 처리하였다. 
 
500KB 크기의 이미지는 가로x세로 512x512로 한개의 스레드에서 처리했기에 순차실행한 것과 차이가 없다.  
39.1MB 크기의 이미지는 이미지를 불러오는 시간은 아주 조금 증가했다. 그러나 필터를 적용하고 저장하는 시간이 매우 단축되었다.

---

## 프로젝트 구조
- images
  - Filter를 적용하려는 이미지들이 위치하는 디렉토리
  - color 디렉토리에는 컬러 이미지가 위치하며, 해당 디렉토리의 이미지를 사용한다
- result_images
  - 결과 이미지가 위치한다.
- configs
  - filter.txt가 위치한다.
- src
  - 프로그램 코드들이 위치한다.


---

<br>

## etc
cpp 관련한 환경 설정하는게 제일 힘들었다...

### openCV 설정관련
[Visual Studio Code에서 CMake 사용하여 OpenCV 코드 컴파일 하기](https://webnautes.tistory.com/933)