import os
import csv
import json
import re

# 경로 설정
text_base_dir = r"C:\...\VL"
voice_base_dir = r"C:\...\VS"
output_csv = r"C:\...\metadata.csv"

# 정규식을 사용해 숫자/텍스트 조합을 텍스트만 남기도록 변환하는 함수
def convert_text(text):
    # 한글을 제외한 모든 문자 제거
    text = re.sub(r'[^가-힣\s]', '', text)
    # 두 번 이상 연속된 공백을 하나의 공백으로 줄임
    text = re.sub(r'\s+', ' ', text)
    # 양쪽 끝의 공백 제거
    return text.strip()

# 모든 폴더를 재귀적으로 탐색하여 json 파일을 찾는 함수
def find_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(root, file)
                json_files.append(json_path)
    return json_files

# 메타데이터 파일 생성
with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter='|')
    
    json_files = find_json_files(text_base_dir)
    
    for json_path in json_files:
        # text 경로를 voice 경로로 변환
        relative_path = os.path.relpath(json_path, text_base_dir)
        wav_path = os.path.join(voice_base_dir, relative_path.replace('text', 'voice').replace('.json', '.wav'))
        
        if os.path.exists(wav_path):
            with open(json_path, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
                text = data["script"]["text"]
                
                # 텍스트 변환
                converted_text = convert_text(text)
                
                # wav 파일 이름 추출 및 '_22050' 추가
                wav_id = os.path.splitext(os.path.basename(wav_path))[0] + '_22050'
                
                # 메타데이터 파일에 기록 (3열에 2열과 동일한 값 추가)
                writer.writerow([wav_id, converted_text, converted_text])

print("metadata.csv 파일 생성 완료!")