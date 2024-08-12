import openai
import os
from dotenv import load_dotenv
import prompt
import time

prompt = prompt

class MessageSummary:
    def __init__(self, prompt):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')

        if self.api_key is None:
            raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

        openai.api_key = self.api_key
        self.max_tokens = 150
        self.model_settings = {
            "model": prompt.model,
            "role_message": {
                "role": "system",
                "content": prompt.system_setting
            }
        }

    def initmodel(self):
        try:
            response = openai.chat.completions.create(
                model=self.model_settings["model"],
                messages=[self.model_settings["role_message"]],
                temperature=0
            )
            return response
        except openai.error.OpenAIError as e:
            print(f"OpenAI API 오류: {e}")
            return None

    def get_summary(self, data: str) -> str:
        try:
            start_time = time.time()  # Start time
            response = openai.chat.completions.create(
                model=self.model_settings["model"],
                messages=[
                    self.model_settings["role_message"],
                    {"role": "user", "content": data}
                ],
                temperature=0,
                max_tokens=self.max_tokens
            )

            end_time = time.time()  # End time
            elapsed_time = end_time - start_time  # Calculate elapsed time

            result = response.choices[0].message.content
            print(f"Summary generation time: {elapsed_time:.2f} seconds")  # Print elapsed time
            return result
        except openai.error.OpenAIError as e:
            print(f"OpenAI API 오류: {e}")
            return "오류 발생"

# 테스트 코드
if __name__ == "__main__":
    text = """
[서울성모병원 진료예약 확인 알림]
- 문*숙 님 / 등록번호: 30756112
- 일자: 2024년09월19일(목요일)
- 시간: 10시44분
- 본관 2층 척추센터 정형외과  김영훈  선생님   
문의 및 예약변경 시 1588-1511로 연락주세요.  
카카오톡이 아닌 기존처럼 문자로 받길 원하실 경우에는 우측상단의 "알림톡 받지 않기"를 눌러주시기 바랍니다.
    """

    summary = MessageSummary(prompt)
    summary.initmodel()
    print(summary.get_summary(text))
