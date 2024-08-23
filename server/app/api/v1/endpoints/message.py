from fastapi import APIRouter, HTTPException
from app.feature.messageanalyzer.model import MessageAnalyzer
from app.schemas.message import MessageRequest, MessageRespond

router = APIRouter()

# 이 엔드포인트는 여러 개의 메시지를 받아서 처리할 수 있습니다.
@router.post("/analyzed_message")  # 처리된 데이터를 문자열 리스트로 반환
async def get_analyzed_message(request: MessageRequest):
    model = MessageAnalyzer()
    result = model.get_summary(request.message)
    if result is None :
        raise HTTPException(status_code=500, detail="문자 분석 중 오류가 발생했습니다.")
    
    # result를 파싱하여 MessageRespond 형식으로 변환
    try:
        lines = result.split("\n")
        parsed_data = {
            "source": lines[0].split(" : ")[1].strip(),
            "date": lines[1].split(" : ")[1].strip(),
            "message_type": lines[2].split(" : ")[1].strip(),
            "reason": lines[3].split(" : ")[1].strip(),
            "summary": lines[4].split(" : ")[1].strip()
        }

        response_data = MessageRespond(**parsed_data)
        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메시지 파싱 중 오류가 발생했습니다: {str(e)}")

