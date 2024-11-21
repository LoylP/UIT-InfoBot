import nltk
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from nltk.tokenize import sent_tokenize
from typing import List, Tuple
import re

class AdvancedQuestionGenerator:
    def __init__(self, model_name: str = "VietAI/vit5-base-vietnews-summarization"):
        # Download required NLTK resources
        self._download_nltk_resources()
        
        # Initialize T5 model and tokenizer
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name).to(self.device)
        
    def _download_nltk_resources(self):
        """Download NLTK resources if not already present"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    def preprocess_text(self, text: str) -> List[str]:
        """Preprocess and filter text to focus on UIT-related content"""
        # Normalize text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split into sentences
        sentences = sent_tokenize(text)
        
        # Define UIT-related keywords
        keywords = [
            'Trường Đại học Công nghệ Thông tin', 'ĐHQG-HCM', 'tân sinh viên',
            'nhập học', 'giấy báo', 'học phí', 'sinh viên', 'MSSV', 'KTX', 
            'Lễ Khai giảng', 'học kỳ'
        ]
        
        # Filter sentences with important keywords
        meaningful_sentences = [
            sent for sent in sentences 
            if any(keyword.lower() in sent.lower() for keyword in keywords)
        ]
        
        return meaningful_sentences

    def generate_question_from_sentence(self, sentence: str) -> str:
        """Generate a question from a given sentence focusing on UIT context"""
        # Add a prompt to guide T5
        input_text = f"generate question about UIT admission: {sentence}"
        
        # Tokenize and generate question
        inputs = self.tokenizer.encode(
            input_text, 
            max_length=512, 
            truncation=True, 
            return_tensors="pt"
        ).to(self.device)
        
        outputs = self.model.generate(
            inputs,
            max_length=64,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True
        )
        
        question = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return question

    def generate_questions(self, text: str, num_questions: int = 5) -> List[Tuple[str, str]]:
        """Generate multiple questions from UIT-related text"""
        # Preprocess text and get relevant sentences
        sentences = self.preprocess_text(text)
        
        # Prioritize sentences with UIT-specific keywords
        keywords = ['Trường Đại học Công nghệ Thông tin', 'ĐHQG-HCM', 'sinh viên', 'nhập học']
        important_sentences = [sent for sent in sentences if any(keyword in sent for keyword in keywords)]
        
        # Fallback to general sentences if not enough important ones
        selected_sentences = important_sentences[:num_questions] or sentences[:num_questions]

        # Generate questions
        qa_pairs = []
        for sentence in selected_sentences:
            try:
                question = self.generate_question_from_sentence(sentence)
                qa_pairs.append((question, sentence))
            except Exception as e:
                print(f"Error generating question for sentence: {e}")
                continue
                    
        return qa_pairs

    def generate_questions_by_type(self, text: str, num_questions: int = 5) -> dict:
        """Generate questions categorized by type"""
        qa_pairs = self.generate_questions(text, num_questions)
        
        # Categorize questions
        categorized_questions = {
            'what': [],
            'how': [],
            'when': [],
            'where': [],
            'other': []
        }
        
        for question, answer in qa_pairs:
            q_lower = question.lower()
            if any(q_lower.startswith(w) for w in ['what', 'điều gì', 'cái gì']):
                categorized_questions['what'].append((question, answer))
            elif any(q_lower.startswith(w) for w in ['how', 'làm sao', 'như thế nào']):
                categorized_questions['how'].append((question, answer))
            elif any(q_lower.startswith(w) for w in ['when', 'khi nào']):
                categorized_questions['when'].append((question, answer))
            elif any(q_lower.startswith(w) for w in ['where', 'ở đâu']):
                categorized_questions['where'].append((question, answer))
            else:
                categorized_questions['other'].append((question, answer))
                
        return categorized_questions

def main():
    # Initialize generator
    generator = AdvancedQuestionGenerator()
    
    # Read text from file
    file_path = '/home/loylp/project/UIT-InfoBot/Document/content.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Generate questions
    print("Generating regular questions:")
    questions = generator.generate_questions(text, num_questions=5)
    for i, (question, answer) in enumerate(questions, 1):
        print(f"\nQ{i}: {question}")
        print(f"A{i}: {answer}")
    
    print("\nGenerating categorized questions:")
    categorized_questions = generator.generate_questions_by_type(text, num_questions=8)
    for category, qa_pairs in categorized_questions.items():
        if qa_pairs:
            print(f"\n{category.upper()} questions:")
            for i, (question, answer) in enumerate(qa_pairs, 1):
                print(f"\nQ{i}: {question}")
                print(f"A{i}: {answer}")

if __name__ == "__main__":
    main()