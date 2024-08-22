import openai
import os
from dotenv import load_dotenv

class Categroy:
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
                "content": "너는 지금부터 문자 데이터들을 요약하는 역할을 할꺼야. 너가 받은 문자 데이터를 바탕으로 "
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

    def get_Category(self, data: str) -> str:
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
김*현 회원님, 
정기결제로 생활요금 간편하게 납부하시고, 최대 2만5천원 청구할인 혜택도 받아보세요

[혜택]
- 혜택 신청 후 생활요금 정기결제 신규 신청 시, 항목별 최대 5천원 청구할인(최대 2만5천원)
▶ 혜택 상세 확인: bit.ly/4dbUdAI

[기간]
2024/08/01 ~ 08/31

[대상카드]
모든 현대카드 (법인·체크·하이브리드·GIFT 카드 제외, 4대 보험은 가족카드 제외)

· 이벤트 시작일 직전 1년간 현대카드로 신청 항목 정기결제 이용 이력이 없는 회원에 한함
· 1년 내 이용한 정기결제 이력은 앱>메뉴>카드관리>생활 요금 결제 등록>정기결제에서 확인
· 기간 내 혜택 참여 및 정기결제 신청 완료한 본인 회원에 한해 제공(정기결제 항목 별 1회 혜택 제공)
· 자세한 이용방법은 혜택 신청 후 발송되는 문자메시지 참고
· 혜택 제공 시점에 신청 항목 정기결제 유지 필수(카드 해지·정지·탈회 시 제공 불가하며, 마케팅 동의한 회원에 한해 혜택 제공)
· 당사에서 진행하는 다른 정기결제 이용유도 이벤트와 동일 항목 중복 수혜 불가

>상환 능력에 비해 신용카드 이용금액이 과도할 경우,귀하의 개인신용평점이 하락할 수 있습니다
>개인신용평점 하락 시 금융거래와 관련된 불이익이 발생할 수 있습니다.
>일정 기간 원리금을 연체할 경우,모든 원리금을 변제할 의무가 발생할 수 있습니다.
-신용카드 발급이 부적정한 경우(연체금 보유, 개인신용평점 낮음 등)카드 발급이 제한될 수 있습니다 
-카드 이용대금과 이에 수반되는 모든 수수료를 지정된 대금 결제일에 상환합니다.
-금융소비자는 금융소비자보호법 제19조 제1항에 따라 해당 상품 또는 서비스에 대하여 설명을 받을 권리가 있습니다.
-자세한 내용 및 이용 조건은 카드 신청 전 현대카드 홈페이지 및 상품설명서, 약관 참고
-준법감시심의필 240801-030 호 (2024-08-01 ~ 2025-07-31)


    """

    summary = MessageSummary()
    summary.initmodel()
    print(summary.get_summary(text))
