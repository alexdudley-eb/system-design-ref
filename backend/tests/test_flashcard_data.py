"""
Tests for flashcard question data integrity and structure.

Verifies that all flashcard questions have required fields,
unique IDs, and educationally correct content.
"""

import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flashcard_questions import CONCEPT_QUESTIONS, PATTERN_QUESTIONS, NUMBERS_QUESTIONS, ALL_FLASHCARD_QUESTIONS


class TestConceptQuestions:
    """Test concept question structure and content."""
    
    def test_all_have_required_fields(self):
        """Verify all concept questions have required fields."""
        required_fields = ['id', 'category', 'question', 'answer', 'key_points']
        
        for q in CONCEPT_QUESTIONS:
            for field in required_fields:
                assert field in q, f"Question {q.get('id', 'unknown')} missing field: {field}"
            
            assert isinstance(q['key_points'], list), f"Question {q['id']}: key_points must be a list"
            assert len(q['key_points']) > 0, f"Question {q['id']}: key_points cannot be empty"
    
    def test_unique_ids(self):
        """Verify no duplicate IDs in concept questions."""
        ids = [q['id'] for q in CONCEPT_QUESTIONS]
        assert len(ids) == len(set(ids)), "Duplicate IDs found in CONCEPT_QUESTIONS"
    
    def test_cap_theorem_accuracy(self):
        """Verify CAP theorem example is educationally correct."""
        cap_q = next((q for q in CONCEPT_QUESTIONS if q['id'] == 'concept-3'), None)
        assert cap_q is not None, "CAP theorem question (concept-3) not found"
        
        example_text = cap_q['key_points'][2].lower()
        assert 'tunable' in example_text or 'configur' in example_text, \
            "CAP theorem should mention MongoDB is tunable, not strictly CP"
    
    def test_minimum_question_count(self):
        """Verify we have enough concept questions."""
        assert len(CONCEPT_QUESTIONS) >= 20, "Should have at least 20 concept questions"


class TestPatternQuestions:
    """Test pattern question structure and content."""
    
    def test_all_have_required_fields(self):
        """Verify all pattern questions have required fields."""
        required_base_fields = ['id', 'category', 'question', 'answer']
        
        for q in PATTERN_QUESTIONS:
            for field in required_base_fields:
                assert field in q, f"Question {q.get('id', 'unknown')} missing field: {field}"
            
            has_comparison = 'comparison' in q
            has_key_points = 'key_points' in q
            assert has_comparison or has_key_points, \
                f"Question {q['id']} must have either 'comparison' or 'key_points'"
    
    def test_unique_ids(self):
        """Verify no duplicate IDs in pattern questions."""
        ids = [q['id'] for q in PATTERN_QUESTIONS]
        assert len(ids) == len(set(ids)), "Duplicate IDs found in PATTERN_QUESTIONS"
    
    def test_pattern_1_has_comparison(self):
        """Verify pattern-1 (real-time communication) has comparison dict."""
        pattern_1 = next((q for q in PATTERN_QUESTIONS if q['id'] == 'pattern-1'), None)
        assert pattern_1 is not None, "Pattern-1 question not found"
        assert 'comparison' in pattern_1, "Pattern-1 should have comparison dict"
        assert isinstance(pattern_1['comparison'], dict), "comparison must be a dict"
    
    def test_minimum_question_count(self):
        """Verify we have enough pattern questions."""
        assert len(PATTERN_QUESTIONS) >= 10, "Should have at least 10 pattern questions"


class TestNumbersQuestions:
    """Test numbers question structure and content."""
    
    def test_all_have_required_fields(self):
        """Verify all numbers questions have required fields."""
        required_fields = ['id', 'category', 'question', 'answer', 'context']
        
        for q in NUMBERS_QUESTIONS:
            for field in required_fields:
                assert field in q, f"Question {q.get('id', 'unknown')} missing field: {field}"
            
            assert isinstance(q['context'], str), f"Question {q['id']}: context must be a string"
            assert len(q['context']) > 0, f"Question {q['id']}: context cannot be empty"
    
    def test_unique_ids(self):
        """Verify no duplicate IDs in numbers questions."""
        ids = [q['id'] for q in NUMBERS_QUESTIONS]
        assert len(ids) == len(set(ids)), "Duplicate IDs found in NUMBERS_QUESTIONS"
    
    def test_minimum_question_count(self):
        """Verify we have enough numbers questions."""
        assert len(NUMBERS_QUESTIONS) >= 10, "Should have at least 10 numbers questions"


class TestAllQuestions:
    """Test combined question bank integrity."""
    
    def test_globally_unique_ids(self):
        """Verify no duplicate IDs across all question categories."""
        all_ids = [q['id'] for q in ALL_FLASHCARD_QUESTIONS]
        assert len(all_ids) == len(set(all_ids)), "Duplicate IDs found across all flashcard questions"
    
    def test_all_questions_combined(self):
        """Verify ALL_FLASHCARD_QUESTIONS contains all questions."""
        expected_count = len(CONCEPT_QUESTIONS) + len(PATTERN_QUESTIONS) + len(NUMBERS_QUESTIONS)
        assert len(ALL_FLASHCARD_QUESTIONS) == expected_count, \
            f"ALL_FLASHCARD_QUESTIONS should have {expected_count} questions"
    
    def test_total_question_count(self):
        """Verify we have a healthy total question bank."""
        assert len(ALL_FLASHCARD_QUESTIONS) >= 40, \
            "Should have at least 40 total flashcard questions for variety"
