import torch
import os
from TTS.api import TTS

import time

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
print("device =", device)

# Initialize TTS model
tts = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24", progress_bar=False).to(device)

# Define source and target directories
source_dir = r"C:\Users\SKT005\bbd-ai\feature\AI-09\voice_to_be_converted"
target_dir = r"C:\Users\SKT005\bbd-ai\feature\AI-09\target_voice"
output_dir = r"C:\Users\SKT005\bbd-ai\feature\AI-09\output_voice"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Iterate over all files in the source directory
for filename in os.listdir(source_dir):
    for targetname in os.listdir(target_dir):
        if filename.endswith(".wav") and targetname.endswith(".wav"):

            start = time.time()
            source_wav = os.path.join(source_dir, filename)
            target_wav = os.path.join(target_dir, targetname)
            output_path = os.path.join(output_dir, f"converted_{filename[:-4]}_from_{targetname}")
            
            # Perform voice conversion
            tts.voice_conversion_to_file(
                source_wav=source_wav,
                target_wav=target_wav,
                file_path=output_path
            )

            end = time.time()

            print(end - start, "seconds")
            print(f"Converted {filename} to {output_path}")

print("Voice conversion completed for all files.")