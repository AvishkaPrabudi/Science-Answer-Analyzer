import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

class TextPreprocessor:
    """
    This class cleans and prepares text for analysis
    """
    
    def __init__(self):
        # Initialize tools
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Keep important science words that are usually stopwords
        science_important = {'not', 'no', 'without', 'because', 'during', 'before', 'after'}
        self.stop_words = self.stop_words - science_important
    
    def preprocess(self, text):
        """
        Main preprocessing function
        Input: Raw text (string)
        Output: Cleaned list of words
        """
        # Step 1: Convert to lowercase
        text = text.lower()
        
        # Step 2: Tokenize (split into words)
        tokens = word_tokenize(text)
        
        # Step 3: Remove punctuation and non-alphabetic tokens
        tokens = [word for word in tokens if word.isalpha()]
        
        # Step 4: Remove stopwords
        tokens = [word for word in tokens if word not in self.stop_words]
        
        # Step 5: Lemmatize (convert to base form)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        
        return tokens
    
    def preprocess_to_text(self, text):
        """
        Returns cleaned text as a single string (for TF-IDF)
        """
        tokens = self.preprocess(text)
        return ' '.join(tokens)


# TEST THE PREPROCESSOR
if __name__ == "__main__":
    # Create preprocessor object
    preprocessor = TextPreprocessor()
    
    # Test with a sample science answer
    sample_answer = """
    Photosynthesis is the process by which plants convert light energy 
    into chemical energy. This process occurs in the chloroplasts using chlorophyll.
    """
    
    print("Original Text:")
    print(sample_answer)
    print("\n" + "="*50 + "\n")
    
    print("Cleaned Tokens:")
    cleaned_tokens = preprocessor.preprocess(sample_answer)
    print(cleaned_tokens)
    print("\n" + "="*50 + "\n")
    
    print("Cleaned Text:")
    cleaned_text = preprocessor.preprocess_to_text(sample_answer)
    print(cleaned_text)