# Taking_Medicine_Management

## Hardware Configuration

- Raspbeery Pi 4
- SD card 32G
- element14 camera module

## Server Configuration

- Ubuntu 21.0.4 desktop verion
- debian
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

https://www.realvnc.com/en/connect/download/viewer/

![image](https://user-images.githubusercontent.com/90185805/188858355-becbecc5-684b-472d-a6b5-0b1ff9804f57.png)

- Input IP Info & Login

![image](https://user-images.githubusercontent.com/81907470/188837620-54cadc02-8911-4ab3-9fc2-ad14e35bca88.png)

![image](https://user-images.githubusercontent.com/81907470/188837633-a673a286-7e61-43e9-92ba-5ad743539189.png)

![image](https://user-images.githubusercontent.com/81907470/188837746-ec4f635a-08cc-421f-8c50-1d2cc9c2a3ac.png)

### Python Version Downgrading

!! To use tensorflow & OpenCV in raspberrypi4, you should downgrade python version and manage dependency --- python3.7.12

- Check current version & path

```
which python
python -V

which python3
python3 -V
```
![image](https://user-images.githubusercontent.com/81907470/190107522-67163422-622f-4326-8cc1-543d423ca8d3.png)

- Firmware upgrade & update

```
sudo apt-get update & sudo apt-get upgrade
```

- Install python 3.7.12

```
wget https://www.python.org/ftp/python/3.7.12/Python-3.7.12.tgz
```

```
sudo tar xzf Ptyhon-3.7.12.tgz
```

![image](https://user-images.githubusercontent.com/81907470/190112185-31587a21-4c23-46fd-8349-7987b084c08d.png)

```
cd Python-3.7.21
./configure --enable-optimizations
sudo make -j 4
sudo make altinstall
```

- Change default python version
```
echo "alias python=/usr/local/bin/python3.7" >> ~/.bashrc
source ~/.bashrc
```

- Symbolic link python3.7.12 path
```
sudo ln -sf /usr/local/bin/python3.7 /usr/bin/python
sudo ln -sf /usr/local/bin/python3.7 /usr/bin/python3
```
![image](https://user-images.githubusercontent.com/81907470/190114062-ee21ffac-b211-49a3-9433-74920d6e4def.png)

- Symblic link pip3.7 (to avoid dependency issue)

![image](https://user-images.githubusercontent.com/81907470/190115034-8c37a201-ab78-47fb-ae05-f2ef0c5f445f.png)

```
sudo ln -sf /usr/local/bin/pip3.7 /usr/bin/pip
sudo ln -sf /usr/local/bin/pip3.7 /usr/bin/pip3
```

### Install Tensorflow

!! you should check firmware & python version and install suitable tensorflow
> tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl

- Check System
```
uname -a
```

![image](https://user-images.githubusercontent.com/81907470/190106325-5031bf81-e0f4-4c27-abe8-c3f817fb1f91.png)

- Find & Check matching version 

![image](https://user-images.githubusercontent.com/81907470/190106588-fb286ad2-a97d-41ed-92ea-7a0b25387cb9.png)

- Make virtual envrionment

```
cd Desktop
mkdir project
cd project
```

```
python3 -m pip install virtualenv
python3 -m virtualenv env
source env/bin/activate
```
(type 'deactivate' to quit)

- Install prerequired package 

```
sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev cython3 libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev
```

```
pip install -U wheel mock six
sudo -H pip3 install --upgrade setuptools
```

- Install tensorflow
(tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl)

```
wget https://github.com/Qengineering/Tensorflow-Raspberry-Pi/raw/master/tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl
```

```
sudo -H pip3 install tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl
```

```
sudo reboot
```

- Test tensorflow

```
python 
import tensorflow
tensorflow.__version__
```
![image](https://user-images.githubusercontent.com/81907470/190125553-15e14c73-c99b-433b-9f67-44541b933baa.png)

### Install OpenCV4

https://github.com/rnasterofmysea/RaspberryPi4_Yolov3

- raspberrypi upgrade

```
sudo apt-get -y update && sudo apt-get -y  upgrade
sudo apt-get -y install python3-dev
```

- install python package

```
pip3 install opencv-python
```

- install opencv library

```
pip3 install opencv-contrib-python 
sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test
```

or 

```
sudo apt-get install libatlas-base-dev
```

### Test OpenCV

- make test.py

```
import cv2
img = cv2.imread("/lenna.png")

cv2.imshow("Test",img)

img_canny = cv2.Canny(img, 50, 150)

cv2.imshow("Test img Edge", img_canny)

cv2.waitKey(0)

cv2.destroyAllWindows()
```

- save image in current directory

![image](https://user-images.githubusercontent.com/81907470/190128141-9d863e94-668c-4d2c-b958-2d7dcd90a3fd.png)

- run test.py

```
python test.py
```


# Next Cloud

## Package upgrade & update & install

  
```
sudo apt upgrade
sudo apt update
sudo apt install nginx mariadb-server php php-fpm php-mysql php-zip php-common php-zip php-xml php-mbstring php-gd php-curl -y
```




## Check packages

- check raspberry pi IP address

```
ifconfig
```

- connect [IP address]

![image](https://user-images.githubusercontent.com/81907470/180170222-c88f7b95-04ea-48c1-a796-c577e782a17e.png)

## Database setting

- Enter mariadb as root

```
sudo mariadb -u root
```
- Create database

```
MariaDB [(none)]> CREATE DATABASE nextcloud;
```

- Create new account

```
MariaDB [(none)]> CREATE USER 'nextcloud'@'localhost' IDENTIFIED BY '1234';
```

- Grant setting

```
MariaDB [(none)]> GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextcloud'@'localhost';
```

```
quit
```
![image](https://user-images.githubusercontent.com/90185805/190652682-ec5dc013-bc73-495f-bce6-d3426a8153ee.png)


## Install NextCloud

- Download zip file

```
wget https://download.nextcloud.com/server/releases/latest.zip
```

- unzip zip file
```
sudo rm /var/www/html/*
sudo unzip ./latest.zip -d /var/www/html/
sudo chown -R www-data:www-data /var/www/html
(auth setting)
```

## Nginx setting
- php 버전 확인 
```
php -v
```
![image](https://user-images.githubusercontent.com/90185805/190646402-1d7eec5a-a14f-414a-afb6-c3340b751e7b.png)

```
sudo nano /etc/nginx/sites-enabled/default
```

- delete code > copy & paste


```nginx
upstream php-handler {
    server unix:/var/run/php/php8.1-fpm.sock;
}

server {
    listen 80;
    listen [::]:80;
    server_name localhost;

    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Robots-Tag none;
    add_header X-Download-Options noopen;
    add_header X-Permitted-Cross-Domain-Policies none;
    add_header Referrer-Policy no-referrer;
    fastcgi_hide_header X-Powered-By;

    root /var/www/html/nextcloud;

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    location = /.well-known/carddav {
      return 301 $scheme://$host:$server_port/remote.php/dav;
    }
    location = /.well-known/caldav {
      return 301 $scheme://$host:$server_port/remote.php/dav;
    }

    client_max_body_size 512M;
    fastcgi_buffers 64 4K;

    gzip on;
    gzip_vary on;
    gzip_comp_level 4;
    gzip_min_length 256;
    gzip_proxied expired no-cache no-store private no_last_modified no_etag auth;
    gzip_types application/atom+xml application/javascript application/json application/ld+json application/manifest+json application/rss+xml applicaEnter this intion/vnd.geo+json application/vnd.ms-fontobject application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc text/vtt text/x-component text/x-cross-domain-policy;

    location / {
        rewrite ^ /index.php;
    }

    location ~ ^\/(?:build|tests|config|lib|3rdparty|templates|data)\/ {
        deny all;
    }
    location ~ ^\/(?:\.|autotest|occ|issue|indie|db_|console) {
        deny all;
    }

    location ~ ^\/(?:index|remote|public|cron|core\/ajax\/update|status|ocs\/v[12]|updater\/.+|oc[ms]-provider\/.+)\.php(?:$|\/) {
        fastcgi_split_path_info ^(.+?\.php)(\/.*|)$;
        set $path_info $fastcgi_path_info;
        try_files $fastcgi_script_name =404;
        include fastcgi_params;
        fastcgi_read_timeout 1800;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $path_info;
        fastcgi_param modHeadersAvailable true;
        fastcgi_param front_controller_active true;
        fastcgi_pass php-handler;
        fastcgi_intercept_errors on;
        fastcgi_request_buffering off;
    }

    location ~ ^\/(?:updater|oc[ms]-provider)(?:$|\/) {
        try_files $uri/ =404;
        index index.php;
    }

    location ~ \.(?:css|js|woff2?|svg|gif|map)$ {
        try_files $uri /index.php$request_uri;
        add_header Cache-Control "public, max-age=15778463";
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header X-Robots-Tag none;
        add_header X-Download-Options noopen;
        add_header X-Permitted-Cross-Domain-Policies none;
        add_header Referrer-Policy no-referrer;

        access_log off;
    }

    location ~ \.(?:png|html|ttf|ico|jpg|jpeg|bcmap)$ {
        try_files $uri /index.php$request_uri;
        access_log off;
    }
}
```
- Reload nginx

```
sudo nginx -s reload
```

## Check Nginx
- nginx 상태 확인
```
service nginx status
```

![image](https://user-images.githubusercontent.com/90185805/190648530-77738125-a43b-4e92-93c6-722ec7cb4959.png)

- http://도메인 주소 또는 IP
```
http://127.0.0.1/

http://localhost/
```
![image](https://user-images.githubusercontent.com/90185805/190655561-e73bfca0-f13d-4df3-af0e-256a41fa1b59.png)


## nextcloud와 로컬PC 연동

- 로컬PC의 nextlcoud 실행 후 프로필 => 설정

![image](https://user-images.githubusercontent.com/90185805/190653934-994dbb79-900b-4b92-8e32-20721733394f.png)

- 동기화 폴더 연결 추가

![image](https://user-images.githubusercontent.com/90185805/190653975-a5ef5c95-e46c-4ec9-b1c7-b88fb4f2f62c.png)

- 동기화 할 로컬 폴더 선택

![image](https://user-images.githubusercontent.com/90185805/190654016-aee03819-620a-4780-9479-572898a50cf7.png)

- nextcloud의 원격 대상 폴더 선택

![image](https://user-images.githubusercontent.com/90185805/190654057-7d2ac610-3dfd-4cf8-a4fa-ee41415b1b72.png)

- 동기화하지 않을 원격 폴더 선택

![image](https://user-images.githubusercontent.com/90185805/190654203-3a0baaea-4502-4845-b4c5-57abb891ac7b.png)

- nextcloud와 로컬 PC 연동 완료

![image](https://user-images.githubusercontent.com/90185805/190654247-7c4fd149-ad28-443c-aa3d-2889125da56e.png)

- 동기화 확인

![image](https://user-images.githubusercontent.com/90185805/190654278-7219624b-e447-4ac3-b4d9-4027ba5296db.png)

## 이미지 라벨링
- ./windows_v1.8.1/data
    - 클래스를 추가할 수 있는 txt파일
- ./windows_v1.8.1/labelImg.exe
    - 실행파일

![image](https://user-images.githubusercontent.com/90185805/190962315-d90d06ba-4748-4a6c-b248-502726bc5849.png)

### predefined_classes.txt
- medicine box를 추가

![image](https://user-images.githubusercontent.com/90185805/190963399-0b932544-bcc6-404e-9860-b52f5202a0eb.png)

### 실행화면
- 1번 클릭하여 `YOLO`로 변경
- 2번 클릭 후 라벨링할 이미지 파일을 선택

![image](https://user-images.githubusercontent.com/90185805/190963181-0d67e7a3-fe3c-403e-a47e-839146e30688.png)

### 이미지가 추가 된 화면

![image](https://user-images.githubusercontent.com/90185805/190963967-690cc443-0d04-47ac-aab0-80bae0f8850f.png)

### 이미지 라벨링 시작
1. 키보드 `w`클릭하여 이미지 라벨링
2. txt파일에서 추가시킨 class명을 선택
3. 저장하여 txt파일 추가
4. 키보드 `d`를 눌러 다음 이미지로 전환
5. 학습시킬 이미지 파일에 이동하여 `classes.txt` 파일 삭제

![image](https://user-images.githubusercontent.com/90185805/190964073-3803cfeb-ff8d-4b58-b05a-77cf080fffb9.png)

![image](https://user-images.githubusercontent.com/90185805/190964226-b7c819ca-4014-4f0f-aafe-321de15ea4be.png)

- txt파일에는 이미지의 라벨링 좌표값이 저장되어있다.

![image](https://user-images.githubusercontent.com/90185805/190965061-5c3b86f1-3d61-4804-a621-e415d4c2d913.png)


### 이미지 라벨링 참고
- https://velog.io/@kimsoohyun/YOLO-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%9D%BC%EB%B2%A8%EB%A7%81%EC%9D%84-%EC%9C%84%ED%95%9C-labelImg-%EC%82%AC%EC%9A%A9%EB%B2%95

---

## Colab에서 라벨링한 이미지로 YOLO3 학습

### 1번
![image](https://user-images.githubusercontent.com/90185805/190965554-afe0d0cd-e9d4-42be-8476-d6f8fba1363e.png)

### 2번
![image](https://user-images.githubusercontent.com/90185805/190965700-4a9d72be-a8e6-4b3a-b494-af685e390e4c.png)

### 3번
![image](https://user-images.githubusercontent.com/90185805/190965841-3c700a0e-c595-4736-a0b5-f37ce3115b85.png)

### 4번
![image](https://user-images.githubusercontent.com/90185805/190968055-9bc0d567-9845-4453-a6b6-50f41b6f935c.png)

### 5번
![image](https://user-images.githubusercontent.com/90185805/190965893-020c24bf-12b4-49a9-9834-444a691650e2.png)

### 6번
![image](https://user-images.githubusercontent.com/90185805/190965912-5be46da4-2812-4433-8f18-423b05220956.png)


### 학습된 YOLO3 나온 결과_1
![image](https://user-images.githubusercontent.com/90185805/190965948-2f461c83-c4e0-4aad-b0e2-418512f09f29.png)

### 학습된 YOLO3 나온 결과_2
![image](https://user-images.githubusercontent.com/90185805/190966007-2dc0341d-6a2a-4895-b028-ad6d197f770f.png)

### YOLO3 파일 정보
 - `yolov3_testing.cfg` : YOLO3 config 파일
 - `yolov3_training_last.weights` : 학습된 YOLO3 가중치 데이터
![image](https://user-images.githubusercontent.com/90185805/190967489-fd98b940-b0f2-4908-979e-91fd9361020c.png)

```python
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

net = cv2.dnn.readNet("../gdrive/MyDrive/yolov3/yolov3_training_last.weights", "cfg/yolov3_training.cfg")
classes = []
with open("./data/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()] 
colors = np.random.uniform(0, 255, size=(len(classes), 3))
img = cv2.imread("test_medicine2.jpg")
img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)
class_ids = []
confidences = []
boxes = []
flag = "flag"
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            flag = str(confidence)
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)            
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            from google.colab.patches import cv2_imshow
font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label+flag, (x, y + 30), font, 3, color, 3)
cv2_imshow(img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Python Selenium Scrapter ( Ubuntu & Jupyter)

### !Selenum latest Version (version4)
- setting url path by "By"

### Ubuntu Code

```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
import os

#def set_chrome_driver():
#    chrome_options = webdriver.ChromeOptions()
#    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#    return driver

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def crawling_img(name):
#     driver = webdriver.Chrome("D:\chromedriver\chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",options=options)
    #driver = set_chrome_driver()
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    elem = driver.find_element(By.NAME,"q")
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)

    #
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")  # 브라우저의 높이를 자바스크립트로 찾음
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 브라우저 끝까지 스크롤을 내림
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element(BY.CSS_SELECTOR,".mye4qd").click()
            except:
                break
        last_height = new_height

    imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    dir = "./before" + "/" + name + "1"
    createDirectory(dir) #폴더 생성
    count = 1
    for img in imgs:
        try:
            img.click()
            time.sleep(2)
            imgUrl = driver.find_element(By.XPATH,
                '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img').get_attribute(
                "src")
            path = "./before" + "/" + name + "1/"
            urllib.request.urlretrieve(imgUrl, path + name + str(count) + ".jpg")
            count = count + 1
            if count >= 1000:
                break
        except:
            pass
    driver.close()
idols = ["white pill bottle"]
for idol in idols:
    crawling_img(idol)

```
### Jupyter Code

```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
import os

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def crawling_img(name):
#     driver = webdriver.Chrome("D:\chromedriver\chromedriver")
    driver = set_chrome_driver()
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    elem = driver.find_element(By.NAME,"q")
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)

    #
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")  # 브라우저의 높이를 자바스크립트로 찾음
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 브라우저 끝까지 스크롤을 내림
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element(BY.CSS_SELECTOR,".mye4qd").click()
            except:
                break
        last_height = new_height

    imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    dir = ".\idols" + "\\" + name
    createDirectory(dir) #폴더 생성
    count = 1
    for img in imgs:
        try:
            img.click()
            time.sleep(2)
            #저장할 이미지 경로 및 
            imgUrl = driver.find_element(By.XPATH,
                '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img').get_attribute(
                "src")
            path = ".\idols" + "\\" + name + "\\"
            urllib.request.urlretrieve(imgUrl, path + name + str(count) + ".jpg")
            count = count + 1
            if count >= 10:
                break
        except:
            pass
    driver.close()
idols = ["white pill bottle"]
for idol in idols:
    crawling_img(idol)
```

### Yolov3 + Live Streaming service

```
import cv2
import numpy as np
from google.colab.patches import cv2_imshow
# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture("http://182.226.36.189:6974/?action=stream")
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("../gdrive/MyDrive/yolov3/yolov3_training_last.weights","cfg/yolov3_training.cfg")

# YOLO NETWORK 재구성
classes = []
with open("./data/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()] 

while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    h, w, c = frame.shape

    # YOLO 입력
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
    True, crop=False)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)
                

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            score = confidences[i]

            # 경계상자와 클래스 정보 이미지에 입력
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5, 
            (255, 255, 255), 1)
    from google.colab.patches import cv2_imshow
    cv2_imshow(frame)

    if cv2.waitKey(100) > 0:
        break

```

#### Result

- 1초당 10 프레임 (10fps)
- 인식 확인

- 보안 사항
    - 인식률, rectablge box 좌표 반환

![image](https://user-images.githubusercontent.com/81907470/192218962-0eaa7221-28d8-4c20-a7fe-9118c33514e6.png)


### Colab에서 YOLO3 학습 참고 자료

- https://periar.tistory.com/236

--- 

## Reference

### Python Scrapter

#### Selenum

- https://dejavuqa.tistory.com/109

#### Ubuntu

- https://oslinux.tistory.com/33

#### Jupyter

- https://velog.io/@jungeun-dev/Python-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81Selenium-%EA%B5%AC%EA%B8%80-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%88%98%EC%A7%91
- https://durian9s-coding-tree.tistory.com/56

### Yolov3 + OpenCV4 + Tesseract OCR

- https://github.com/rnasterofmysea/RaspberryPi4_Yolov3

### Yolov3 + Flask + Background running

- https://kumoh-irl.tistory.com/19
- https://ultrakid.tistory.com/11

### Posenet + Pose estimation

-  https://ivdevlog.tistory.com/2

### Posenet + Dataset << * Chanwon
- https://hongchan.tistory.com/3

### Downgrade Python

- https://velog.io/@bae_mung/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4-4-openCV-tensorflow-%EC%84%B8%ED%8C%85
- https://eun-dolphin.tistory.com/21
- https://installvirtual.com/install-python-3-7-on-raspberry-pi/

### Install tensorflow

- https://www.youtube.com/watch?v=QLZWQlg-Pk0
- https://github.com/PINTO0309/Tensorflow-bin
- https://qengineering.eu/install-tensorflow-2.1.0-on-raspberry-pi-4.html

## Trouble Issues

### (Raspberry Pi 4) SSH connection timeout - fixed

https://sote.tistory.com/249
https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=duehd88&logNo=20201603052
