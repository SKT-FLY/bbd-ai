import json

# 여러 개의 JSONL 파일 경로를 리스트에 저장
file_paths = [r'C:\Users\SKT005\bbd-ai\feature\AI-00\dataset\dataset_ccd\ccd-validate-int.jsonl',
              r'C:\Users\SKT005\bbd-ai\feature\AI-00\dataset\dataset_jld\jld-validate-int.jsonl',
              r'C:\Users\SKT005\bbd-ai\feature\AI-00\dataset\dataset_jjd\jjd-validate-int.jsonl',
              r'C:\Users\SKT005\bbd-ai\feature\AI-00\dataset\dataset_ksd\ksd-validate-int.jsonl',
              r'C:\Users\SKT005\bbd-ai\feature\AI-00\dataset\dataset_kwd\kwd-validate-int.jsonl'
              ]

# 병합된 데이터를 저장할 리스트 초기화
merged_data = []

for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            merged_data.append(json.loads(line))


# 병합된 데이터를 하나의 JSONL 파일로 저장
with open(r'C:\Users\SKT005\bbd-ai\feature\AI-00\dataset\merged_validateset.jsonl', 'w', encoding='utf-8') as output_file:
    for entry in merged_data:
        output_file.write(json.dumps(entry, ensure_ascii=False) + '\n')

