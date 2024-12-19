from underthesea import text_normalize, word_tokenize
import re

def remove_duplicate_vowels(sentence):
    vowels = "aáàảãạăắằẳẵặâấầẩẫậeéèẻẽẹêếềểễệiíìỉĩịoóòỏõọôốồổỗộơớờởỡợuúùủũụ"
    result = ""
    prev_char = None

    for char in sentence:
        if char in vowels:
            if prev_char is None or prev_char != char:
                result += char
        else:
            result += char
        prev_char = char 

    return result

def preprocess_text(text):
    text = text.lower()                                                                 # Convert to lowercase
    text = re.sub(r'<a\s+[^>]*>.*?</a>', '', text, flags=re.DOTALL | re.IGNORECASE)     # Remove hyperlinks
    text = re.sub(r'[^\w\s]', ' ', text)                                                # Remove punctuation
    text = re.sub(r'\d+', '', text)                                                     # Remove digits
    text = text_normalize(text)                                                         # Correct word syntax: baỏ -> bảo
    text = re.sub(r'\b\S\b', '', text, flags=re.UNICODE)                                # Keep only words with length greater than 1
    text = ' '.join(word.replace(' ', '_') for word in word_tokenize(text))             # Word segmentation
    text = remove_duplicate_vowels(text)                                                # Removes duplicate vowels: Ngoooooon -> Ngon
    return text
