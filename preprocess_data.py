import pandas as pd
import csv
from modules.preprocess import preprocess_text

df = pd.read_csv('./dataset/crawl_data.csv', encoding='utf-8')

if 'text' in df.columns and 'label' in df.columns:
    df['processed_text'] = df['text'].fillna('')
    with open('./dataset/processed_data.csv', 'a', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        for index, row in df.iterrows():
            if len(row['processed_text']) > 10:
                text = row['processed_text']   
                text = preprocess_text(text)                                                                                                   
                writer.writerow([text,row['label']])
else:
    raise ValueError("Cột 'text' hoặc 'label' không tồn tại trong dataset. Vui lòng kiểm tra lại.")
