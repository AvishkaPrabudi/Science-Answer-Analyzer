from keyword_extractor import KeywordExtractor
from science_vocabulary import ScienceVocabularyBuilder

class EnhancedKeywordExtractor(KeywordExtractor):
    """
    Enhanced version that uses textbook-trained vocabulary
    """
    
    def __init__(self, max_keywords=10, vocabulary_file="science_vocabulary.json"):
        super().__init__(max_keywords)
        self.vocab_builder = ScienceVocabularyBuilder()
        
        # Try to load existing vocabulary
        if not self.vocab_builder.load_vocabulary(vocabulary_file):
            print("No vocabulary found. Will use standard extraction.")
    
    def extract_keywords_with_boost(self, text, subject="general", top_n=None):
        """
        Extract keywords with boost for known science terms
        """
        # Get standard keywords
        keywords = self.extract_keywords(text, top_n)
        
        # Boost scores for known science terms
        boosted_keywords = []
        for word, score in keywords:
            if self.vocab_builder.check_if_science_term(word, subject):
                # Boost score by 50% for known science terms
                boosted_score = score * 1.5
                boosted_keywords.append((word, boosted_score))
            else:
                boosted_keywords.append((word, score))
        
        # Re-sort by boosted scores
        boosted_keywords.sort(key=lambda x: x[1], reverse=True)
        
        return boosted_keywords[:top_n if top_n else self.max_keywords]


# TEST
if __name__ == "__main__":
    from preprocessor import TextPreprocessor
    
    preprocessor = TextPreprocessor()
    extractor = EnhancedKeywordExtractor()
    
    # Test answer
    answer = """
    Photosynthesis is the process where plants convert light energy into 
    chemical energy. Chlorophyll in chloroplasts absorbs sunlight.
    """
    
    cleaned = preprocessor.preprocess_to_text(answer)
    
    print("STANDARD KEYWORDS:")
    standard = extractor.extract_keywords(cleaned)
    for word, score in standard:
        print(f"{word}: {score:.3f}")
    
    print("\n\nBOOSTED KEYWORDS (if vocabulary loaded):")
    boosted = extractor.extract_keywords_with_boost(cleaned, subject="biology_grade10")
    for word, score in boosted:
        print(f"{word}: {score:.3f}")




