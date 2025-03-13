## 프로젝트 소개

<img src="https://github.com/user-attachments/assets/d8c87553-e1ed-44f0-8d1e-cbfaa4358ec2" />

### 유노유노후는 노후 계획을 세우는 사람들을 위한 개인 맞춤형 지역 및 여가시설 추천 서비스입니다.


- 몇몇 중장년층 사람들은 정보 부족 등의 문제로 은퇴 후 자신이 노후에 지낼 곳을 정하고 계획하는 것을 어려워합니다.
- 이러한 은퇴 후 어디서, 어떻게 보내야할지에 대한 정보가 필요한 사람들을 대상으로, **노후 라이프스타일 맞춤 지역 추천 및 정보를 제공하는 서비스** 입니다.

https://youknowhoknow.netlify.app/



## 기능 
### 주요 기능

|<img src="https://github.com/user-attachments/assets/1941ceac-f150-4b53-8c25-76ee62ed44f3" />|<img src="https://github.com/user-attachments/assets/9c56ed1e-1d6a-4eb4-8c14-15bed012c46e" />|
|:---:|:---:|
|**노후 지역 찾기** 탭에서는 유저의 라이프스타일 선호 키워드를 바탕으로 노후에 살 지역을 지도로 추천해줍니다.|해당 지역의 주변 시설들에 대한 위치와 정보를 보여줍니다.|



### 서브 기능

|![image](https://github.com/user-attachments/assets/a74223c4-1d67-4e83-bf7c-1e0540e50d95)|<img alt="image" src="https://github.com/user-attachments/assets/9781674b-eb88-4df4-a853-09dc2c3f515b" >|
|:---:|:---:|
|지역에서 선택한 시설 및 인프라에 대한 정보를 확인할 수 있습니다.|**지역 Q&A** 탭에서 지역의 거주민에게 원하는 지역에 대한 질문을 남길 수 있습니다.유저는 자신의 지역에 대한 질문에 답변을 남길 수 있습니다.|
||
|<img alt="image" src="https://github.com/user-attachments/assets/8490427e-3600-4c7c-848a-add8ee6d0a9d" >|<img src="https://github.com/user-attachments/assets/9edd420c-aae9-4228-83ef-b4a1593c1c9e" />|
| **지역 생활** 탭에서는 지역에 대한 거주민의 생생한 리뷰를 확인할 수 있습니다.|유저 또한 자신이 사는 지역에 대한 리뷰를 남길 수 있습니다.|
||
|<img src="https://github.com/user-attachments/assets/3e9e6033-4654-4695-96a0-55bdb220d9d0" />|<img alt="image" src="https://github.com/user-attachments/assets/7f0e11cc-6406-4023-86d9-e798422d469d" />|
|추천된 지역에서 원하는 시설을 장바구니에 담으면 한 달치 여가 비용을 계산해주고, 생활비를 바탕으로 한 내 적정 여가 비용과 비교하여 적정한지 판단합니다.|여가비용 확인 후 구체적인 미래를 그릴 수 있도록 노후 계획 작성을 도와줍니다.|
||
<img alt="image" src="https://github.com/user-attachments/assets/a8d165e7-55d8-488f-a4a6-024f142c9c2a">|<img alt="image" src="https://github.com/user-attachments/assets/036635ff-1476-42a8-aadb-ebcaa38d93f1" >
|시설, 인프라에 대한 리뷰 확인할 수 있고, 유저 또한 리뷰를 남길 수 있습니다.|원하는 지역 및 시설과 인프라를 저장하여 마이페이지에서 확인할 수 있습니다.|





## 기술 스택

- **개발 환경**
  - Visual Studio Code
  - Git / GitHub

- **Config**
  - NPM (Node Package Manager)

- **Backend Framework**
  - Django framework
  - MySQL
  - AWS RDS, S3, EC2
  - Gunicorn, nginx

- **Communication Tools**
  - Slack
  - Notion
  - Google Meet

## 담당 파트

- **기획**: 김시연
- **디자인**: 최윤경
- **백엔드**: 박연우, 박예빈
- **프론트엔드**: 황인영, 안예현

## 프로젝트 아키텍처

프로젝트는 클라이언트-서버 구조로 구성되어 있습니다.

### 1. **프론트엔드**
   - React를 사용하여 구성된 SPA(Single Page Application)입니다.
   - 주요 기능: 사용자 인터페이스(UI)와 사용자 경험(UX)을 담당하며, 백엔드에서 제공하는 API를 통해 데이터를 받아와 화면에 렌더링합니다.
   - 상태 관리: React의 상태 관리 기능을 사용합니다.

### 2. **백엔드**
   - 백엔드 서버는 Django 로 RESTful API를 제공하며, 프론트엔드 애플리케이션과 JSON 형식으로 데이터를 주고받습니다.
   - 데이터베이스와 연동하여 작업을 처리합니다. AWS S3에 이미지 정적 파일을 저장합니다.
   
### 3. **통신**
   - 프론트엔드와 백엔드는 HTTP/HTTPS 프로토콜을 통해 통신합니다.
   - API 호출은 주로 Axios 또는 Fetch API를 사용하여 비동기적으로 처리됩니다.
