import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 현재 날짜와 요일 가져오기
now = datetime.datetime.now()
today = now.date()

# 요일 텍스트 매핑
DAYS = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
current_weekday_text = DAYS[now.weekday()]

# API 키 설정
API_KEY = os.getenv("OPENAI_API_KEY_FOR_STANDARDIZATION")
client = OpenAI(api_key=API_KEY)

def json_to_key_value_text(schedule_json):
    """JSON 데이터를 키-값 텍스트 나열 형식으로 변환"""
    schedule = schedule_json[0]
    return "\n".join([f"{key}: {value}" for key, value in schedule.items()])

def get_weekday(date_string):
    """날짜 문자열로부터 요일 텍스트 반환"""
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    return DAYS[date.weekday()]

def create_gpt_prompt(schedule_json):
    """GPT에게 전달할 프롬프트 생성"""
    command = json_to_key_value_text(schedule_json)
    booked_day = schedule_json[0]["schedule_start_time"][:10]
    booked_day_text = get_weekday(booked_day)
    
    return [
        {"role": "system", "content": f"당신은 고객의 개인 비서입니다. 오늘은 {today}, {current_weekday_text}입니다. 다음의 예약 정보를 받아 고객에게 설명하세요. 예약된 요일은 {booked_day_text}입니다. 연도 정보는 빼도 괜찮습니다. 부드럽고 친절한 말투로, 일상적인 용어를 써서 짧고 간결하게 설명하세요."},
        {"role": "user", "content": command},
    ]

def get_gpt_response(schedule_json):
    """GPT 모델 호출 및 응답 반환"""
    messages = create_gpt_prompt(schedule_json)
    print(messages)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content.strip()

# 예시 JSON 데이터
schedule_json = [
    {
        "schedule_id": 1,
        "schedule_name": "신경외과 예약",
        "schedule_start_time": "2024-08-30T13:05:01",
        "schedule_description": "병원 예약",
        "user_id": 1
    }
]

# GPT의 응답 출력
gpt_message = get_gpt_response(schedule_json)
print(gpt_message)