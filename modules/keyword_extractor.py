from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class KeywordExtractor:
    """
    Extracts important keywords using TF-IDF
    """
    
    def __init__(self, max_keywords=10):
        self.max_keywords = max_keywords
        self.vectorizer = TfidfVectorizer(max_features=max_keywords)
    
    def extract_keywords(self, text, top_n=None):
        """
        Extract keywords from text
        Input: Preprocessed text (string)
        Output: List of (keyword, score) tuples
        """
        if top_n is None:
            top_n = self.max_keywords
        
        try:
            # Create TF-IDF matrix
            tfidf_matrix = self.vectorizer.fit_transform([text])
            
            # Get feature names (words)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get TF-IDF scores
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Create keyword-score pairs
            keyword_scores = list(zip(feature_names, tfidf_scores))
            
            # Sort by score (highest first)
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Return top N keywords
            return keyword_scores[:top_n]
        
        except:
            # If text is too short or has issues
            return []
    
    def extract_keywords_from_multiple(self, texts, top_n=None):
        """
        Extract keywords from multiple texts
        Useful for comparing student answers with model answer
        """
        if top_n is None:
            top_n = self.max_keywords
        
        # Fit on all texts
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        feature_names = self.vectorizer.get_feature_names_out()
        
        results = []
        for i, text in enumerate(texts):
            tfidf_scores = tfidf_matrix.toarray()[i]
            keyword_scores = list(zip(feature_names, tfidf_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            results.append(keyword_scores[:top_n])
        
        return results


# TEST THE KEYWORD EXTRACTOR
if __name__ == "__main__":
    from preprocessor import TextPreprocessor
    
    # Initialize
    preprocessor = TextPreprocessor()
    extractor = KeywordExtractor(max_keywords=10)
    
    # Model answer
    model_answer = """
    Photosynthesis is the biochemical process by which plants, algae, and some bacteria 
    convert light energy from the sun into chemical energy stored in glucose. 
    This process occurs in chloroplasts using chlorophyll pigment. 
    The equation is: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2
    """
    
    # Student answer
    student_answer = """
    Photosynthesis is when plants make food using sunlight. 
    It happens in chloroplasts with chlorophyll. 
    Plants take carbon dioxide and water and make glucose and oxygen.
    """
    
    # Preprocess both
    model_cleaned = preprocessor.preprocess_to_text(model_answer)
    student_cleaned = preprocessor.preprocess_to_text(student_answer)
    
    print("MODEL ANSWER KEYWORDS:")
    print("="*50)
    model_keywords = extractor.extract_keywords(model_cleaned, top_n=8)
    for keyword, score in model_keywords:
        print(f"{keyword}: {score:.3f}")
    
    print("\n\nSTUDENT ANSWER KEYWORDS:")
    print("="*50)
    student_keywords = extractor.extract_keywords(student_cleaned, top_n=8)
    for keyword, score in student_keywords:
        print(f"{keyword}: {score:.3f}")