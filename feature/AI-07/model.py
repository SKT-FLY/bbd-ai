import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
from tensorflow.keras.models import load_model
import preprocessing

class DetectPhishing:
    def __init__(self):
        # 모델 파일 경로 템플릿을 초기화
        self.model_path_template = '/home/odaebum/bbd-ai/feature/AI-07/phishing_model_{}.h5'

    def make_test_input(self, text):
        # 전처리 객체를 생성하고, 입력 텍스트를 전처리
        msg = preprocessing.PreprocessingMessage()
        return msg.make_test_input(text)

    def all_pred(self, text):
        test_input = self.make_test_input(text)
        preds = []

        # 5개의 모델에 대해 예측 수행
        for i in range(1, 6):
            model_path = self.model_path_template.format(i)
            model = load_model(model_path)
            prediction = model.predict(test_input)[0][1]
            preds.append(prediction)

        pred_mean = np.mean(preds)
        print('피싱일 확률은', '{:.2%}'.format(pred_mean), '입니다.')

        return pred_mean

if __name__ == "__main__":
    model = DetectPhishing()
    text = '복권 1등 당첨을 원하세요? 지금당장 저희 링크로 접속하세요'
    model.all_pred(text)
