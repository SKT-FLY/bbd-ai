import numpy as np
import re
import tensorflow as tf
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.model_selection import KFold
from tensorflow.keras.models import load_model


from soynlp.normalizer import *

stop_words=set(['은','는','이','가','하','아','들','의','있','수','보','주','등','한','안','때','지','두', '이모티콘', '페이스톡 해요', '(광고)',
                'ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ','ㅛ','ㅕ','ㅑ','ㅐ','ㅔ','ㅗ','ㅓ','ㅏ','ㅣ','ㅠ','ㅜ','ㅡ',
                'ㅃ','ㅉ','ㄸ','ㄲ','ㅆ','ㅒ','ㅖ','ㅚ','ㅟ','ㅢ','ㅘ','ㅙ','ㅞ','ㅝ','ㄳ','ㄵ','ㄶ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅄ','ㅋㅋ','ㅇㅇ'])

MAX_SEQUENCE_LENGTH=100
okt=Okt()
tokenizer=Tokenizer()

test = '복권 1등 당첨을 원하세요? 지금당장 저희 링크로 접속하세요'


def preprocessing(text, okt, remove_stopwords = False, stop_words = []):
    # remove_stopword : 불용어를 제거할지 선택 기본값은 False
    # stop_word : 불용어 사전은 사용자가 직접 입력해야함 기본값은 비어있는 리스트

    # 한글 및 공백을 제외한 문자 모두 제거.
    text1 = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]", "", text)

    repeat_text = repeat_normalize(text1, num_repeats=2)

    # okt 객체를 활용해서 형태소 단위로 나눈다.
    word = okt.morphs(repeat_text, stem=True)

    # 불용어 제거(선택적)
    if remove_stopwords:
        word = [token for token in word if not token in stop_words]

    return word

def get_clean_text(text):
    # 비어있는 데이터에서 멈추지 않도록 문자열인 경우에만 진행
    clean_text=[]
    if type(text)==str:
      clean_text.append(preprocessing(text, okt, remove_stopwords=True, stop_words=stop_words))
    else:
        # string이 아니면 비어있는 값 추가
        clean_text.append([])
    return clean_text

clean_text = get_clean_text(test)

def make_test(text):
  test = preprocessing(text, okt, remove_stopwords=True, stop_words=stop_words)
  tokenizer=Tokenizer()
  tokenizer.fit_on_texts(clean_text)
  test_s = tokenizer.texts_to_sequences(test)
  test_s = [x[0] for x in test_s if x != []]
  test_input = pad_sequences([test_s], maxlen=MAX_SEQUENCE_LENGTH, padding='post')
  return test_input


def one_pred(text):
  test_input = make_test(text)
  model = load_model('/home/odaebum/Messenger-phishing-detection/android/model/phishing_model_'+str(i)+'.h5')
  prediction = model.predict(test_input)[0][1]
  print('피싱일 확률은','{:.2%}'.format(prediction),'입니다.')

def all_pred(text, k):
  test_input = make_test(text)
  preds = []
  for i in range(1,k+1):
    model = load_model('/home/odaebum/Messenger-phishing-detection/android/model/phishing_model_'+str(i)+'.h5')
    prediction = model.predict(test_input)[0][1]
    preds.append(prediction)
  pred_mean = np.mean(preds)
  print('피싱일 확률은','{:.2%}'.format(pred_mean),'입니다.')

all_pred(test,5)
