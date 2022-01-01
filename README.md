# Meal

학교 검색 & 급식 조회 웹 사이트

## 실행 방법

1. 의존성 설치하기

   ```bash
   pip install -r requirements.txt
   ```

2. 환경변수 설치하기
   1. `.env` 파일 생성해주세요.
   2. `.env` 파일에 다음과 같은 내용을 추가해주세요.
      ```text
      redis_url = redis://:<password>@<host>:<port>/<id>
      api_key = #
      ```
   3. redis 서버가 없다면 접속 URL 대신 # 을 넣으면 됩니다. 
   4. API 키는 [https://open.neis.go.kr](https://open.neis.go.kr)에서 API 키 발급받아야 합니다.

3. 서버 실행하기

   ```bash
   gunicorn -c gunicorn.py
   ```

## 시

본 프로그램에는 윤동주 시인과 이육사 시인의 시가 포함되어 있습니다.
