# Convolutional filter(s) for images

## 개발 환경
- OS : Window10
- gcc & g++ : MSYS2 사용
  - mingw64 8.0 버전이 `filesystem` 모듈과 버그를 일으켜 MSYS2를 사용함
- cpp standard : cpp+17
- cmake 사용
  

## Usage
### Required
1. `CMakeList.txt` 파일 수정
  - 1번 라인의 OpenCV 디렉토리 설정

### Script
1. ./run.sh

### Non Script
1. 컴파일
  1. `cmake . -G "MinGW Makefiles"`
  2. `make`
2. 실행
  - `./main.exe ./images/color ./result_images < ./configs/filter.txt`
  - `./images/color`는 input 이미지들이 담긴 폴더. 없을 경우 프로그램 종료
  - `./result_images`는 결과 이미지가 담길 폴더. 없을 경우 만들어줌

## 프로그램 플로우
1. opencv를 사용하여 Image file load
2. conv-filter apply
3. filter appiled file 저장


---

## 시간측정 결과
### Single Thread(Single Core)시 결과
시간단위 : 1/sec
| 파일 크기 | load image 시간 | apply filter 시간 | save image 시간 |
|---|---|---|---|
|500KB|0.007|0.208|0.011|
|39.1MB|0.795|24.649|1.350|


### Multi Thread(6CPU)로 병렬실행한 결과
시간단위 : 1/sec
| 파일 크기 | load image 시간 | apply filter + save image 시간 | 총 시간| 싱글 스레드 총 시간 |
|---|---|---|---|---|
|500KB|0.007|0.216|0.223|0.217|
|39.1MB|0.805|4.016|4.821|23.845|
|25개, 총 207MB|7.068|21.828|28.894|174.806|
|120개, 총 58.2MB|1.586|2.386|3.972|25.305|

## 제안하는 알고리즘
Image Filtering 시 Divide&Conquer기법을 이용, 이미지 분할 후 Multi Threading을 통해 이를 처리, 후에 결과를 합쳐 이미지를 재구성 하는 방식을 사용, 단 Image width,col < 512pixel 일 경우 단일 쓰레드를 취하는 방식 사용  
Image Save시에도 Divide&Conquer기법을 이용, 이미지 분할 후 Multu Threading을 통해 Bypass를 늘려 Throuput을 늘리는 방식 사용

Multi Threading 적용 시 약6~7배정도 excution time이 빨라졌다.

## Test Data Set 설명
한 스레드가 처리하는 최대 이미지 크기를 256x256, 512x512, 1024x1024로 두고 데이터셋을 총 207MB의 25개 사진으로 하여 10번씩 테스트하였음

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

## Third Party Software 리스트 및 License 정보
### OpenCV 4.5.2  
https://github.com/opencv/opencv  
Copyrigth 2021 ~ present, OpenCV team  
[ApaChe License 2.0](http://www.apache.org/licenses/LICENSE-2.0)

