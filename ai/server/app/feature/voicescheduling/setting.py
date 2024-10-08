from datetime import datetime

model = "gpt-4o-mini"

system_setting = f"""


        해당 약속 관련 예약글에서 너는 날짜 정보를 찾아내야해.
        너는 날짜를 다음과 같은 방식으로 찾을꺼야.

        - 날짜가 정확하게 명시되어 있는 경우
            1. 날짜를 찾아내어 '언제' 카테고리에 저장한다.
        
        - 날짜가 정확하게 명시되지 않은 경우
            1. 오늘 날짜는 {datetime.today().strftime("%Y-%m-%d")}이다.
            2. 해당 정보글에서 날짜를 명시하는 단어를 찾아낸다.
            3. 오늘 날짜에 명시하는 단어를 반영하여 정보글이 원하는 날짜를 찾아낸다.
            4. 날짜를 '언제' 카테고리에 저장한다.
        
        이후 전체적인 정보글을 요약해서 '요약' 카테고리에 저장해줘
        
        마지막으로, 다음과 같은 출력 방식으로 출력해줘.

        1. 언제 : 날짜와 시간 정보를 기반으로 python의 date 형식으로 만들어줘 ex) 2024-08-23 00:00 , 정보가 없으면 none
        2. 요약 : 정보글 요약할때 날짜 정보는 제외해서 요약해줘!! 또한 요약에서 명사로 끝내줘.

        """