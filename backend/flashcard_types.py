"""
Type definitions for flashcard questions.

This module provides TypedDict classes for structured flashcard questions
used in the Quiz Me mode. These types help with IDE autocomplete and type checking.
"""

from typing import TypedDict, List, Dict, Optional


class ConceptQuestion(TypedDict):
    """
    Question about distributed systems concepts.
    
    Examples: CAP theorem, consistency models, ACID properties
    """
    id: str
    category: str
    question: str
    answer: str
    key_points: List[str]


class PatternQuestionWithComparison(TypedDict):
    """
    Pattern question with comparison table (e.g., WebSockets vs SSE vs Long Polling).
    """
    id: str
    category: str
    question: str
    answer: str
    comparison: Dict[str, str]


class PatternQuestionWithKeyPoints(TypedDict):
    """
    Pattern question with key points list (most pattern questions).
    """
    id: str
    category: str
    question: str
    answer: str
    key_points: List[str]


class NumbersQuestion(TypedDict):
    """
    Question about latency, throughput, capacity, or scale numbers.
    
    Uses 'context' field instead of 'key_points' to provide reference context.
    """
    id: str
    category: str
    question: str
    answer: str
    context: str


class TechnologyQuestion(TypedDict):
    """
    Technology selection question with multiple choice options.
    
    Note: This structure may be used if TECHNOLOGY_QUESTIONS exists in the codebase.
    """
    id: str
    category: str
    question: str
    options: List[Dict[str, str]]
    correct_answer: str
    explanation: str
    key_considerations: Optional[List[str]]
    limitations: Optional[List[str]]
