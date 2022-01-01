# Meal

학교 검색 & 급식 조회 웹 사이트

## 실행 방법

1. 의존성 설치하기

   ```bash
   pip install -r requirements.txt
   ```

2. 환경변수 설치하기

   ```bash
   export redis_url='redis://:<password>@<host>:<port>/<id>'
   export api_key='#'
   ```

   - redis 서버가 없다면 접속 URL 대신 # 을 넣으면 됩니다. 

   - API 키는 [https://open.neis.go.kr](https://open.neis.go.kr)에서 API 키 발급받아야 합니다.

3. 서버 실행하기

   ```bash
   gunicorn -c gunicorn.py
   ```
