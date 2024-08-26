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

        # MessageRespond 인스턴스 생성
        return MessageRespond(
            source=source,
            date=date_str,
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


if __name__ == "__main__":
    text = """

    [Web발신]
안녕하세요, 소프트웨어융합대학 교학팀입니다.
2023학년도 후기 졸업대상자 학위증 배부 참석 여부 조사 안내드립니다.

1.설문조사 기간: ~8/13(화) 16:00까지
2.배부날짜: 8/21(수) 
3.장소: 미래관 429호 자율주행스튜디오
4.배부시간 : 10:00 ~ 11:30 / 13:30 ~ 15:30 (시간엄수)

 
* 아래 링크를 통해 참석 여부를 알려주시기 바랍니다(불참시에도 설문조사 참여 필수)
> https://forms.gle/QFSqNNvoq77x7N356


*학위복 대여 사전신청(~8/14) 관련해서는 학사공지를 확인해주시기 바랍니다.(
 (https://cs.kookmin.ac.kr/news/notice/)
 >사전예약기간 내 미신청시 당일 절대 대여불가

감사합니다.
소프트웨어융합대학 교학팀
    
    """

    print(get_analyzed_message(text))