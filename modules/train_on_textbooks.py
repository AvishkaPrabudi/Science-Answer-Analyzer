import os
from modules.pdf_extractor import PDFTextExtractor
from modules.science_vocabulary import ScienceVocabularyBuilder

def train_on_textbooks():
    """Extract text from all textbooks and build vocabulary"""
    extractor = PDFTextExtractor()
    vocab_builder = ScienceVocabularyBuilder()
    
    # Define textbook mapping - UPDATED FOR YOUR FILES
    textbooks = {
        "grade10_science_part1": "textbooks/Grade-10-Science-Part-I.pdf",
        "grade10_science_part2": "textbooks/Grade-10-Science-Part-II.pdf",
        "grade11_science_part1": "textbooks/Grade 11 Science Part I.pdf",
        "grade11_science_part2": "textbooks/Grade 11 Science Part II.pdf",
    }
    
    print("="*70)
    print("TRAINING ON SCIENCE TEXTBOOKS")
    print("="*70)
    
    # Create directories
    os.makedirs("trained_data", exist_ok=True)
    os.makedirs("textbooks", exist_ok=True)
    
    found_pdfs = []
    missing_pdfs = []
    
    # Check which PDFs exist
    for subject, pdf_path in textbooks.items():
        if os.path.exists(pdf_path):
            found_pdfs.append((subject, pdf_path))
            print(f"✓ Found: {pdf_path}")
        else:
            missing_pdfs.append(pdf_path)
            print(f"✗ Missing: {pdf_path}")
    
    if not found_pdfs:
        print("\n❌ No textbook PDFs found!")
        print("\nExpected files in 'textbooks/' folder:")
        for pdf in textbooks.values():
            print(f"  - {pdf}")
        return
    
    print(f"\n✓ Found {len(found_pdfs)} textbook(s)")
    print("Starting extraction... This may take several minutes.\n")
    
    # Process each textbook
    for subject, pdf_path in found_pdfs:
        print(f"\n{'='*70}")
        print(f"Processing: {subject}")
        print('='*70)
        
        # Extract text
        text = extractor.extract_text(pdf_path)
        
        if len(text) < 100:
            print(f"⚠ Warning: Very little text extracted from {subject}")
            print(f"  Only {len(text)} characters found. PDF might be image-based.")
            continue
        
        # Save extracted text
        text_file = f"trained_data/{subject}_extracted.txt"
        extractor.save_extracted_text(text, text_file)
        
        # Build vocabulary
        vocab_builder.build_vocabulary_from_text(text, subject=subject)
        
        # Show top terms
        print(f"\nTop 15 terms in {subject}:")
        top_terms = vocab_builder.get_top_terms(subject, top_n=15)
        for i, (term, freq) in enumerate(top_terms, 1):
            print(f"  {i:2d}. {term:20s} ({freq:4d} times)")
    
    # Save complete vocabulary
    vocab_file = "trained_data/science_vocabulary.json"
    vocab_builder.save_vocabulary(vocab_file)
    
    print("\n\n" + "="*70)
    print("✅ TRAINING COMPLETE!")
    print("="*70)
    print(f"Vocabulary saved to: {vocab_file}")
    print(f"Processed {len(found_pdfs)} textbook(s)")
    print(f"\nExtracted text files saved in: trained_data/")
    
    if missing_pdfs:
        print(f"\n⚠ Note: {len(missing_pdfs)} textbook(s) not found")

if __name__ == "__main__":
    train_on_textbooks()