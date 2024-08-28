"""
fine-tuning을 위한 코드입니다.
#make_dataset.py 가 더 적당한 이름일 수 있음
작성자 : @송주영

!!! 주의 : 데이터셋은 따로 다운로드 받아서 코드 실행해야 함
코드 돌리기 전 바꾸어야 할 사항 : 데이터셋 경로, 완성된 jsonl 파일이 저장될 경로
"""

import os
import json
from tqdm import tqdm

def process_json_file(file_path):
    """JSON 파일을 읽고 필요한 데이터를 추출하여 포맷을 맞춘 후 반환합니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pronunciation = data.get('transcription', {}).get('pronunciation', '')
    standard = data.get('transcription', {}).get('standard', '')
    
    formatted_data = {
        "messages": [
            {"role": "system", "content": "다음은 한국어를 소리 나는 대로 적은 것입니다. 만약 이것이 방언이라면 표준어로 바꾸세요."},
            {"role": "user", "content": pronunciation},
            {"role": "assistant", "content": standard}
        ]
    }
    
    return formatted_data

def process_folder(folder_path):
    """단일 폴더 내의 모든 JSON 파일을 처리하고 결과를 리스트로 반환합니다."""
    files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    results = []
    
    for file_name in tqdm(files, desc=f"Processing folder {os.path.basename(folder_path)}"):
        file_path = os.path.join(folder_path, file_name)
        
        try:
            result = process_json_file(file_path)
            results.append(result)  
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
    
    return results

def main(folders, output_file):
    """여러 폴더를 순회하여 JSON 파일을 처리하고 결과를 JSONL 파일에 저장합니다."""
    all_results = []
    for folder_path in folders:
        print(f"Processing folder: {folder_path}")
        folder_results = process_folder(folder_path)
        all_results.extend(folder_results)
    
    # 모든 결과를 한 번에 JSONL 파일에 저장
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for item in tqdm(all_results, desc="Writing results to file"):
            out_file.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    folders = [
        r"feature\AI-00\dialect\dialect_jjd\VL_03_A",
        r"feature\AI-00\dialect\dialect_jjd\VL_03_F",
    ]  # JSON 파일이 위치한 폴더 경로들
    output_file = r"C:\Users\SKT005\bbd-ai\feature\AI-00\dataset\dataset_jjd\jjd-validate.jsonl"
    
    # 결과를 저장할 JSONL 파일
    main(folders, output_file)