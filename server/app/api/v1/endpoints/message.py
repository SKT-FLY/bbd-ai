from fastapi import APIRouter, HTTPException
from app.feature.func02.model import MessageAnalyzer
from app.schemas.message import MessageRequest

router = APIRouter()

# 이 엔드포인트는 여러 개의 메시지를 받아서 처리할 수 있습니다.
@router.post("/analyzed_message")  # 처리된 데이터를 문자열 리스트로 반환
async def get_analyzed_message(request: MessageRequest):
    model = MessageAnalyzer()
    model.initmodel()
    result = model.get_summary(request.message)
    if result is None :
        raise HTTPException(status_code=500, detail="스미싱 판별 중 오류가 발생했습니다.")
    return await {"message": result}