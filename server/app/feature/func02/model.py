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
MMS 스팸신고[Web발신](광고)경자년 지나고 새로운 신축년이 밝았습니다올해들어 최고의 선택은 이것 아닐까요?반갑습니다 박건희대표 입니다2021년도 새해복 많이받으세요요즘같은 힘든시기 대책방안을 마련했습니다.주부님들 사이에서 유행중인 재.테.크은행 직원들도 진행하는 목돈마련남들보다 한걸음 더 앞서는게 가장 중요합니다처음이신분들도 환영합니다.원.금보.장 재.테.크50~60대분들도 이용하는 쉽고 편리한 투 자방식상담문의hxxp://click.gl/X3y2u2무료거부 **********

    """

    summary = MessageSummary(prompt)
    summary.initmodel()
    print(summary.get_summary(text))
