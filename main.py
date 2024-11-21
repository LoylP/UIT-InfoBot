import underthesea
from spellchecker import SpellChecker
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Tải mô hình T5
tokenizer_t5 = T5Tokenizer.from_pretrained('t5-base')
model_t5 = T5ForConditionalGeneration.from_pretrained('t5-base')

# Hàm sửa lỗi chính tả bằng thư viện SpellChecker
def correct_spelling(text):
    spell = SpellChecker(language='vi')
    words = text.split()
    corrected_text = ' '.join([spell.correction(word) if spell.unknown([word]) else word for word in words])
    return corrected_text

# Hàm mở rộng ngữ nghĩa với mô hình T5
def expand_meaning(text):
    input_text = f"expand: {text}"  # Thêm prompt yêu cầu mở rộng ngữ nghĩa
    inputs = tokenizer_t5(input_text, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model_t5.generate(inputs['input_ids'], max_length=512, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
    expanded_text = tokenizer_t5.decode(outputs[0], skip_special_tokens=True)
    return expanded_text

# Hàm sử dụng Underthesea để phân tích câu văn
def process_with_underthesea(text):
    # Tách từ và gán nhãn
    words = underthesea.word_tokenize(text)
    print(f"Tách từ: {words}")
    
    # Nhận diện thực thể (nếu có)
    named_entities = underthesea.ner(text)
    print(f"Nhận diện thực thể: {named_entities}")
    
    return words

# Hàm chính xử lý văn bản
def process_text(text):
    # Sửa lỗi chính tả
    corrected_text = correct_spelling(text)
    print(f"Đã sửa lỗi chính tả: {corrected_text}")
    
    # Mở rộng ngữ nghĩa
    expanded_text = expand_meaning(corrected_text)
    print(f"Đã mở rộng ngữ nghĩa: {expanded_text}")
    
    # Xử lý với Underthesea (tách từ và nhận diện thực thể)
    processed_text = process_with_underthesea(expanded_text)
    
    return processed_text

# Ví dụ
input_text = "Hôm nay tôi rất vui vẽ đi học và gặp các bạn"
processed_text = process_text(input_text)
