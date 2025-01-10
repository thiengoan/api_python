from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
import csv
import re
from modules.preprocess import preprocess_text

# Load data
df = pd.read_csv('output.csv', encoding='utf-8')  # Replace with your dataset path

# Kiểm tra cột 'text' có tồn tại hay không
if 'text' in df.columns and 'label' in df.columns:
    # Tạo một cột mới 'processed_text' từ cột 'text' bằng cách áp dụng tiền xử lý
    df['processed_text'] = df['text'].fillna('') # Ví dụ tiền xử lý đơn giản
    # Ghi thêm dữ liệu vào file CSV
    with open('./dataset/data.csv', 'a', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        # Ghi từng dòng từ DataFrame vào file CSV, bao gồm chỉ mục tăng dần
        for index, row in df.iterrows():
            if len(row['processed_text']) > 10:
                text = row['processed_text'].lower()                                                                 # Convert to lowercase
                text = re.sub(r'<a\s+[^>]*>.*?</a>', '', text, flags=re.DOTALL | re.IGNORECASE)     # Remove hyperlinks
                text = re.sub(r'[^\w\s]', ' ', text)                                                # Remove punctuation
                text = re.sub(r'\d+', '', text)                                                     # Remove digits                                                        # Correct word syntax: baỏ -> bảo
                writer.writerow([index + 321609,text,row['label']])
else:
    raise ValueError("Cột 'text' hoặc 'label' không tồn tại trong dataset. Vui lòng kiểm tra lại.")
