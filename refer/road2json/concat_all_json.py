import os
import json

# JSON 파일들이 있는 디렉토리 경로
json_folder = 'J:\json_save_path/'

# JSON 파일 목록을 불러옴
json_files = [file for file in os.listdir(json_folder) if file.endswith('.json')]

# 번호 순서대로 파일 읽어서 합치기
combined_data = []
for json_file in sorted(json_files):
    with open(os.path.join(json_folder, json_file), 'r') as f:
        json_data = json.load(f)
        combined_data.append(json_data)

# 결과를 하나의 JSON 파일로 저장
output_file = 'combined.json'
with open(output_file, 'w') as f:
    json.dump(combined_data, f,indent='\t')

print(f'JSON 파일들이 번호 순서대로 합쳐져 {output_file} 파일로 저장되었습니다.')
