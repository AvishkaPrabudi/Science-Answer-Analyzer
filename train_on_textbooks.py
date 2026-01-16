import os
from modules.pdf_extractor import PDFTextExtractor
from modules.science_vocabulary import ScienceVocabularyBuilder

extractor = PDFTextExtractor()
vocab_builder = ScienceVocabularyBuilder()

textbook_folder = "textbooks"
pdf_files = [f for f in os.listdir(textbook_folder) if f.endswith('.pdf')]

print("="*70)
print("TRAINING ON SCIENCE TEXTBOOKS")
print("="*70)
print(f"\nFound {len(pdf_files)} PDFs:")
for pdf in pdf_files:
    print(f"  - {pdf}")

os.makedirs("trained_data", exist_ok=True)

print("\nStarting extraction... This will take 10-15 minutes.\n")

for pdf_file in pdf_files:
    pdf_path = os.path.join(textbook_folder, pdf_file)
    subject_name = pdf_file.replace('.pdf', '').replace(' ', '_').lower()
    
    print(f"\n{'='*70}")
    print(f"Processing: {pdf_file}")
    print('='*70)
    
    text = extractor.extract_text(pdf_path)
    
    if len(text) > 100:
        # Save extracted text
        text_file = f"trained_data/{subject_name}_extracted.txt"
        extractor.save_extracted_text(text, text_file)
        
        # Build vocabulary
        vocab_builder.build_vocabulary_from_text(text, subject=subject_name)
        print(f"Success! Extracted {len(text):,} characters")
        
        # Show top 15 terms
        top_terms = vocab_builder.get_top_terms(subject_name, top_n=15)
        print(f"\nTop 15 science terms:")
        for i, (term, freq) in enumerate(top_terms, 1):
            print(f"  {i:2d}. {term:20s} ({freq:4d} times)")
    else:
        print(f"Warning: Only {len(text)} characters extracted")

vocab_builder.save_vocabulary("trained_data/science_vocabulary.json")

print("\n" + "="*70)
print("✅ TRAINING COMPLETE!")
print("="*70)
print(f"Processed {len(pdf_files)} textbooks")
print("Vocabulary saved to: trained_data/science_vocabulary.json")
print("\nYou can now use this vocabulary for accurate keyword matching!")