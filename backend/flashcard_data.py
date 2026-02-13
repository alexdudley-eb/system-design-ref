# Flashcard questions for Quiz Me mode
# Categories: Technology, Concepts, Patterns, Numbers

CONCEPT_QUESTIONS = [
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
            "Example: MongoDB is CP, Cassandra is AP"
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

PATTERN_QUESTIONS = [
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

NUMBERS_QUESTIONS = [
    {
        "id": "numbers-1",
        "category": "Latency",
        "question": "What is the typical latency for a RAM access?",
        "answer": "100 nanoseconds (ns)",
        "context": "This is 1,500x faster than SSD random read (150 μs)"
    },
    {
        "id": "numbers-2",
        "category": "Latency",
        "question": "What is the typical latency for an SSD random read?",
        "answer": "150 microseconds (μs)",
        "context": "This is 1,500x slower than RAM but 100x faster than HDD"
    },
    {
        "id": "numbers-3",
        "category": "Latency",
        "question": "What is the typical latency for network within same datacenter?",
        "answer": "0.5 milliseconds (ms)",
        "context": "Baseline for microservice communication"
    },
    {
        "id": "numbers-4",
        "category": "Latency",
        "question": "What is the typical latency for network between US coasts (SF to NYC)?",
        "answer": "40 milliseconds (ms)",
        "context": "Important for multi-region deployments"
    },
    {
        "id": "numbers-5",
        "category": "Throughput",
        "question": "How much data can Kafka handle per second per partition?",
        "answer": "~10 MB/s per partition",
        "context": "Use multiple partitions for higher throughput"
    },
    {
        "id": "numbers-6",
        "category": "Throughput",
        "question": "How many requests can a typical web server handle per second?",
        "answer": "~1,000-10,000 requests/second",
        "context": "Depends on request complexity and server specs"
    },
    {
        "id": "numbers-7",
        "category": "Storage",
        "question": "How much storage does YouTube handle?",
        "answer": "~1 exabyte (1,000 petabytes)",
        "context": "Reference for large-scale video storage systems"
    },
    {
        "id": "numbers-8",
        "category": "Scale",
        "question": "How many tweets are sent per day?",
        "answer": "~500 million tweets/day",
        "context": "~6,000 tweets/second average, 10,000+ peak"
    },
    {
        "id": "numbers-9",
        "category": "Scale",
        "question": "How many Google searches per day?",
        "answer": "~8 billion searches/day",
        "context": "~90,000 searches/second average"
    },
    {
        "id": "numbers-10",
        "category": "QPS",
        "question": "What is a typical read:write ratio for social media?",
        "answer": "100:1 (read-heavy)",
        "context": "Optimize for read performance with caching and replicas"
    },
    {
        "id": "numbers-11",
        "category": "Capacity",
        "question": "How many connections can a typical load balancer handle?",
        "answer": "~50,000-100,000 concurrent connections",
        "context": "Modern load balancers like HAProxy, NGINX"
    },
    {
        "id": "numbers-12",
        "category": "Bandwidth",
        "question": "What is typical internet bandwidth per user?",
        "answer": "~100 Mbps (home), ~1 Gbps (datacenter)",
        "context": "Use for calculating video streaming bitrates"
    },
    {
        "id": "numbers-13",
        "category": "Database",
        "question": "How many queries per second can MySQL handle?",
        "answer": "~10,000 simple queries/second",
        "context": "With proper indexing and hardware"
    },
    {
        "id": "numbers-14",
        "category": "Cache",
        "question": "What is a good cache hit ratio?",
        "answer": "80-90%",
        "context": "Below 70% suggests cache is not effective"
    },
    {
        "id": "numbers-15",
        "category": "Availability",
        "question": "How much downtime does 99.99% availability allow per year?",
        "answer": "52 minutes per year",
        "context": "Also called 'four nines' availability"
    }
]

ALL_FLASHCARD_QUESTIONS = CONCEPT_QUESTIONS + PATTERN_QUESTIONS + NUMBERS_QUESTIONS
