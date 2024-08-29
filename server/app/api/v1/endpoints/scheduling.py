from fastapi import APIRouter, HTTPException
from app.feature.voicescheduling.model import VoiceScheduler
from app.schemas.schedule import ScheduleRespond, ScheduleRequest
from datetime import datetime

router = APIRouter()

def parse_message(message: str) -> ScheduleRespond:
    try:
        # 고정된 키워드를 기준으로 파싱
        when = message.split("1. 언제 :")[1].split("\n")[0].strip()
        summary = message.split("2. 요약 :")[1].strip()

        # MessageRespond 인스턴스 생성
        return ScheduleRespond(
            when=when,
            description=summary
        )

    except (IndexError, ValueError) as e:
        raise ValueError(f"메시지를 파싱하는 중 오류가 발생했습니다: {e}")

# 이 엔드포인트는 여러 개의 메시지를 받아서 처리할 수 있습니다.
@router.post("/scheduled_voice")  # 처리된 데이터를 문자열 리스트로 반환
async def get_analyzed_message(request: ScheduleRequest):
    model = VoiceScheduler()
    result = model.get_scheduling(request.message)
    if result is None :
        raise HTTPException(status_code=500, detail="예약 등록 중 오류가 발생했습니다.")
    parsed_result = parse_message(result)

    return parsed_result


if __name__ == "__main__":
    text = "나 8월 31일에 노인정 방문해야해"

    print(get_analyzed_message(text))