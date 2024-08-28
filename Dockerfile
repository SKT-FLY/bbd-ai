# 베이스 이미지로 Python 3.9 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /workspace/server

# 의존성 파일 복사
COPY requirements.txt .

# 의존성 설치ru
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스 코드 복사
COPY . /workspace

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
