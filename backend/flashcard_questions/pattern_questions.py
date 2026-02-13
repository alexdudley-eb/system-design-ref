"""
Pattern questions for system design and architecture patterns.

Covers real-time communication, resilience patterns (Circuit Breaker, Bulkhead),
distributed transactions (Saga), data management (Outbox, CQRS, Event Sourcing),
deployment strategies, and architectural patterns.
"""

from typing import List, Union
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flashcard_types import (
    PatternQuestionWithComparison,
    PatternQuestionWithKeyPoints,
)

PatternQuestion = Union[PatternQuestionWithComparison, PatternQuestionWithKeyPoints]

PATTERN_QUESTIONS: List[PatternQuestion] = [
    {
        "id": "pattern-1",
        "category": "Real-time Communication",
        "question": "Name 3 ways to handle real-time updates to clients.",
        "answer": "WebSockets, Server-Sent Events (SSE), Long Polling",
        "comparison": {
            "WebSockets": "Bidirectional, low latency, stateful connection",
            "SSE": "Unidirectional (server→client), auto-reconnect, simpler",
            "Long Polling": "Works everywhere, higher latency, more overhead"
        }
    },
    {
        "id": "pattern-2",
        "category": "Resilience",
        "question": "What is the Circuit Breaker pattern?",
        "answer": "A pattern that prevents cascading failures by detecting faults and stopping requests to failing services temporarily.",
        "key_points": [
            "States: Closed (normal), Open (failing), Half-Open (testing)",
            "Fails fast instead of waiting for timeouts",
            "Used in microservices with libraries like Hystrix, Resilience4j"
        ]
    },
    {
        "id": "pattern-3",
        "category": "Distributed Transactions",
        "question": "What is the Saga pattern?",
        "answer": "A pattern for managing distributed transactions through a sequence of local transactions, with compensating transactions for rollback.",
        "key_points": [
            "Choreography: Events trigger next steps",
            "Orchestration: Central coordinator",
            "Used instead of 2PC for long-running transactions"
        ]
    },
    {
        "id": "pattern-4",
        "category": "Data Management",
        "question": "What is the Outbox pattern?",
        "answer": "A pattern ensuring reliable message publishing by writing messages to an outbox table in the same transaction as business data.",
        "key_points": [
            "Solves dual-write problem",
            "Message relay polls outbox and publishes",
            "Guarantees at-least-once delivery"
        ]
    },
    {
        "id": "pattern-5",
        "category": "Architecture",
        "question": "What is CQRS (Command Query Responsibility Segregation)?",
        "answer": "A pattern separating read and write operations into different models, allowing independent optimization.",
        "key_points": [
            "Commands: Mutate state",
            "Queries: Read state (possibly from replicas)",
            "Often combined with Event Sourcing"
        ]
    },
    {
        "id": "pattern-6",
        "category": "Data Management",
        "question": "What is Event Sourcing?",
        "answer": "A pattern where state changes are stored as a sequence of events, rather than just the current state.",
        "key_points": [
            "Complete audit trail",
            "Can replay events to rebuild state",
            "Challenges: Event schema evolution, storage size"
        ]
    },
    {
        "id": "pattern-7",
        "category": "Caching",
        "question": "What is the Cache-Aside pattern?",
        "answer": "Application code manually loads data from cache, and on cache miss, loads from database and populates cache.",
        "key_points": [
            "Also called Lazy Loading",
            "Cache only contains requested data",
            "Application controls cache logic"
        ]
    },
    {
        "id": "pattern-8",
        "category": "Microservices",
        "question": "What is the Strangler Fig pattern?",
        "answer": "Incrementally replacing a monolithic system by routing traffic to new microservices while keeping the monolith running.",
        "key_points": [
            "Named after fig vines that gradually replace trees",
            "Low-risk migration strategy",
            "Both systems run in parallel during transition"
        ]
    },
    {
        "id": "pattern-9",
        "category": "Resilience",
        "question": "What is the Bulkhead pattern?",
        "answer": "Isolating system resources into pools to prevent cascading failures if one pool is exhausted.",
        "key_points": [
            "Named after ship bulkheads",
            "Example: Separate thread pools per service",
            "Limits blast radius of failures"
        ]
    },
    {
        "id": "pattern-10",
        "category": "Retry Logic",
        "question": "What is exponential backoff with jitter?",
        "answer": "A retry strategy where wait time increases exponentially with random jitter added to prevent thundering herd.",
        "key_points": [
            "Prevents synchronized retries",
            "Example: 1s, 2s, 4s, 8s (with random ±30%)",
            "Essential for distributed systems"
        ]
    },
    {
        "id": "pattern-11",
        "category": "Data Access",
        "question": "What is the Repository pattern?",
        "answer": "An abstraction layer that encapsulates data access logic, providing a collection-like interface for domain objects.",
        "key_points": [
            "Separates business logic from data access",
            "Makes testing easier with mocks",
            "Centralizes query logic"
        ]
    },
    {
        "id": "pattern-12",
        "category": "Messaging",
        "question": "What is the Pub/Sub (Publish-Subscribe) pattern?",
        "answer": "A messaging pattern where publishers send messages to topics, and subscribers receive messages from topics they're interested in.",
        "key_points": [
            "Decouples producers and consumers",
            "Supports multiple subscribers per topic",
            "Used in Kafka, Redis Pub/Sub, SNS"
        ]
    },
    {
        "id": "pattern-13",
        "category": "Deployment",
        "question": "What is Blue-Green deployment?",
        "answer": "Running two identical production environments (blue and green), switching traffic between them for zero-downtime deployments.",
        "key_points": [
            "Easy rollback by switching traffic back",
            "Requires 2x infrastructure temporarily",
            "Used for risk-free deployments"
        ]
    },
    {
        "id": "pattern-14",
        "category": "Deployment",
        "question": "What is Canary deployment?",
        "answer": "Gradually rolling out changes to a small subset of users before full deployment.",
        "key_points": [
            "Monitor metrics from canary group",
            "Rollback if issues detected",
            "Lower risk than big-bang deployment"
        ]
    },
    {
        "id": "pattern-15",
        "category": "API Design",
        "question": "What is the Backend for Frontend (BFF) pattern?",
        "answer": "Creating separate backend services tailored to specific frontend applications (web, mobile, etc.).",
        "key_points": [
            "Each BFF optimized for its client",
            "Reduces over-fetching and under-fetching",
            "Trade-off: More code to maintain"
        ]
    }
]
