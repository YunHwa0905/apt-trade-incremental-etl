# 서울 아파트 실거래가 증분 적재 시스템

> **Apt** (아파트) + **Trade** (실거래) — 매일 쌓이는 서울 아파트 실거래 데이터 ETL & 분석 플랫폼

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-11-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Spring](https://img.shields.io/badge/Spring_Legacy-5.x-6DB33F?style=flat-square&logo=spring&logoColor=white)
![MyBatis](https://img.shields.io/badge/MyBatis-3.5-DC382D?style=flat-square)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-MySQL-2496ED?style=flat-square&logo=docker&logoColor=white)
![Tomcat](https://img.shields.io/badge/Tomcat-9.0-F8DC75?style=flat-square&logo=apachetomcat&logoColor=black)
![GoogleCharts](https://img.shields.io/badge/Google_Charts-Visualization-4285F4?style=flat-square&logo=googlecharts&logoColor=white)

---

## 시스템 흐름도
<img width="885" height="660" alt="image" src="https://github.com/user-attachments/assets/bb738f48-f1d6-45b2-a62b-7afccb7c8740" />



---

## 📌 프로젝트 개요

국토교통부 실거래가 API는 신고 즉시 갱신되는 준-실시간 데이터지만, 부동산 계약은 신고까지 최대 30일의 시차가 있습니다. 이 프로젝트는 "초 단위 실시간"이 아니라 **일 단위 증분 수집**으로 설계하여, 매일 같은 데이터를 재조회해도 중복 없이 신규 신고분만 쌓이도록 만들었습니다.

| 항목 | 내용 |
|---|---|
| 서비스명 | apt-trade-incremental-etl |
| 개발 유형 | 실거래가 ETL 파이프라인 + 분석 + 웹 조회 시스템 |
| 데이터 출처 | 국토교통부 아파트 매매 실거래가 상세 자료 (공공데이터포털) |
| 수집 범위 | 서울 25개 자치구, 2023년 1월 ~ 현재 (매일 갱신) |
| 주요 기술 | Python ETL, MySQL, Spring Legacy, MyBatis, Google Charts |

---

## 🔧 기술 스택

### ETL / 분석
| 항목 | 내용 |
|---|---|
| 언어 | Python 3.12 |
| 수집 | requests |
| DB 연동 | pymysql |
| 환경변수 | python-dotenv |
| 스케줄링 | crontab (WSL Ubuntu) |

### Backend
| 항목 | 내용 |
|---|---|
| 프레임워크 | Spring Legacy (Spring MVC) |
| 포트 | 8181 |
| ORM | MyBatis |
| DB | MySQL 8.0 |
| WAS | Apache Tomcat 9.0 |
| 빌드 | Maven |

### Frontend
| 항목 | 내용 |
|---|---|
| 뷰 | JSP / JSTL |
| 시각화 | Google Charts (ComboChart) |
| 통신 | Ajax (Jackson JSON) |

---

## 📊 분석 로직

원본 실거래 데이터(`apt_trade`)를 기반으로 세 가지 분석 배치를 수행합니다.

| 구분 | 처리 방식 | 결과 테이블 |
|---|---|---|
| 가격 추이 | 지역+연/월 단위 평균가·평당가 집계, 전월대비 변동률 계산. 서울 전체 추이는 거래건수 가중평균 적용 | monthly_price_summary |
| 신고가/신저가 | 단지별 거래일 순 추적, 직전 최고/최저가 경신 여부 판정 | new_high_low_history |
| 이상거래 탐지 | 같은 단지+같은 월 평균 평당가 대비 ±30% 이상 편차 거래 탐지 (최소 샘플 3건 미달 단지는 제외) | outlier_trade |

분석 배치는 모두 증분 처리됩니다. 이미 판정이 끝난 거래는 재검사하지 않고 신규로 적재된 거래만 처리하여, 매일 재실행해도 안전하고 빠르게 동작합니다.

---

## 📁 프로젝트 구조

```
apt-trade-incremental-etl/
├── etl/                             # Python ETL
│   ├── collector/
│   │   ├── api_client.py            # API 호출
│   │   ├── parser.py                # 응답 파싱, dedup_key 생성
│   │   └── region_codes.py          # 서울 25개구 법정동코드
│   ├── db/
│   │   ├── connection.py            # MySQL 커넥션
│   │   ├── repository.py            # 증분 적재 (INSERT IGNORE)
│   │   └── schema.sql               # DDL
│   ├── analysis/
│   │   ├── price_trend.py           # 가격추이 집계
│   │   ├── new_high_low.py          # 신고가/신저가 탐지
│   │   └── outlier_detect.py        # 이상거래 탐지
│   ├── backfill.py                  # 과거 데이터 일괄 백필
│   ├── backfill_progress.py         # 백필 진행상태 추적
│   ├── run_daily.py                 # 일별 증분 수집 (crontab)
│   ├── run_analysis.py              # 분석 배치 통합 실행 (crontab)
│   └── requirements.txt
├── web/                             # Spring Legacy 백엔드
│   ├── src/main/java/com/apttrade/web/
│   │   ├── controller/              # TradeController, PriceTrendController, DetectionController
│   │   ├── service/
│   │   ├── mapper/
│   │   └── vo/
│   ├── src/main/resources/
│   │   └── mapper/                  # MyBatis XML
│   ├── src/main/webapp/WEB-INF/
│   │   ├── web.xml
│   │   ├── spring/
│   │   └── views/
│   └── pom.xml
└── README.md
```

---

## 🗄️ 데이터 모델

### MySQL — `apt_trade` 테이블

| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | BIGINT (PK) | 자동 증가 |
| dedup_key | VARCHAR (UNIQUE) | 중복판별 키 (법정동+지번+단지명+동+층+면적+계약일+금액) |
| sgg_cd | VARCHAR | 법정동코드 (구 단위) |
| apt_nm | VARCHAR | 단지명 |
| deal_date | DATE | 계약일 |
| deal_amount | BIGINT | 거래금액(만원) |
| price_per_pyeong | DECIMAL | 평당가(만원), ETL에서 계산 |
| dealing_gbn | VARCHAR | 거래유형(중개/직거래) |
| sler_gbn / buyer_gbn | VARCHAR | 매도자/매수자 구분 |
| is_outlier | BOOLEAN | 이상거래 플래그 |

### MySQL — 분석 결과 테이블

| 테이블 | 설명 |
|---|---|
| monthly_price_summary | sgg_cd + 연/월 단위 평균가, 평당가, 거래건수, 전월대비 변동률 |
| new_high_low_history | apt_trade_id 참조, HIGH/LOW 구분, 경신 시점 평당가 |
| outlier_trade | apt_trade_id 참조, 단지 평균 평당가 대비 편차율 |

> 데이터 출처: 국토교통부 아파트 매매 실거래가 상세 자료 (data.go.kr)

---

## 🚀 실행 방법

### 1. MySQL 실행 (Docker)

```bash
docker run -d --name apt-trade-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=<비밀번호> mysql:8.0
docker exec -i apt-trade-mysql mysql -u root -p < etl/db/schema.sql
```

### 2. ETL (Python)

```bash
cd etl
pip install -r requirements.txt --break-system-packages
cp .env.example .env   # SERVICE_KEY, DB 접속정보 입력
python3 backfill.py        # 과거 데이터 백필 (최초 1회)
python3 run_analysis.py    # 분석 배치 실행
```

### 3. 백엔드 (Spring Legacy)

```bash
cd web
# STS에서 Maven 프로젝트로 열기
# src/main/resources/db.properties에 DB 접속정보 입력
# Tomcat에 배포
# 포트: 8181
```

### 4. 화면 접속

- 실거래 목록: http://localhost:8181/web/trade/list
- 가격 추이: http://localhost:8181/web/price-trend
- 신고가/신저가: http://localhost:8181/web/detection/high-low
- 이상거래: http://localhost:8181/web/detection/outlier

---

## 🖥️ 개발 환경

| 항목 | 버전 / 내용 |
|---|---|
| OS | Windows 11 + WSL Ubuntu 24.04 |
| Python | 3.12 |
| JDK | 11 (Eclipse Adoptium) |
| Spring Framework | 5.3.x (Legacy MVC) |
| MyBatis | 3.5.13 |
| Maven | 3.x |
| Tomcat | 9.0.118 |
| Docker | MySQL 8.0 컨테이너 |
| IDE | STS (Spring), VS Code (Python) |

---

## ✅ 구현 완료 목록

- [x] 국토부 실거래가 API 연동 및 JSON 파싱
- [x] dedup_key 기반 증분 적재 (UNIQUE 제약 + INSERT IGNORE)
- [x] 서울 25개구 × 2년 6개월 백필 (141,366건)
- [x] crontab 기반 일별 증분 수집 (신고 지연 보정: 이번달+지난달 재조회)
- [x] 가격추이 / 신고가신저가 / 이상거래 분석 배치 (전체 증분 처리)
- [x] Spring Legacy + MyBatis 웹 애플리케이션
- [x] 실거래 목록 검색/페이지네이션 화면
- [x] Google Charts 기반 가격추이 시각화 (지역별 선택, 서울 전체 가중평균)
- [x] 이상거래 정렬 옵션(편차율/거래일순) 및 구이름 표시
- [x] crontab 분석 배치 자동화 (수집 09:00 → 분석 09:30)

---

## ⚠️ 알려진 이슈

| 이슈 | 상태 | 비고 |
|---|---|---|
| 신용잔고/전세가율 등 추가 지표 미수집 | 개선 예정 | 국토부 전월세 API 연동 검토 중 |
| 화면 단위 테스트 코드 부재 | 개선 예정 | Controller/Service 단위 테스트 추가 검토 |
| ERD 다이어그램 미작성 | 개선 예정 | mermaid.js 기반 ERD 추가 검토 |
| WSL ↔ Windows 환경 전환 시 DB 인증 이슈 재발 가능 | 확인 필요 | 동일 실행 환경 유지 권장 |

---

## 📚 학습 내용

| 분야 | 핵심 학습 내용 |
|---|---|
| ETL 설계 | 고유 ID가 없는 외부 API 데이터의 증분 적재 키 설계, UNIQUE 제약 기반 중복 방지 |
| 데이터 정합성 | 신고 지연(최대 30일)을 고려한 재조회 전략, 동일 키 충돌 시 일련번호 부여로 데이터 손실 방지 |
| 분석 설계 | 단순 평균과 가중평균의 차이, 비교 기준(구 단위 vs 단지 단위) 변경에 따른 이상치 탐지 정확도 개선(46,058건→496건) |
| Spring Legacy | MyBatis 동적 SQL(`<choose>`, `<if>`), root/servlet 다중 컨텍스트 구조, MapperScannerConfigurer 설정 |
| 배포/운영 | crontab을 활용한 ETL-분석 파이프라인 자동화, 단계적 실행 순서 설계(수집 → 분석) |
| 트러블슈팅 | Spring 빈 생성 실패 원인 추적, MySQL 인증 플러그인 이슈 대응, API 엔드포인트 오인 문제 해결 |

---

## 🖼️ 화면 예시

### 실거래 목록
<img width="700" alt="실거래 목록" src="https://github.com/user-attachments/assets/3f086f3f-a5d5-482d-87be-0bf2d957deaf" />

### 가격 추이
<img width="700" alt="가격 추이" src="https://github.com/user-attachments/assets/6113c10b-1109-4df3-bd19-f8bf72c5b86b" />

### 신고가 / 신저가
<img width="700" alt="신고가 신저가" src="https://github.com/user-attachments/assets/df500d38-9f26-4a3a-ab00-c5604f5f86d2" />

### 이상거래 탐지
<img width="700" alt="이상거래 탐지" src="https://github.com/user-attachments/assets/0a43f8db-72da-49c1-9c0f-08a027740ab9" />

---

## 👥 팀 구성

> 1인 개발

---
