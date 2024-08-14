"""
OPTIONAL : 데이터셋이 너무 길면 줄일 수 있습니다.

18만 line에 달하는 jsonl 파일의 앞 줄만을 가져오기 위한 코드입니다.
작성자 : @송주영

코드 돌리기 전 바꾸어야 할 사항 : input_file, output_file 경로
"""

input_file = r'C:\Users\SKT005\bbd-ai\feature\AI-00\dataset\dataset_jld\jld-validate.jsonl'
output_file = r'C:\Users\SKT005\bbd-ai\feature\AI-00\dataset\dataset_jld\jld-validate_1.jsonl'

with open(input_file, 'r', encoding='utf-8') as infile:
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i in range(5604):
            line = infile.readline()
            if not line:
                break
            outfile.write(line)
