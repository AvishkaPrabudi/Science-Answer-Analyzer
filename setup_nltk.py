import nltk

print("Downloading NLTK data...")
nltk.download('punkt')
nltk.download('punkt_tab')  # NEW - needed for newer NLTK
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
print("Done! NLTK is ready.")