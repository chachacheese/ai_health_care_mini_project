# 🩺 FastAPI + Tortoise ORM 기반 AI Health Care 
> 본 레포는 오즈코딩스쿨 AI 헬스케어 심화반 실습 프로젝트를 Fork하여  
> 제가 구현한 기능 중심으로 재구성한 버전입니다.
ORM 모델 정의, DB 연결, CRUD 작성 등 백엔드의 핵심 흐름을 직접 경험하는 것을 목표로 하였습니다.

---

## 🚀 프로젝트 개요
- FastAPI로 비동기 서버 환경 구성  
- Tortoise ORM을 사용한 모델 정의 및 SQLite 연동  
- 건강 기록(Exercise / Meal / Sleep / Water)에 대한 기본 CRUD 구현  
- `pages`(HTML 반환) 라우팅 구조 일부 작성  
- DB 초기화 및 스키마 자동 생성 흐름 이해  

## ✨ 프로젝트 특징
- FastAPI Router를 활용하여 페이지 라우트(pages)와 API 라우트(api)를 분리
- Tortoise ORM으로 모든 테이블을 비동기 방식으로 CRUD 처리
- 간단한 웹 UI(대시보드)를 통해 건강 데이터 조회 가능
- 라우터 → 서비스 → ORM 모델로 이어지는 계층 구조 이해
---

## 🧱 구현된 주요 기능
### ✔ 데이터베이스 & ORM  
- Tortoise ORM 기반 Exercise, Meal, Sleep 모델 정의  
- SQLite 연결 
- 비동기 환경에서 ORM 조작 테스트

### ✔ 라우팅 구성  
- `/pages/*` : 템플릿/HTML 반환용 라우트 일부 구현  

### ✔ CRUD 구현  
- Exercise / Meal / Sleep CRUD 

---
```
## 📁 프로젝트 구조 (내가 구현한 부분만 요약)

app/
 ├── 📦 db.py                 # Tortoise ORM 초기화 및 DB 설정
 ├── 🧬 models/               # User · Exercise · Meal · Sleep · Water 모델 정의
 │    ├── exercise.py
 │    ├── meal.py
 │    ├── sleep.py
 │    └── water.py            #강사님이 참고하라고 알려주신 파일
 └── 🌐 routers/        
      └── pages.py         # 대시보드 일부,HTML 반환 라우트 일부 구현
```

---

## 🛠 사용 기술
- **FastAPI** — 비동기 웹 프레임워크  
- **Tortoise ORM** — 비동기 ORM(모델 정의 및 DB 조작)
- **SQLite** — 경량 데이터베이스  
- **Uvicorn** — Fast API 실행용 ASGI 서버  
- **Pydantic** — 요청/응답 데이터 검증  

---

## 📚 학습 포인트
- 비동기 웹 서버 환경 이해 (Async / Await 패턴)  
- ORM을 사용한 데이터베이스 모델링  
- FastAPI 라우팅 구조 설계(pages/api 분리 방식 경험)  
- 기본 CRUD 작성 및 API 테스트  
- DB 초기화 및 스키마 자동 생성 과정 이해  

---

## 🔧 실행 방법

### 1. 가상환경 생성 및 패키지 설치
pip install -r requirements.txt
### 2. 서버 실행
uvicorn app.main:app --reload

---

## 📬 Contact  
- Velog: https://velog.io/@jiiiin0  
- Email: oz.data.88@gmail.com
- GitHub: https://github.com/chachacheese
---
