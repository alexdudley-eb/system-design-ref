"""
Concept questions for distributed systems and database fundamentals.

Covers CAP theorem, ACID, consistency models, replication, sharding,
caching strategies, indexing, and other core distributed systems concepts.
"""

from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flashcard_types import ConceptQuestion

CONCEPT_QUESTIONS: List[ConceptQuestion] = [
    {
        "id": "concept-1",
        "category": "Consistency Models",
        "question": "What is eventual consistency?",
        "answer": "A consistency model where all replicas eventually converge to the same value after writes stop, but may temporarily show different values.",
        "key_points": [
            "Prioritizes availability over immediate consistency",
            "Common in distributed systems (DynamoDB, Cassandra)",
            "Trade-off: Higher availability, lower consistency guarantee"
        ]
    },
    {
        "id": "concept-2",
        "category": "Consistency Models",
        "question": "What is strong consistency?",
        "answer": "A consistency model where all reads return the most recent write, ensuring all replicas are always synchronized.",
        "key_points": [
            "Guarantees linearizability",
            "Common in relational databases",
            "Trade-off: Lower availability, higher latency"
        ]
    },
    {
        "id": "concept-3",
        "category": "CAP Theorem",
        "question": "What does the CAP theorem state?",
        "answer": "In a distributed system, you can only guarantee 2 out of 3: Consistency, Availability, and Partition tolerance.",
        "key_points": [
            "Partition tolerance is usually required in distributed systems",
            "Must choose between CP (Consistency + Partition) or AP (Availability + Partition)",
            "Example: MongoDB is tunable (CP with majority writes), Cassandra is AP"
        ]
    },
    {
        "id": "concept-4",
        "category": "ACID",
        "question": "What does ACID stand for in databases?",
        "answer": "Atomicity, Consistency, Isolation, Durability - properties that guarantee reliable transaction processing.",
        "key_points": [
            "Atomicity: All or nothing",
            "Consistency: Valid state transitions",
            "Isolation: Concurrent transactions don't interfere",
            "Durability: Committed data persists"
        ]
    },
    {
        "id": "concept-5",
        "category": "BASE",
        "question": "What does BASE stand for in distributed systems?",
        "answer": "Basically Available, Soft state, Eventually consistent - an alternative to ACID for distributed systems.",
        "key_points": [
            "Prioritizes availability over consistency",
            "Used in NoSQL databases",
            "Accepts temporary inconsistency"
        ]
    },
    {
        "id": "concept-6",
        "category": "Sharding",
        "question": "What is database sharding?",
        "answer": "Horizontal partitioning where data is split across multiple database servers based on a shard key.",
        "key_points": [
            "Improves scalability and performance",
            "Challenges: Resharding, hotspots, joins across shards",
            "Common strategies: Hash-based, Range-based, Geographic"
        ]
    },
    {
        "id": "concept-7",
        "category": "Replication",
        "question": "What is the difference between leader-follower and multi-leader replication?",
        "answer": "Leader-follower has one primary for writes and multiple replicas for reads; multi-leader has multiple nodes that accept writes.",
        "key_points": [
            "Leader-follower: Simpler, single write path, read scalability",
            "Multi-leader: Better write availability, conflict resolution needed",
            "Multi-leader used for multi-datacenter setups"
        ]
    },
    {
        "id": "concept-8",
        "category": "Load Balancing",
        "question": "What are the main load balancing algorithms?",
        "answer": "Round Robin, Least Connections, Weighted Round Robin, IP Hash, Random, Least Response Time.",
        "key_points": [
            "Round Robin: Simple, equal distribution",
            "Least Connections: Better for varying request loads",
            "IP Hash: Session affinity, same user → same server"
        ]
    },
    {
        "id": "concept-9",
        "category": "Caching Strategies",
        "question": "What is the difference between write-through and write-back caching?",
        "answer": "Write-through writes to cache and database synchronously; write-back writes to cache first, then asynchronously to database.",
        "key_points": [
            "Write-through: Lower latency for reads, slower writes, strong consistency",
            "Write-back: Faster writes, risk of data loss, eventual consistency",
            "Write-back used for high-write systems"
        ]
    },
    {
        "id": "concept-10",
        "category": "Caching Strategies",
        "question": "What are the main cache eviction policies?",
        "answer": "LRU (Least Recently Used), LFU (Least Frequently Used), FIFO (First In First Out), Random.",
        "key_points": [
            "LRU: Best for temporal locality (recent access patterns)",
            "LFU: Best for frequency-based patterns",
            "FIFO: Simple but not optimal"
        ]
    },
    {
        "id": "concept-11",
        "category": "Indexing",
        "question": "What is the difference between B-tree and LSM-tree indexes?",
        "answer": "B-tree optimizes for reads with in-place updates; LSM-tree optimizes for writes with sequential writes and compaction.",
        "key_points": [
            "B-tree: Better read performance, used in MySQL, PostgreSQL",
            "LSM-tree: Better write performance, used in Cassandra, RocksDB",
            "LSM-tree trades read performance for write throughput"
        ]
    },
    {
        "id": "concept-12",
        "category": "Message Queues",
        "question": "What is the difference between at-most-once, at-least-once, and exactly-once delivery?",
        "answer": "At-most-once delivers 0-1 times (may lose messages), at-least-once delivers 1+ times (may duplicate), exactly-once delivers exactly 1 time.",
        "key_points": [
            "At-most-once: Fastest, lowest overhead, tolerates loss",
            "At-least-once: Most common, idempotent consumers needed",
            "Exactly-once: Hardest to implement, requires distributed transactions"
        ]
    },
    {
        "id": "concept-13",
        "category": "Rate Limiting",
        "question": "What are the main rate limiting algorithms?",
        "answer": "Token bucket, Leaky bucket, Fixed window counter, Sliding window log, Sliding window counter.",
        "key_points": [
            "Token bucket: Allows burst traffic",
            "Leaky bucket: Smooth rate, no bursts",
            "Sliding window: Most accurate, more complex"
        ]
    },
    {
        "id": "concept-14",
        "category": "Hashing",
        "question": "What is consistent hashing and why is it useful?",
        "answer": "A hashing scheme where adding/removing nodes only affects adjacent nodes, minimizing data redistribution.",
        "key_points": [
            "Used in distributed caching, sharding",
            "Virtual nodes for better distribution",
            "Only K/n keys need remapping (K=keys, n=nodes)"
        ]
    },
    {
        "id": "concept-15",
        "category": "Consensus",
        "question": "What is the purpose of consensus algorithms like Raft and Paxos?",
        "answer": "To achieve agreement on a single value among distributed nodes, even in the presence of failures.",
        "key_points": [
            "Used for leader election, log replication",
            "Requires majority (quorum) for decisions",
            "Raft is simpler and more understandable than Paxos"
        ]
    },
    {
        "id": "concept-16",
        "category": "Microservices",
        "question": "What is service discovery and why is it needed?",
        "answer": "A mechanism for services to find and communicate with each other dynamically, without hardcoded addresses.",
        "key_points": [
            "Client-side: Service queries registry (Consul, Eureka)",
            "Server-side: Load balancer handles routing",
            "Needed for dynamic scaling and deployment"
        ]
    },
    {
        "id": "concept-17",
        "category": "Data Partitioning",
        "question": "What are hot spots in data partitioning and how do you avoid them?",
        "answer": "Hot spots occur when certain partitions receive disproportionately high traffic. Avoid with better shard keys, consistent hashing, or synthetic keys.",
        "key_points": [
            "Celebrity problem: Popular users create hot partitions",
            "Use compound keys or add randomness",
            "Monitor partition metrics"
        ]
    },
    {
        "id": "concept-18",
        "category": "API Design",
        "question": "What is the difference between REST and GraphQL?",
        "answer": "REST uses fixed endpoints returning predefined data structures; GraphQL uses a single endpoint where clients specify exactly what data they need.",
        "key_points": [
            "REST: Simple, cacheable, over-fetching/under-fetching",
            "GraphQL: Flexible queries, no over-fetching, complex caching",
            "GraphQL better for mobile clients with varying needs"
        ]
    },
    {
        "id": "concept-19",
        "category": "Security",
        "question": "What is the difference between authentication and authorization?",
        "answer": "Authentication verifies who you are (identity); authorization determines what you can do (permissions).",
        "key_points": [
            "Authentication: Username/password, OAuth, JWT",
            "Authorization: RBAC, ABAC, ACLs",
            "Both needed for secure systems"
        ]
    },
    {
        "id": "concept-20",
        "category": "Distributed Transactions",
        "question": "What is the Two-Phase Commit (2PC) protocol?",
        "answer": "A distributed transaction protocol where a coordinator ensures all participants either commit or abort together.",
        "key_points": [
            "Phase 1: Prepare (vote)",
            "Phase 2: Commit/Abort",
            "Blocking protocol, not partition-tolerant"
        ]
    },
    {
        "id": "concept-21",
        "category": "API Gateway",
        "question": "What is an API Gateway and what problems does it solve?",
        "answer": "A reverse proxy that provides a single entry point for clients, handling routing, authentication, rate limiting, and protocol translation.",
        "key_points": [
            "Simplifies client-side logic",
            "Cross-cutting concerns (auth, logging, rate limiting)",
            "Can become a bottleneck if not scaled"
        ]
    },
    {
        "id": "concept-22",
        "category": "Data Streaming",
        "question": "What is the difference between batch processing and stream processing?",
        "answer": "Batch processing processes large volumes of data at scheduled intervals; stream processing processes data continuously as it arrives.",
        "key_points": [
            "Batch: Higher latency, better for analytics, MapReduce",
            "Stream: Low latency, real-time, Kafka Streams, Flink",
            "Lambda architecture combines both"
        ]
    },
    {
        "id": "concept-23",
        "category": "Denormalization",
        "question": "What is denormalization and when should you use it?",
        "answer": "Storing redundant data to improve read performance by reducing joins.",
        "key_points": [
            "Trade-off: Read performance vs write complexity",
            "Use for read-heavy workloads",
            "Requires consistency mechanisms"
        ]
    },
    {
        "id": "concept-24",
        "category": "Data Formats",
        "question": "What are the trade-offs between JSON and Protocol Buffers?",
        "answer": "JSON is human-readable and flexible; Protocol Buffers are compact, type-safe, and faster to parse.",
        "key_points": [
            "JSON: Easy to debug, larger size, slower parsing",
            "Protobuf: Smaller size, requires schema, faster",
            "Protobuf better for internal microservices"
        ]
    },
    {
        "id": "concept-25",
        "category": "Availability",
        "question": "What does '99.99% availability' mean in practice?",
        "answer": "The system is down for no more than 52 minutes per year (0.01% of 8760 hours).",
        "key_points": [
            "99.9% = 43.8 minutes/month downtime",
            "99.99% = 4.38 minutes/month downtime",
            "Each 9 increases cost significantly"
        ]
    }
]
