
from pydub import AudioSegment

def repeat_wav(input_file, output_file, n):
    # WAV 파일 열기
    sound = AudioSegment.from_wav(input_file)
    
    # n번 반복
    repeated_sound = sound * n
    
    # 결과를 새로운 파일로 저장
    repeated_sound.export(output_file, format="wav")

# 예시 사용법
input_wav = r"C:\Users\SKT005\bbd-ai\feature\AI-09\target_voice\UDHR-slow-shu.wav"
output_wav = r"C:\Users\SKT005\bbd-ai\feature\AI-09\target_voice\repeated_UDHR-slow-shu.wav"
n = 10  # 반복 횟수

repeat_wav(input_wav, output_wav, n)
