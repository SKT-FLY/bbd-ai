import openai
import os
from dotenv import load_dotenv
import time
from app.feature.func02 import prompt

prompt=prompt

class MessageAnalyzer:
    def __init__(self, prompt=prompt):
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
