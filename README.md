
# diary-project
OZ 8기 미니 프로젝트 - 다이어리 페이지 만들기

## 📌 프로젝트 소개
Diary Project는 사용자가 자신의 감정을 기록하고, 태그를 추가하여 다양한 필터링이 가능하도록 설계된 웹 애플리케이션입니다.
현재 Users(사용자)와 Diaries(일기) 모델을 정의한 상태이며, Diary_tags(일기-태그 관계)는 추후 구현 예정입니다.

---
## 📂 ERD (데이터베이스 구조)

아래는 현재 프로젝트의 데이터베이스 구조를 나타낸 ERD(Entity Relationship Diagram)입니다.

![image](https://github.com/user-attachments/assets/7c67a379-084d-4889-a65d-b36cdfa52a2c)

현재 Users(사용자)와 Diaries(일기) 테이블이 구현된 상태이며, Diary_tags(일기-태그 관계)는 추후 개발 예정입니다.

---


#### 1️⃣ 사용자 모델 (Users)

현재 AbstractUser를 상속한 커스텀 유저 모델을 사용하고 있으며, 이메일 기반 로그인 방식을 지원합니다.

#### 2️⃣ 일기 모델 (Diaries)

사용자가 작성한 일기 정보를 저장하는 테이블입니다.
mood 필드는 ENUM 형태로 감정 상태를 저장하며, user 필드는 ForeignKey를 사용하여 User 모델과 연결됩니다.

___
🚀 진행 예정 (Diary_tags 모델 추가 예정)

현재 Diary_tags 모델(일기-태그 관계)은 아직 구현되지 않았으며, 이후 개발할 예정입니다.
추가 개발 시, Diary와 Tag 모델을 ManyToManyField로 연결할 계획입니다.
___

## ⚙️ 기술 스택
- **Backend:** Python, Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **ORM:** Django ORM
- **Authentication:** Django Authentication System
- **Deployment:** AWS EC2, Docker
- **Version Control:** Git, GitHub

---
