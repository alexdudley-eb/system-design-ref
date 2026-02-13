"""
Tests for API endpoints related to quiz and flashcard functionality.

Covers:
- Quiz question endpoints (/api/quiz/question, /api/quiz/questions)
- Flashcard endpoints (/api/flashcard/question, /api/flashcard/questions)
- Response formats and data integrity
- Question distribution and randomization
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


class TestQuizQuestionEndpoints:
    """Test quiz question API endpoints."""
    
    def test_get_single_random_question(self):
        """Test getting a random quiz question."""
        response = client.get('/api/quiz/question')
        assert response.status_code == 200
        
        data = response.json()
        assert 'id' in data
        assert 'type' in data
        assert data['type'] in ['scenario', 'technology']
        
        if data['type'] == 'scenario':
            assert 'scenario' in data
            assert 'question' in data
        elif data['type'] == 'technology':
            assert 'question' in data
            assert 'options' in data
            assert 'correct_answer' in data
    
    def test_get_scenario_question(self):
        """Test getting a scenario question specifically."""
        response = client.get('/api/quiz/question?question_type=scenario')
        assert response.status_code == 200
        
        data = response.json()
        assert data['type'] == 'scenario'
        assert 'scenario' in data
        assert 'question' in data
    
    def test_get_technology_question(self):
        """Test getting a technology question specifically."""
        response = client.get('/api/quiz/question?question_type=technology')
        assert response.status_code == 200
        
        data = response.json()
        assert data['type'] == 'technology'
        assert 'options' in data
        assert len(data['options']) == 4
        assert 'correct_answer' in data
    
    def test_get_multiple_questions_default(self):
        """Test getting multiple quiz questions with default count."""
        response = client.get('/api/quiz/questions')
        assert response.status_code == 200
        
        data = response.json()
        assert 'questions' in data
        assert len(data['questions']) == 5
    
    def test_get_multiple_questions_custom_count(self):
        """Test getting multiple quiz questions with custom count."""
        for count in [1, 3, 5, 10]:
            response = client.get(f'/api/quiz/questions?count={count}')
            assert response.status_code == 200
            
            data = response.json()
            assert 'questions' in data
            assert len(data['questions']) == count
    
    def test_no_duplicate_questions_in_set(self):
        """Test that a single request doesn't return duplicate questions."""
        response = client.get('/api/quiz/questions?count=10')
        assert response.status_code == 200
        
        data = response.json()
        questions = data['questions']
        question_ids = [q['id'] for q in questions]
        
        assert len(question_ids) == len(set(question_ids)), \
            "Duplicate questions found in single request"
    
    def test_question_distribution(self):
        """Test that scenario/technology distribution is roughly 70/30."""
        scenario_count = 0
        tech_count = 0
        iterations = 100
        
        for _ in range(iterations):
            response = client.get('/api/quiz/question')
            assert response.status_code == 200
            
            q = response.json()
            if q['type'] == 'scenario':
                scenario_count += 1
            else:
                tech_count += 1
        
        scenario_pct = (scenario_count / iterations) * 100
        assert 60 <= scenario_pct <= 80, \
            f"Expected 60-80% scenarios, got {scenario_pct}%"


class TestFlashcardEndpoints:
    """Test flashcard API endpoints."""
    
    def test_get_single_random_flashcard(self):
        """Test getting a random flashcard."""
        response = client.get('/api/flashcard/question')
        assert response.status_code == 200
        
        data = response.json()
        assert 'id' in data
        assert 'question' in data
        assert 'answer' in data
        assert 'category' in data
    
    def test_get_concept_flashcard(self):
        """Test getting a concept category flashcard."""
        response = client.get('/api/flashcard/question?category=concept')
        assert response.status_code == 200
        
        data = response.json()
        assert 'key_points' in data
        assert isinstance(data['key_points'], list)
    
    def test_get_pattern_flashcard(self):
        """Test getting a pattern category flashcard."""
        response = client.get('/api/flashcard/question?category=pattern')
        assert response.status_code == 200
        
        data = response.json()
        has_comparison_or_points = 'comparison' in data or 'key_points' in data
        assert has_comparison_or_points, \
            "Pattern questions should have comparison or key_points"
    
    def test_get_numbers_flashcard(self):
        """Test getting a numbers category flashcard."""
        response = client.get('/api/flashcard/question?category=numbers')
        assert response.status_code == 200
        
        data = response.json()
        assert 'context' in data
        assert isinstance(data['context'], str)
    
    def test_get_flashcard_set_default(self):
        """Test getting multiple flashcards with defaults."""
        response = client.get('/api/flashcard/questions')
        assert response.status_code == 200
        
        data = response.json()
        assert 'questions' in data
        assert len(data['questions']) == 10
    
    def test_get_flashcard_set_custom_count(self):
        """Test getting flashcards with custom count."""
        for count in [5, 10, 15, 20]:
            response = client.get(f'/api/flashcard/questions?count={count}')
            assert response.status_code == 200
            
            data = response.json()
            assert len(data['questions']) == count
    
    def test_get_flashcard_set_by_category(self):
        """Test filtering flashcards by category."""
        categories = ['concept', 'pattern', 'numbers']
        
        for category in categories:
            response = client.get(f'/api/flashcard/questions?count=10&category={category}')
            assert response.status_code == 200
            
            data = response.json()
            assert len(data['questions']) == 10
    
    def test_no_duplicate_flashcards_in_set(self):
        """Test that a single request doesn't return duplicate flashcards."""
        response = client.get('/api/flashcard/questions?count=20')
        assert response.status_code == 200
        
        data = response.json()
        flashcards = data['questions']
        flashcard_ids = [f['id'] for f in flashcards]
        
        assert len(flashcard_ids) == len(set(flashcard_ids)), \
            "Duplicate flashcards found in single request"


class TestErrorHandling:
    """Test API error handling and validation."""
    
    def test_invalid_question_type(self):
        """Test that invalid question_type returns error."""
        response = client.get('/api/quiz/question?question_type=invalid')
        assert response.status_code == 422
    
    def test_quiz_count_below_minimum(self):
        """Test that count below minimum is rejected."""
        response = client.get('/api/quiz/questions?count=0')
        assert response.status_code == 422
    
    def test_quiz_count_above_maximum(self):
        """Test that count above maximum is rejected."""
        response = client.get('/api/quiz/questions?count=11')
        assert response.status_code == 422
    
    def test_flashcard_count_below_minimum(self):
        """Test that flashcard count below minimum is rejected."""
        response = client.get('/api/flashcard/questions?count=4')
        assert response.status_code == 422
    
    def test_flashcard_count_above_maximum(self):
        """Test that flashcard count above maximum is rejected."""
        response = client.get('/api/flashcard/questions?count=21')
        assert response.status_code == 422
