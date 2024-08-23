from fastapi import APIRouter, HTTPException
from app.feature.messageanalyzer.model import MessageAnalyzer
from app.schemas.message import MessageRequest, MessageRespond
from datetime import datetime

router = APIRouter()

def parse_message(message: str) -> MessageRespond:
    try:
        # 고정된 키워드를 기준으로 파싱
        source = message.split("1. 보낸 출처 :")[1].split("\n")[0].strip()
        date_str = message.split("2. 날짜 :")[1].split("\n")[0].strip()
        message_type = message.split("3. 문자 종류 :")[1].split("\n")[0].strip()
        summary = message.split("4. 요약 :")[1].strip()

        # 날짜를 datetime 객체로 변환
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

        # MessageRespond 인스턴스 생성
        return MessageRespond(
            source=source,
            date=date,
            message_type=message_type,
            summary=summary
        )

    except (IndexError, ValueError) as e:
        raise ValueError(f"메시지를 파싱하는 중 오류가 발생했습니다: {e}")


# 이 엔드포인트는 여러 개의 메시지를 받아서 처리할 수 있습니다.
@router.post("/analyzed_message")  # 처리된 데이터를 문자열 리스트로 반환
async def get_analyzed_message(request: MessageRequest):
    model = MessageAnalyzer()
    result = model.get_summary(request.message)
    if result is None :
        raise HTTPException(status_code=500, detail="문자 분석 중 오류가 발생했습니다.")
    parsed_result = parse_message(result)

    return parsed_result
