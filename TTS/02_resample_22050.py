#22050Hz로 리샘플하는 코드

import librosa
import soundfile as sf
from glob import glob
import os

def resample_wav_file(input_file, output_dir, target_sampling_rate=22050):
    try:
        audio, sampling_rate = librosa.load(input_file, sr=None)
        audio_resampled = librosa.resample(audio, orig_sr=sampling_rate, target_sr=target_sampling_rate)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, os.path.basename(os.path.splitext(input_file)[0]) + "_{target_sampling_rate}.wav")
        sf.write(output_file, audio_resampled, target_sampling_rate)
        print(f"Resampled {input_file} to {output_file} at {target_sampling_rate}Hz")
    
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

# 이곳을 수정하고 실행할 것
dataset_path = <wav 파일이 저장된 경로>
output_dir = <22,050Hz 파일을 저장할 경로>

for wav_file in glob(dataset_path + "*.wav"):
    resample_wav_file(wav_file, output_dir)