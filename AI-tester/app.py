from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# 현재 파일의 경로를 기준으로 feature/AI-01 디렉토리 경로를 sys.path에 추가하여 model 모듈을 임포트할 수 있도록 설정
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'feature', 'AI-01')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'feature', 'AI-01')))
import model

app = FastAPI()
classifier = model.SpamClassifier()
classifier.initmodel()

category = model.Category()
category.initmodel()

class MessageRequest(BaseModel):
    message: str


# API 엔드포인트 정의
@app.post("/is_spam")
async def check_spam(request: MessageRequest):
    result = classifier.is_spam(request.message)
    if result is None:
        raise HTTPException(status_code=500, detail="스미싱 판별 중 오류가 발생했습니다.")
    return {"message": request.message, "is_spam": result}

@app.post("/input")
async def input_to_standard(request: MessageRequest):
    result = classifier.get_Category(request.message)
    if result is None:
        raise HTTPException(status_code=500, detail="카테고리화 중 오류가 발생했습니다.")
    return {"message": result}


# 테스트용 엔드포인트
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# FastAPI 애플리케이션 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)