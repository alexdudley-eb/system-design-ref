"""
Flashcard questions module for Quiz Me mode.

This module provides structured question banks for interview preparation:
- concept_questions: Distributed systems concepts
- pattern_questions: Design and architectural patterns  
- numbers_questions: Scale, latency, and performance metrics

All questions are re-exported here for easy importing:
    from flashcard_questions import CONCEPT_QUESTIONS, PATTERN_QUESTIONS, NUMBERS_QUESTIONS
"""

from .concept_questions import CONCEPT_QUESTIONS
from .pattern_questions import PATTERN_QUESTIONS
from .numbers_questions import NUMBERS_QUESTIONS

# Combined list of all flashcard questions
ALL_FLASHCARD_QUESTIONS = CONCEPT_QUESTIONS + PATTERN_QUESTIONS + NUMBERS_QUESTIONS

__all__ = [
    'CONCEPT_QUESTIONS',
    'PATTERN_QUESTIONS',
    'NUMBERS_QUESTIONS',
    'ALL_FLASHCARD_QUESTIONS',
]
