import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
from soynlp.normalizer import *

class PreprocessingMessage:
    def __init__(self):
        self.stop_words = set([
            '은', '는', '이', '가', '하', '아', '들', '의', '있', '수', '보', '주', '등', '한', '안', '때', '지', '두', 
            '이모티콘', '페이스톡 해요', '(광고)', '을', '로',
            'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 
            'ㅛ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ', 'ㅗ', 'ㅓ', 'ㅏ', 'ㅣ', 'ㅠ', 'ㅜ', 'ㅡ',
            'ㅃ', 'ㅉ', 'ㄸ', 'ㄲ', 'ㅆ', 'ㅒ', 'ㅖ', 'ㅚ', 'ㅟ', 'ㅢ', 'ㅘ', 'ㅙ', 'ㅞ', 'ㅝ',
            'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ', 'ㅋㅋ', 'ㅇㅇ'
        ])
        self.okt = Okt()
        self.tokenizer = Tokenizer()
        self.MAX_SEQUENCE_LENGTH = 100
        
    def preprocessing(self, text, remove_stopwords=True):
        # 한글 및 공백을 제외한 문자 모두 제거
        text = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]", "", text)

        # 반복되는 글자 정규화
        text = repeat_normalize(text, num_repeats=2)

        # 형태소 분석을 통해 단어 리스트 생성
        words = self.okt.morphs(text, stem=True)

        # 불용어 제거
        if remove_stopwords:
            words = [word for word in words if word not in self.stop_words]

        return words
    
    def get_clean_text(self, text):
        if isinstance(text, str):
            return self.preprocessing(text)
        else:
            return []
         
    def make_test_input(self, text):
        # 텍스트 전처리
        clean_text = self.get_clean_text(text)
        
        # 텍스트를 토크나이저에 맞게 시퀀스로 변환
        self.tokenizer.fit_on_texts(clean_text)
        sequences = self.tokenizer.texts_to_sequences([clean_text])
        
        # 시퀀스를 MAX_SEQUENCE_LENGTH 길이로 패딩
        test_input = pad_sequences(sequences, maxlen=self.MAX_SEQUENCE_LENGTH, padding='post')
        
        return test_input

# 테스트 코드
if __name__ == "__main__":
    test_text = '복권 1등 당첨을 원하세요? 지금당장 저희 링크로 접속하세요'
    preprocessor = PreprocessingMessage()
   
    clean_text = preprocessor.get_clean_text(test_text)
    print("전처리된 텍스트:", clean_text)
    
    test_input = preprocessor.make_test_input(test_text)
    print("모델 입력 데이터:", test_input)
