from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class AnswerComparator:
    """
    Compares student answer with model answer
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def calculate_similarity(self, model_answer, student_answer):
        """
        Calculate similarity between two answers
        Returns: similarity score (0 to 1)
        """
        try:
            # Create TF-IDF vectors for both answers
            tfidf_matrix = self.vectorizer.fit_transform([model_answer, student_answer])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return similarity
        
        except:
            return 0.0
    
    def find_matched_keywords(self, model_keywords, student_keywords):
        """
        Find which keywords from model answer are present in student answer
        Input: Two lists of (keyword, score) tuples
        Output: matched keywords, missing keywords
        """
        model_words = set([kw[0] for kw in model_keywords])
        student_words = set([kw[0] for kw in student_keywords])
        
        matched = model_words.intersection(student_words)
        missing = model_words - student_words
        
        return list(matched), list(missing)


# TEST THE COMPARATOR
if __name__ == "__main__":
    from preprocessor import TextPreprocessor
    from keyword_extractor import KeywordExtractor
    
    # Initialize
    preprocessor = TextPreprocessor()
    extractor = KeywordExtractor(max_keywords=10)
    comparator = AnswerComparator()
    
    # Answers
    model_answer = """
    Photosynthesis is the process by which plants convert light energy into 
    chemical energy using chlorophyll in chloroplasts.
    """
    
    student_answer = """
    Photosynthesis is when plants use sunlight and chlorophyll to make energy.
    """
    
    # Preprocess
    model_cleaned = preprocessor.preprocess_to_text(model_answer)
    student_cleaned = preprocessor.preprocess_to_text(student_answer)
    
    # Extract keywords
    model_kw = extractor.extract_keywords(model_cleaned, top_n=6)
    student_kw = extractor.extract_keywords(student_cleaned, top_n=6)
    
    # Calculate similarity
    similarity = comparator.calculate_similarity(model_cleaned, student_cleaned)
    
    # Find matched/missing keywords
    matched, missing = comparator.find_matched_keywords(model_kw, student_kw)
    
    print("SIMILARITY SCORE:", f"{similarity:.2%}")
    print("\nMATCHED KEYWORDS:", matched)
    print("MISSING KEYWORDS:", missing)