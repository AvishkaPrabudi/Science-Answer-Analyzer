from modules.preprocessor import TextPreprocessor
from modules.keyword_extractor import KeywordExtractor
from modules.comparator import AnswerComparator
from modules.science_vocabulary import ScienceVocabularyBuilder

class AnswerEvaluator:
    """
    Complete system to evaluate student answers
    """
    
    def __init__(self, vocabulary_file="trained_data/science_vocabulary.json"):
        self.preprocessor = TextPreprocessor()
        self.keyword_extractor = KeywordExtractor(max_keywords=15)
        self.comparator = AnswerComparator()
        self.vocab_builder = ScienceVocabularyBuilder()
        
        # Load trained vocabulary
        if self.vocab_builder.load_vocabulary(vocabulary_file):
            print("✓ Loaded textbook vocabulary")
        else:
            print("⚠ Running without textbook vocabulary")
    
    def evaluate_answer(self, model_answer, student_answer, subject="general", max_marks=10):
        """
        Evaluate a student answer against model answer
        
        Returns:
            dict with score, feedback, matched_keywords, missing_keywords
        """
        print("\n" + "="*70)
        print("EVALUATING ANSWER")
        print("="*70)
        
        # Preprocess both answers
        model_cleaned = self.preprocessor.preprocess_to_text(model_answer)
        student_cleaned = self.preprocessor.preprocess_to_text(student_answer)
        
        # Extract keywords from both
        model_keywords = self.keyword_extractor.extract_keywords(model_cleaned, top_n=10)
        student_keywords = self.keyword_extractor.extract_keywords(student_cleaned, top_n=10)
        
        print("\nMODEL ANSWER KEYWORDS:")
        for word, score in model_keywords:
            is_textbook_term = self.vocab_builder.check_if_science_term(word, subject)
            marker = "📘" if is_textbook_term else "  "
            print(f"  {marker} {word}: {score:.3f}")
        
        print("\nSTUDENT ANSWER KEYWORDS:")
        for word, score in student_keywords:
            is_textbook_term = self.vocab_builder.check_if_science_term(word, subject)
            marker = "📘" if is_textbook_term else "  "
            print(f"  {marker} {word}: {score:.3f}")
        
        # Calculate similarity
        similarity = self.comparator.calculate_similarity(model_cleaned, student_cleaned)
        
        # Find matched and missing keywords
        matched, missing = self.comparator.find_matched_keywords(model_keywords, student_keywords)
        
        # Calculate score
        keyword_match_ratio = len(matched) / len(model_keywords) if model_keywords else 0
        
        # Weighted scoring: 60% similarity + 40% keyword match
        final_score_ratio = (similarity * 0.6) + (keyword_match_ratio * 0.4)
        final_score = round(final_score_ratio * max_marks, 2)
        
        # Generate feedback
        feedback = self._generate_feedback(final_score_ratio, matched, missing, max_marks)
        
        result = {
            "score": final_score,
            "max_marks": max_marks,
            "percentage": round(final_score_ratio * 100, 1),
            "similarity": round(similarity * 100, 1),
            "keyword_match": round(keyword_match_ratio * 100, 1),
            "matched_keywords": matched,
            "missing_keywords": missing,
            "feedback": feedback
        }
        
        return result
    
    def _generate_feedback(self, score_ratio, matched, missing, max_marks):
        """Generate detailed feedback for student"""
        feedback = []
        
        if score_ratio >= 0.8:
            feedback.append("✅ Excellent answer! All key concepts covered.")
        elif score_ratio >= 0.6:
            feedback.append("✓ Good answer. Most key concepts present.")
        elif score_ratio >= 0.4:
            feedback.append("⚠ Average answer. Some important concepts missing.")
        else:
            feedback.append("❌ Needs improvement. Many key concepts missing.")
        
        if matched:
            feedback.append(f"\n✓ Keywords found: {', '.join(matched)}")
        
        if missing:
            feedback.append(f"\n✗ Missing keywords: {', '.join(missing)}")
            feedback.append(f"  → Focus on these concepts to improve your answer.")
        
        return "\n".join(feedback)
    
    def print_result(self, result):
        """Pretty print the evaluation result"""
        print("\n" + "="*70)
        print("EVALUATION RESULT")
        print("="*70)
        print(f"\n📊 SCORE: {result['score']}/{result['max_marks']} ({result['percentage']}%)")
        print(f"\n📈 METRICS:")
        print(f"   • Overall Similarity: {result['similarity']}%")
        print(f"   • Keyword Match: {result['keyword_match']}%")
        print(f"\n💬 FEEDBACK:")
        print(result['feedback'])
        print("\n" + "="*70)


# TEST THE EVALUATOR
if __name__ == "__main__":
    evaluator = AnswerEvaluator()
    
    # Example: Grade 10 Biology question
    model_answer = """
    Photosynthesis is the process by which green plants convert light energy 
    into chemical energy. It occurs in chloroplasts using chlorophyll pigment. 
    The process uses carbon dioxide and water to produce glucose and oxygen. 
    The equation is: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2
    """
    
    # Good student answer
    student_answer_good = """
    Photosynthesis is when plants make food using sunlight. It happens in 
    chloroplasts with chlorophyll. Plants take carbon dioxide and water 
    and make glucose and oxygen gas.
    """
    
    # Average student answer
    student_answer_average = """
    Photosynthesis is the process where plants make food from sunlight.
    It produces oxygen.
    """
    
    # Poor student answer
    student_answer_poor = """
    Plants need sunlight to grow and they make oxygen.
    """
    
    print("\n" + "="*70)
    print("TESTING ANSWER EVALUATOR WITH DIFFERENT STUDENT RESPONSES")
    print("="*70)
    
    print("\n\n### TEST 1: GOOD ANSWER ###")
    result1 = evaluator.evaluate_answer(model_answer, student_answer_good, 
                                        subject="grade-10-science-part-i", 
                                        max_marks=10)
    evaluator.print_result(result1)
    
    print("\n\n### TEST 2: AVERAGE ANSWER ###")
    result2 = evaluator.evaluate_answer(model_answer, student_answer_average, 
                                        subject="grade-10-science-part-i", 
                                        max_marks=10)
    evaluator.print_result(result2)
    
    print("\n\n### TEST 3: POOR ANSWER ###")
    result3 = evaluator.evaluate_answer(model_answer, student_answer_poor, 
                                        subject="grade-10-science-part-i", 
                                        max_marks=10)
    evaluator.print_result(result3)