# Taking_Medicine_Management

## Hardware Configuration

- Raspbeery Pi 4
- SD card 32G
- element14 camera module

## Server Configuration

- Ubuntu 21.0.4 desktop verion

## Concept

### Step 1 (item estimation)

- 약통 인식 (실시간 스트리밍)
    - 약통 물체 인식
        - Yolov3 모델 > tenserflow 변환 후 구현
    - 약통에 적힌 숫자 인식
        - Tensorflow 사용
        
- 흐름 Dialog
 
* 약통 등록 상황

1. 사용자가 카메라에 숫자가 적힌 약통을 보여줌
2. tensorflow를 이용하여 약통과 약통에 적힌 숫자 인식
3. 사용자에게 약통(약)에 대한 정보를 입력하도록 요구
4. 약통(약) 정보와 인식된 숫자를 Spring을 통해 DB에 저장
5. 약통 등록 완료

* 약통 인식 상황

1. 사용자가 카메라에 숫자가 적힌 (사전 등록된) 약통을 보여줌
2. tensorflow를 이용하여 약통과 약통에 적힌 숫자 인식
3. DB에 저장된 약통(약)에 대한 정보를 불러옴
4. Step2로 넘어감

### Step 2 (pose estimation)
ⓐ 환경구축
1. 임베디드 환경 구축
2. 우분투 서버 구축

ⓑ 데이터 추출 및 전처리
1. Posenet 이미지 추출 페이지 ( 라즈베리파이 카메라)
2. Posenet 이미지 --> 엑셀 추출
(3. 엑셀 라벨링)

- Spring 기반 웹페이지

ⓒ AI 모델링
1. Dense 모델 생성
2. weight 학습
3. 가중치 학습 결과 확인

- Colab 사용

ⓓ 동영상 스트리밍 환경 구축
1. Spring 웹페이지
2. 라즈베리파이 스트리밍 API
3. 동작인식 AI
4. 포드포워딩 및 웹 서비스 구축

## Proceed

### Hardware & Software Setting

#### Raspberrypi4 SSH && Camera enable

```
sudo raspi-config
Interfacing Option > camera & ssh > enable  
```
![image](https://user-images.githubusercontent.com/81907470/188829857-b089da73-ea49-443a-a0c6-5129a0acf7a3.png)


#### Static IP Assignment

- check IP

```
ifconfig
```
![image](https://user-images.githubusercontent.com/81907470/188831351-7ddf5a7a-768d-4c64-8276-bd7dfaaa01f5.png)

- IP assignment

```
 sudo vim /etc/dhcpcd.conf
```
![image](https://user-images.githubusercontent.com/81907470/188831018-95b3e7d5-e11e-4108-8566-18d65189de87.png)

### VNC Connection

- Raspberry PI setting 

```
sudo raspi-config
Interfacing Option > VNC > enable
```
- Install Ultra VNC

https://uvnc.com/downloads/ultravnc.html

![image](https://user-images.githubusercontent.com/81907470/188837420-7eebef41-7ab7-4800-be17-ab460edddeac.png)

- Input IP Info & Login

![image](https://user-images.githubusercontent.com/81907470/188837620-54cadc02-8911-4ab3-9fc2-ad14e35bca88.png)

![image](https://user-images.githubusercontent.com/81907470/188837633-a673a286-7e61-43e9-92ba-5ad743539189.png)

![image](https://user-images.githubusercontent.com/81907470/188837746-ec4f635a-08cc-421f-8c50-1d2cc9c2a3ac.png)

## Reference

### Yolov3 + OpenCV4 + Tesseract OCR

- https://github.com/rnasterofmysea/RaspberryPi4_Yolov3

### Posenet + Pose estimation

-  https://ivdevlog.tistory.com/2

### Posenet + Dataset << * Chanwon
- https://hongchan.tistory.com/3
 
## Trouble Issues

### (Raspberry Pi 4) SSH connection timeout - fixed

https://sote.tistory.com/249
https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=duehd88&logNo=20201603052
