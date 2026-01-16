from modules.preprocessor import TextPreprocessor
import json
from collections import Counter

class ScienceVocabularyBuilder:
    """
    Build a science-specific vocabulary from textbooks
    """
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.vocabulary = {}
    
    def build_vocabulary_from_text(self, text, subject="general"):
        """
        Extract all important science terms from textbook
        """
        print(f"\nBuilding vocabulary for: {subject}")
        
        # Preprocess text
        tokens = self.preprocessor.preprocess(text)
        
        # Count word frequencies
        word_freq = Counter(tokens)
        
        # Filter for science terms (words appearing multiple times)
        # Science terms usually appear more than once in textbooks
        science_terms = {
            word: freq 
            for word, freq in word_freq.items() 
            if freq >= 3 and len(word) > 3  # Appear 3+ times, longer than 3 chars
        }
        
        self.vocabulary[subject] = science_terms
        
        print(f"✓ Found {len(science_terms)} science terms")
        
        return science_terms
    
    def get_top_terms(self, subject, top_n=100):
        """
        Get most important terms from a subject
        """
        if subject not in self.vocabulary:
            return []
        
        terms = self.vocabulary[subject]
        sorted_terms = sorted(terms.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_terms[:top_n]
    
    def save_vocabulary(self, filename="science_vocabulary.json"):
        """
        Save vocabulary to JSON file
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.vocabulary, f, indent=2)
        
        print(f"\n✓ Vocabulary saved to: {filename}")
    
    def load_vocabulary(self, filename="science_vocabulary.json"):
        """
        Load previously saved vocabulary
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.vocabulary = json.load(f)
            print(f"✓ Vocabulary loaded from: {filename}")
            return True
        except:
            print(f"✗ Could not load vocabulary from: {filename}")
            return False
    
    def check_if_science_term(self, word, subject="general"):
        """
        Check if a word is a known science term
        """
        if subject in self.vocabulary:
            return word.lower() in self.vocabulary[subject]
        return False
    
    def get_term_importance(self, word, subject="general"):
        """
        Get importance score of a science term
        """
        if subject in self.vocabulary:
            return self.vocabulary[subject].get(word.lower(), 0)
        return 0


# TEST THE VOCABULARY BUILDER
if __name__ == "__main__":
    from pdf_extractor import PDFTextExtractor
    
    # Extract text from textbook
    extractor = PDFTextExtractor()
    
    # CHANGE THIS to your textbook path
    pdf_path = "path/to/biology_grade10.pdf"
    
    if os.path.exists(pdf_path):
        print("Extracting textbook content...")
        text = extractor.extract_text(pdf_path)
        
        # Build vocabulary
        vocab_builder = ScienceVocabularyBuilder()
        terms = vocab_builder.build_vocabulary_from_text(text, subject="biology_grade10")
        
        # Show top 20 terms
        print("\n" + "="*60)
        print("TOP 20 SCIENCE TERMS:")
        print("="*60)
        top_terms = vocab_builder.get_top_terms("biology_grade10", top_n=20)
        for term, freq in top_terms:
            print(f"{term}: {freq} occurrences")
        
        # Save vocabulary
        vocab_builder.save_vocabulary()
    else:
        print(f"Please place your textbook PDF and update the path")