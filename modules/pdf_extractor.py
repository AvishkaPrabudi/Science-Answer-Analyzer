import PyPDF2
import pdfplumber
import os

class PDFTextExtractor:
    """
    Extract text from science textbook PDFs
    """
    
    def extract_with_pypdf2(self, pdf_path):
        """
        Method 1: Using PyPDF2
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                print(f"Extracting {total_pages} pages from {os.path.basename(pdf_path)}...")
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                    
                    # Progress indicator
                    if (page_num + 1) % 10 == 0:
                        print(f"Processed {page_num + 1}/{total_pages} pages...")
            
            return text
        
        except Exception as e:
            print(f"Error with PyPDF2: {e}")
            return None
    
    def extract_with_pdfplumber(self, pdf_path):
        """
        Method 2: Using pdfplumber (often better for complex PDFs)
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                
                print(f"Extracting {total_pages} pages from {os.path.basename(pdf_path)}...")
                
                for page_num, page in enumerate(pdf.pages):
                    text += page.extract_text() + "\n"
                    
                    # Progress indicator
                    if (page_num + 1) % 10 == 0:
                        print(f"Processed {page_num + 1}/{total_pages} pages...")
            
            return text
        
        except Exception as e:
            print(f"Error with pdfplumber: {e}")
            return None
    
    def extract_text(self, pdf_path):
        """
        Try both methods, use whichever works better
        """
        print("\n" + "="*60)
        print(f"Extracting text from: {os.path.basename(pdf_path)}")
        print("="*60)
        
        # Try pdfplumber first (usually better)
        text = self.extract_with_pdfplumber(pdf_path)
        
        # If failed, try PyPDF2
        if not text or len(text) < 100:
            print("Trying alternate method...")
            text = self.extract_with_pypdf2(pdf_path)
        
        if text:
            print(f"\n✓ Successfully extracted {len(text)} characters")
            return text
        else:
            print("\n✗ Failed to extract text")
            return ""
    
    def extract_multiple_pdfs(self, pdf_folder):
        """
        Extract text from all PDFs in a folder
        """
        all_text = ""
        pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
        
        print(f"\nFound {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_folder, pdf_file)
            text = self.extract_text(pdf_path)
            all_text += text + "\n\n"
        
        return all_text
    
    def save_extracted_text(self, text, output_file):
        """
        Save extracted text to a file
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\n✓ Saved extracted text to: {output_file}")


# TEST THE EXTRACTOR
if __name__ == "__main__":
    extractor = PDFTextExtractor()
    
    # Test with a single PDF
    pdf_path = "path/to/your/textbook.pdf"  # CHANGE THIS
    
    if os.path.exists(pdf_path):
        text = extractor.extract_text(pdf_path)
        
        # Show first 500 characters
        print("\n" + "="*60)
        print("SAMPLE TEXT (first 500 characters):")
        print("="*60)
        print(text[:500])
        
        # Save to file
        extractor.save_extracted_text(text, "extracted_textbook.txt")
    else:
        print(f"PDF not found: {pdf_path}")
        print("\nPlease update the pdf_path variable with your textbook location")