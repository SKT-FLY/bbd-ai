import os
import shutil

# 경로 설정
source_base_dir = r"C:\...\VS"
destination_dir = r"C:\...\all_wav_files"

# 대상 폴더가 없다면 생성
os.makedirs(destination_dir, exist_ok=True)

# 모든 폴더를 재귀적으로 탐색하여 wav 파일을 찾는 함수
def move_wav_files(source_dir, dest_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.wav'):
                # 원본 파일의 전체 경로
                source_path = os.path.join(root, file)
                # 대상 폴더의 경로로 파일을 이동
                dest_path = os.path.join(dest_dir, file)
                
                # 이름 충돌을 피하기 위해 같은 이름의 파일이 있을 경우 파일명을 수정
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(file)
                    count = 1
                    new_file_name = f"{base}_{count}{ext}"
                    new_dest_path = os.path.join(dest_dir, new_file_name)
                    while os.path.exists(new_dest_path):
                        count += 1
                        new_file_name = f"{base}_{count}{ext}"
                        new_dest_path = os.path.join(dest_dir, new_file_name)
                    dest_path = new_dest_path
                
                shutil.move(source_path, dest_path)  # 파일 이동
                # shutil.copy2(source_path, dest_path)  # 파일 복사 시 사용

# 실행
move_wav_files(source_base_dir, destination_dir)

print("모든 wav 파일이 이동되었습니다!")