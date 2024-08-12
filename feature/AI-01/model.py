import openai
import os
from dotenv import load_dotenv

class SpamClassifier:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')

        if self.api_key is None:
            raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

        openai.api_key = self.api_key

        self.model_settings = {
            "model": "gpt-4o-mini",
            "role_message": {
                "role": "system",
                "content": "너는 보안을 담당하고 스미싱이라는 스팸 문자 데이터들을 분류하는 역할을 할꺼야. 앞으로 너가 받는 문자 데이터들을 분석해서 스미싱 데이터인지 아닌지 판별해줘. 응답은 '예' 또는 '아니오' 형태로만 해줘."
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

    def is_spam(self, data: str) -> str:
        try:
            response = openai.chat.completions.create(
                model=self.model_settings["model"],
                messages=[
                    self.model_settings["role_message"],
                    {"role": "user", "content": data}
                ],
                temperature=0
            )

            result = response.choices[0].message.content
            return result
        except openai.error.OpenAIError as e:
            print(f"OpenAI API 오류: {e}")
            return "오류 발생"

# 테스트 코드
if __name__ == "__main__":
    text = """
[Web발신]
경품이벤트 재차 안내
문*숙님! 건강보험공단 과천지사 (T02-6942-0144_)입니다. 
문*숙님은 2024년 대장암(본인부담없음) 검진 대상자입니다. 
지금, 암검진받고  과천지사를 방문하시면 선착순으로 경품을 드립니다.
서두르세요!
○ 이벤트명: 국가암 검진받고, 선물도 받으세요~
○ 기간: 24년6월17일부터 경품 소진시까지
○ 경품: 친환경주방세제
○ 참가 방법: 대장암(본인부담없음) 검진을 받고 국민건강보험공단 과천지사로 내방  
   단, 개별종합검진 등 개인적으로 검진 받으신 분은 제외됩니다.
▶ 경품 수령 장소: 국민건강보험공단 과천지사 보험급여팀 (과천시 별양상가1로 13 교보빌딩4층 국민건강보험공단)
▶ 관련 문의: 국민건강보험공단 과천지사 T02-6942-0144
    """

    classifier = SpamClassifier()
    classifier.initmodel()
    print(classifier.is_spam(text))
