import openai
import os
from dotenv import load_dotenv
from app.feature.voicescheduling import setting

prompt=setting

class VoiceScheduler:
    def __init__(self, prompt=prompt):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')

        if self.api_key is None:
            raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

        openai.api_key = self.api_key
        self.max_tokens = 70
        self.model_settings = {
            "model": prompt.model,
            "role_message": {
                "role": "system",
                "content": prompt.system_setting
            }
        }


    def get_scheduling(self, data: str) -> str:
        try:
            response = openai.chat.completions.create(
                model=self.model_settings["model"],
                messages=[
                    self.model_settings["role_message"],
                    {"role": "user", "content": data}
                ],
                temperature=0,
                max_tokens=self.max_tokens
            )

            result = response.choices[0].message.content
            return result
        except openai.error.OpenAIError as e:
            print(f"OpenAI API 오류: {e}")
            return "오류 발생"


if __name__ == "__main__" : 
    text = "나 8월 31일에 노인정에 방문해야해"
    model = VoiceScheduler()
    print(model.get_scheduling(text))