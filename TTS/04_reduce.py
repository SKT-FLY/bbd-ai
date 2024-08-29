import pandas as pd

# CSV 파일 로드
df = pd.read_csv('metadata.csv', sep='|', header=None, names=['id', 'text1', 'text2'])

# 텍스트 길이가 15자를 초과하지 않는 데이터만 필터링
filtered_df = df[df['text1'].apply(len) <= 20]

# 필터링된 데이터를 새로운 CSV 파일로 저장
filtered_df.to_csv('filtered_metadata_20.csv', sep='|', index=False, header=False)

print("필터링이 완료되었습니다. 필터링된 데이터는 'filtered_metadata_20.csv' 파일에 저장되었습니다.")