# Science Answer Keyword Analysis System

An AI-powered automated evaluation system for Grade 10 and 11 science answers using Natural Language Processing (NLP) and keyword analysis. The system evaluates student responses by comparing them against model answers using TF-IDF keyword extraction and semantic similarity matching.

## 🎯 Features

- **Automated Answer Evaluation**: Compares student answers with model answers
- **Keyword Extraction**: Uses TF-IDF to identify important scientific terms
- **Textbook Training**: Trains on actual Grade 10 & 11 science textbooks to recognize domain-specific vocabulary
- **Similarity Scoring**: Employs cosine similarity for semantic matching
- **Detailed Feedback**: Provides specific feedback on matched and missing keywords
- **Subject-Specific**: Supports Biology, Chemistry, and Physics with separate vocabularies
- **Weighted Scoring**: Combines similarity (60%) and keyword matching (40%) for fair evaluation

## 🛠️ Technology Stack

- **Python 3.11+**
- **NLTK**: Text preprocessing and tokenization
- **scikit-learn**: TF-IDF vectorization and cosine similarity
- **pdfplumber**: PDF text extraction from textbooks
- **pandas**: Data handling
- **Flask**: Web interface (coming soon)

## 📁 Project Structure
```
science-answer-analyzer/
├── modules/
│   ├── __init__.py
│   ├── preprocessor.py           # Text cleaning and preprocessing
│   ├── keyword_extractor.py      # TF-IDF keyword extraction
│   ├── comparator.py             # Answer similarity comparison
│   ├── pdf_extractor.py          # PDF text extraction
│   └── science_vocabulary.py     # Vocabulary builder from textbooks
├── textbooks/                    # Place Grade 10-11 science PDFs here
├── trained_data/                 # Extracted vocabulary and text
│   └── science_vocabulary.json   # Trained vocabulary database
├── answer_evaluator.py           # Main evaluation engine
├── train_on_textbooks.py         # Training script for textbooks
├── setup_nltk.py                 # NLTK data download script
└── requirements.txt              # Python dependencies
```

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup Steps

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/science-answer-analyzer.git
   cd science-answer-analyzer
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Download NLTK data**
```bash
   python setup_nltk.py
```

4. **Add textbooks** (Optional but recommended)
   - Place your Grade 10-11 science textbook PDFs in the `textbooks/` folder
   - Supported formats: PDF

5. **Train on textbooks** (Optional but recommended)
```bash
   python train_on_textbooks.py
```
   This extracts scientific vocabulary from textbooks for more accurate evaluation.

## 📖 Usage

### Basic Evaluation
```python
from answer_evaluator import AnswerEvaluator

# Initialize evaluator
evaluator = AnswerEvaluator()

# Define model answer (teacher's correct answer)
model_answer = """
Photosynthesis is the process by which green plants convert light energy 
into chemical energy. It occurs in chloroplasts using chlorophyll pigment. 
The process uses carbon dioxide and water to produce glucose and oxygen.
"""

# Student's answer
student_answer = """
Photosynthesis is when plants make food using sunlight. It happens in 
chloroplasts with chlorophyll. Plants take CO2 and water to make glucose.
"""

# Evaluate
result = evaluator.evaluate_answer(
    model_answer=model_answer,
    student_answer=student_answer,
    subject="grade10_science",
    max_marks=10
)

# Print results
evaluator.print_result(result)
```

### Output Example
```
======================================================================
EVALUATION RESULT
======================================================================

📊 SCORE: 7.5/10 (75.0%)

📈 METRICS:
   • Overall Similarity: 78.5%
   • Keyword Match: 70.0%

💬 FEEDBACK:
✓ Good answer. Most key concepts present.

✓ Keywords found: photosynthesis, chloroplast, chlorophyll, glucose
✗ Missing keywords: carbon dioxide, oxygen
  → Focus on these concepts to improve your answer.

======================================================================
```

## 🔧 How It Works

### 1. **Text Preprocessing**
   - Converts text to lowercase
   - Tokenizes into words
   - Removes stopwords (keeping science-important terms)
   - Lemmatizes words to base forms

### 2. **Keyword Extraction**
   - Uses TF-IDF (Term Frequency-Inverse Document Frequency)
   - Identifies top N important keywords from model answer
   - Extracts keywords from student answer

### 3. **Similarity Calculation**
   - Computes cosine similarity between model and student answers
   - Matches keywords found in both answers
   - Identifies missing keywords

### 4. **Scoring Algorithm**
```
   Final Score = (Similarity × 0.6) + (Keyword Match × 0.4) × Max Marks
```

### 5. **Feedback Generation**
   - ≥80%: Excellent
   - 60-79%: Good
   - 40-59%: Average
   - <40%: Needs Improvement

## 📊 Evaluation Metrics

| Metric | Description | Weight |
|--------|-------------|--------|
| **Similarity Score** | Semantic similarity between answers | 60% |
| **Keyword Match** | Percentage of key terms present | 40% |

## 🎓 Training on Textbooks

The system can be trained on Grade 10-11 science textbooks to improve accuracy:

1. Add PDF textbooks to `textbooks/` folder
2. Run training script:
```bash
   python train_on_textbooks.py
```
3. System extracts scientific vocabulary and stores in `trained_data/science_vocabulary.json`

**Benefits:**
- Recognizes subject-specific terminology
- Understands domain vocabulary
- Improves keyword matching accuracy
- Adapts to curriculum-specific language

## 🧪 Testing

Run the test suite:
```bash
python answer_evaluator.py
```

This tests the system with multiple answer qualities (excellent, good, average, poor).

## 📝 Requirements
```
nltk==3.8.1
scikit-learn>=1.3.0
pandas>=2.0.0
flask>=2.3.0
pdfplumber>=0.9.0
PyPDF2>=3.0.0
```

## 🔮 Future Enhancements

- [ ] Web-based interface for teachers
- [ ] Batch evaluation for multiple students
- [ ] Integration with Learning Management Systems (LMS)
- [ ] Support for diagram/equation recognition
- [ ] Multi-language support
- [ ] Plagiarism detection
- [ ] Detailed analytics dashboard
- [ ] API endpoints for external integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Grade 10 & 11 Science Textbooks for training data
- NLTK and scikit-learn communities
- Open-source NLP research community

## 📧 Contact

For questions or support, please open an issue or contact [your.email@example.com](mailto:your.email@example.com)

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ for education**
