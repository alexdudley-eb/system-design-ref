# Reference data for system design interviews
# Based on Hello Interview and industry standards

NUMBERS_TO_KNOW = {
    "latency": [
        {
            "operation": "L1 cache reference",
            "value": "0.5 ns",
            "context": "CPU cache access",
            "usage": "Use for understanding CPU-level optimization"
        },
        {
            "operation": "L2 cache reference",
            "value": "7 ns",
            "context": "CPU cache access",
            "usage": "14x slower than L1"
        },
        {
            "operation": "Main memory (RAM) reference",
            "value": "100 ns",
            "context": "Memory access",
            "usage": "Baseline for in-memory operations"
        },
        {
            "operation": "SSD random read",
            "value": "150 μs",
            "context": "Persistent storage",
            "usage": "1,500x slower than RAM"
        },
        {
            "operation": "Network within same datacenter",
            "value": "0.5 ms",
            "context": "Network latency",
            "usage": "Microservice communication baseline"
        },
        {
            "operation": "SSD sequential read (1 MB)",
            "value": "1 ms",
            "context": "Persistent storage",
            "usage": "Reading large sequential data"
        },
        {
            "operation": "HDD seek",
            "value": "10 ms",
            "context": "Disk storage",
            "usage": "Avoid random disk access patterns"
        },
        {
            "operation": "Network: SF to NYC",
            "value": "40 ms",
            "context": "Cross-region latency",
            "usage": "Multi-region architecture consideration"
        },
        {
            "operation": "Network: SF to Europe",
            "value": "100 ms",
            "context": "Cross-region latency",
            "usage": "CDN becomes critical"
        },
        {
            "operation": "Network: SF to Asia",
            "value": "150 ms",
            "context": "Cross-region latency",
            "usage": "Consider regional deployments"
        }
    ],
    "throughput": [
        {
            "metric": "L1 cache throughput",
            "value": "100 GB/s",
            "context": "CPU cache bandwidth",
            "usage": "CPU-bound processing limit"
        },
        {
            "metric": "Memory bandwidth",
            "value": "10 GB/s",
            "context": "RAM bandwidth",
            "usage": "Memory-intensive operations"
        },
        {
            "metric": "SSD throughput",
            "value": "500 MB/s",
            "context": "Storage bandwidth",
            "usage": "Sequential read/write operations"
        },
        {
            "metric": "HDD throughput",
            "value": "100 MB/s",
            "context": "Disk bandwidth",
            "usage": "Sequential operations only"
        },
        {
            "metric": "1 Gbps network",
            "value": "125 MB/s",
            "context": "Network bandwidth",
            "usage": "Typical network interface"
        },
        {
            "metric": "10 Gbps network",
            "value": "1.25 GB/s",
            "context": "Network bandwidth",
            "usage": "High-performance networking"
        }
    ],
    "capacity": [
        {
            "item": "QPS per server (simple CRUD)",
            "value": "10,000 - 50,000",
            "context": "Application server capacity",
            "usage": "Baseline for horizontal scaling calculations"
        },
        {
            "item": "Database connections per instance",
            "value": "100 - 500",
            "context": "PostgreSQL/MySQL typical",
            "usage": "Connection pooling sizing"
        },
        {
            "item": "Redis operations per second",
            "value": "100,000+",
            "context": "Single Redis instance",
            "usage": "Cache sizing and sharding decisions"
        },
        {
            "item": "WebSocket connections per server",
            "value": "10,000 - 100,000",
            "context": "Real-time connections",
            "usage": "Chat/streaming service scaling"
        },
        {
            "item": "CDN cache hit ratio target",
            "value": "90%+",
            "context": "Content delivery",
            "usage": "Expected cache performance"
        }
    ],
    "storage": [
        {
            "item": "Typical row size (metadata)",
            "value": "100 - 500 bytes",
            "context": "Database storage",
            "usage": "Storage capacity planning"
        },
        {
            "item": "Index overhead",
            "value": "~20% of data size",
            "context": "Database indexing",
            "usage": "Additional storage for indexes"
        },
        {
            "item": "Compression ratio (text)",
            "value": "3:1 to 10:1",
            "context": "Data compression",
            "usage": "Storage and bandwidth savings"
        },
        {
            "item": "Image size (high quality)",
            "value": "1-5 MB",
            "context": "Media storage",
            "usage": "CDN and storage planning"
        },
        {
            "item": "Video size (1080p, 1 min)",
            "value": "50-100 MB",
            "context": "Media storage",
            "usage": "Large blob handling"
        }
    ],
    "availability": [
        {
            "tier": "99.9% (three nines)",
            "downtime_per_year": "8.77 hours",
            "context": "Acceptable for most services",
            "usage": "Standard SLA target"
        },
        {
            "tier": "99.99% (four nines)",
            "downtime_per_year": "52.6 minutes",
            "context": "High availability services",
            "usage": "Financial/payment systems"
        },
        {
            "tier": "99.999% (five nines)",
            "downtime_per_year": "5.26 minutes",
            "context": "Mission-critical systems",
            "usage": "Requires multi-region, auto-failover"
        }
    ]
}

DELIVERY_FRAMEWORK = {
    "overview": "A structured approach to system design interviews that ensures comprehensive coverage and demonstrates strong problem navigation skills.",
    "time_allocation": {
        "total_time": "45 minutes",
        "requirements": "5-10 minutes",
        "high_level_design": "10-15 minutes",
        "deep_dives": "15-20 minutes",
        "wrap_up": "5 minutes"
    },
    "phases": [
        {
            "phase": "1. Requirements Gathering",
            "time": "5-10 minutes",
            "goal": "Narrow the problem scope and establish clear boundaries",
            "activities": [
                "Clarify functional requirements (what must the system do?)",
                "Define non-functional requirements (scale, latency, availability)",
                "Identify out-of-scope items explicitly",
                "Establish core entities and their relationships",
                "Define key API endpoints"
            ],
            "common_mistakes": [
                "Jumping to solutions before understanding the problem",
                "Not asking clarifying questions",
                "Assuming requirements without confirmation"
            ],
            "example_questions": [
                "What's the expected read-to-write ratio?",
                "Do we need strong or eventual consistency?",
                "What's the expected scale (users, requests per second)?",
                "Are there any latency requirements?",
                "Should we prioritize availability or consistency (CAP theorem)?"
            ]
        },
        {
            "phase": "2. High-Level Design",
            "time": "10-15 minutes",
            "goal": "Establish the overall architecture and major components",
            "activities": [
                "Draw a system diagram with major components",
                "Identify client, load balancers, application servers, databases, caches",
                "Show data flow for core operations",
                "Explain component interactions at a high level",
                "Call out key technology choices (SQL vs NoSQL, cache strategy)"
            ],
            "common_mistakes": [
                "Diving too deep into implementation details",
                "Creating overly complex architectures",
                "Not explaining the reasoning behind choices"
            ],
            "tips": [
                "Start simple, add complexity only when needed",
                "Explain trade-offs for major decisions",
                "Use standard components (load balancer, cache, queue)",
                "Keep the diagram clean and readable"
            ]
        },
        {
            "phase": "3. Deep Dives",
            "time": "15-20 minutes",
            "goal": "Demonstrate depth in critical areas and handle edge cases",
            "areas": [
                {
                    "topic": "Database Schema & Indexing",
                    "questions": [
                        "What does the schema look like?",
                        "What indexes do we need for query performance?",
                        "How do we partition/shard the data?"
                    ]
                },
                {
                    "topic": "Scaling Strategies",
                    "questions": [
                        "How do we scale reads (caching, read replicas, CDN)?",
                        "How do we scale writes (sharding, async processing)?",
                        "What are the bottlenecks and how do we address them?"
                    ]
                },
                {
                    "topic": "Caching Strategy",
                    "questions": [
                        "What do we cache and for how long?",
                        "How do we invalidate stale cache?",
                        "What's the expected cache hit ratio?"
                    ]
                },
                {
                    "topic": "Failure Modes & Resilience",
                    "questions": [
                        "What happens if the database fails?",
                        "How do we handle network partitions?",
                        "What's the disaster recovery strategy?"
                    ]
                }
            ],
            "common_mistakes": [
                "Trying to cover everything instead of focusing on 2-3 critical areas",
                "Not responding to interviewer's cues about what to explore",
                "Ignoring edge cases and failure scenarios"
            ],
            "tips": [
                "Follow the interviewer's lead on what to dive into",
                "Show depth in a few areas rather than breadth across all",
                "Discuss trade-offs explicitly"
            ]
        },
        {
            "phase": "4. Wrap-Up & Discussion",
            "time": "5 minutes",
            "goal": "Summarize, discuss alternatives, and handle final questions",
            "activities": [
                "Recap the design and key decisions",
                "Discuss alternative approaches and their trade-offs",
                "Address any remaining concerns or edge cases",
                "Answer interviewer's questions"
            ],
            "reflection_questions": [
                "What would you do differently at 10x scale?",
                "What are the main failure points in this design?",
                "How would you evolve this system over time?"
            ]
        }
    ],
    "best_practices": [
        "Always start with requirements - never skip this step",
        "Draw diagrams - visual communication is key",
        "Think out loud - show your thought process",
        "Discuss trade-offs for every major decision",
        "Ask clarifying questions when stuck",
        "Stay organized and maintain a clear structure",
        "Be honest if you don't know something",
        "Collaborate with the interviewer, don't work against them"
    ]
}

ASSESSMENT_RUBRIC = {
    "overview": "Understanding how interviewers evaluate candidates can help you focus your preparation and performance.",
    "competencies": [
        {
            "name": "Problem Navigation",
            "weight": "30%",
            "description": "Your ability to break down ambiguous problems and prioritize the right pieces",
            "levels": {
                "strong": [
                    "Asks excellent clarifying questions to narrow scope",
                    "Identifies and focuses on the most critical aspects",
                    "Navigates uncertainty with structure and confidence",
                    "Delivers a working design that meets all requirements"
                ],
                "adequate": [
                    "Asks some clarifying questions",
                    "Eventually identifies important aspects",
                    "Completes a basic working design",
                    "May need prompting to explore critical areas"
                ],
                "weak": [
                    "Jumps to solutions without understanding requirements",
                    "Focuses on trivial or unimportant aspects",
                    "Gets stuck and cannot make progress",
                    "Fails to deliver a complete solution"
                ]
            },
            "how_to_improve": [
                "Practice the Delivery Framework structure",
                "Study common interview scenarios to recognize patterns",
                "Learn to distinguish critical vs. nice-to-have features"
            ]
        },
        {
            "name": "Solution Design",
            "weight": "30%",
            "description": "Your ability to architect scalable, performant systems",
            "levels": {
                "strong": [
                    "Designs are well-structured and easy to understand",
                    "Appropriately considers scaling and performance",
                    "Components are logically separated with clear responsibilities",
                    "Handles edge cases and failure scenarios"
                ],
                "adequate": [
                    "Design mostly works but may have gaps",
                    "Basic understanding of scaling principles",
                    "Some consideration of edge cases",
                    "May overlook some failure modes"
                ],
                "weak": [
                    "Design is confusing or disorganized ('spaghetti')",
                    "Ignores scaling concerns",
                    "Major gaps in functionality",
                    "Doesn't consider failures"
                ]
            },
            "how_to_improve": [
                "Master core concepts (caching, sharding, replication)",
                "Study real system architectures (tech blogs)",
                "Practice diagramming and explaining designs clearly"
            ]
        },
        {
            "name": "Technical Excellence",
            "weight": "25%",
            "description": "Your knowledge of technologies, patterns, and best practices",
            "levels": {
                "strong": [
                    "Demonstrates strong knowledge of current technologies",
                    "Uses appropriate tools for each problem",
                    "Recognizes and applies common patterns",
                    "Understands trade-offs between different approaches"
                ],
                "adequate": [
                    "Basic knowledge of common technologies",
                    "Can explain when to use SQL vs NoSQL",
                    "Aware of standard patterns like caching, queues",
                    "May lack depth in specific areas"
                ],
                "weak": [
                    "Limited knowledge of available technologies",
                    "Uses outdated approaches (2015-era thinking)",
                    "Cannot explain technology choices",
                    "Misses obvious patterns"
                ]
            },
            "how_to_improve": [
                "Study key technologies (Redis, Kafka, PostgreSQL, S3)",
                "Learn common patterns (real-time updates, handling contention)",
                "Read about modern hardware constraints (current numbers)"
            ]
        },
        {
            "name": "Communication & Collaboration",
            "weight": "15%",
            "description": "How well you work with the interviewer and explain your thinking",
            "levels": {
                "strong": [
                    "Communicates complex concepts clearly",
                    "Responds well to feedback and suggestions",
                    "Collaborates effectively with the interviewer",
                    "Thinks out loud to show reasoning"
                ],
                "adequate": [
                    "Generally communicates clearly",
                    "Accepts feedback without being defensive",
                    "Mostly collaborative",
                    "May need prompting to explain thinking"
                ],
                "weak": [
                    "Struggles to explain concepts clearly",
                    "Defensive or argumentative with feedback",
                    "Works in isolation instead of collaborating",
                    "Doesn't explain reasoning"
                ]
            },
            "how_to_improve": [
                "Practice explaining designs to friends/peers",
                "Record yourself doing mock interviews",
                "Learn to accept feedback gracefully",
                "Think out loud during practice sessions"
            ]
        }
    ],
    "level_expectations": {
        "mid_level": {
            "expectations": [
                "Complete basic design covering main requirements",
                "Demonstrate understanding of fundamental concepts",
                "May lack depth in advanced areas like sharding or multi-region",
                "Should handle standard scaling scenarios"
            ]
        },
        "senior": {
            "expectations": [
                "Complete design with depth in critical areas",
                "Strong understanding of trade-offs and alternatives",
                "Handle complex scaling scenarios confidently",
                "Proactively identify and address failure modes",
                "Leave time for multiple deep dives"
            ]
        },
        "staff_plus": {
            "expectations": [
                "Everything from senior level",
                "Demonstrate organizational impact thinking",
                "Discuss evolution and migration strategies",
                "Consider team structure and operational concerns",
                "Handle ambiguity with ease and explore multiple solutions"
            ]
        }
    },
    "red_flags": [
        "Memorized answers without understanding (probing reveals gaps)",
        "Cannot explain trade-offs",
        "Defensive when questioned",
        "Ignores interviewer feedback",
        "Over-engineers simple problems",
        "Uses buzzwords without depth"
    ],
    "green_flags": [
        "Asks excellent clarifying questions",
        "Discusses multiple approaches with trade-offs",
        "Adapts design based on requirements",
        "Demonstrates curiosity and learning mindset",
        "Collaborates naturally with interviewer",
        "Shows practical experience with real systems"
    ]
}

COMMON_PATTERNS = {
    "real_time_updates": {
        "title": "Real-Time Updates",
        "problem": "How to push updates to clients immediately when data changes",
        "use_cases": [
            "Chat applications (new messages)",
            "Live dashboards (metrics updates)",
            "Collaborative editing (Google Docs)",
            "Live sports scores",
            "Stock price tickers"
        ],
        "approaches": [
            {
                "name": "WebSockets",
                "description": "Persistent bidirectional connection between client and server",
                "pros": [
                    "True real-time (sub-100ms latency)",
                    "Bidirectional communication",
                    "Low overhead for frequent updates"
                ],
                "cons": [
                    "Stateful connections complicate scaling",
                    "Requires load balancer support for WebSockets",
                    "Connections can drop and need reconnection logic"
                ],
                "when_to_use": "High-frequency updates (chat, gaming, collaborative editing)",
                "technologies": ["Socket.IO", "AWS API Gateway WebSocket API", "Redis Pub/Sub for cross-node routing"]
            },
            {
                "name": "Server-Sent Events (SSE)",
                "description": "Server pushes updates to client over persistent HTTP connection",
                "pros": [
                    "Simpler than WebSockets (one-way, server to client)",
                    "Works over HTTP (easier with proxies/firewalls)",
                    "Auto-reconnection built into browser API"
                ],
                "cons": [
                    "One-way only (client can't send via same connection)",
                    "Limited browser connection limits (6 per domain)",
                    "Not as widely supported as WebSockets"
                ],
                "when_to_use": "Server-to-client only updates (notifications, live feeds)",
                "technologies": ["EventSource API", "Nginx for SSE", "Kafka for event streaming"]
            },
            {
                "name": "Long Polling",
                "description": "Client sends request, server holds it open until data is available",
                "pros": [
                    "Works everywhere (standard HTTP)",
                    "No special server requirements",
                    "Easy to implement"
                ],
                "cons": [
                    "Higher latency than WebSockets (HTTP overhead)",
                    "More server resources (holding connections)",
                    "Not truly real-time"
                ],
                "when_to_use": "Fallback when WebSockets unavailable, low-frequency updates",
                "technologies": ["Standard HTTP", "nginx", "Any web framework"]
            },
            {
                "name": "Short Polling",
                "description": "Client repeatedly sends requests at fixed intervals",
                "pros": [
                    "Dead simple to implement",
                    "Works everywhere",
                    "Stateless"
                ],
                "cons": [
                    "Wastes bandwidth (constant requests)",
                    "High latency (depends on polling interval)",
                    "Scales poorly"
                ],
                "when_to_use": "Only as a last resort or for very low-frequency updates",
                "technologies": ["Standard HTTP", "JavaScript setTimeout/setInterval"]
            }
        ],
        "scaling_considerations": [
            "Use Redis Pub/Sub for cross-node message routing with WebSockets",
            "Implement heartbeats and reconnection logic",
            "Consider connection draining for graceful deployments",
            "Use load balancers with sticky sessions or pub/sub"
        ]
    },
    "dealing_with_contention": {
        "title": "Dealing with Contention",
        "problem": "How to handle multiple users/processes trying to modify the same resource simultaneously",
        "use_cases": [
            "Ticketmaster (limited inventory)",
            "E-commerce (last item in stock)",
            "Banking (account balance updates)",
            "Collaborative editing (same document)",
            "Ride-sharing (driver assignment)"
        ],
        "approaches": [
            {
                "name": "Optimistic Locking",
                "description": "Assume no conflicts, detect them at commit time using version numbers",
                "pros": [
                    "High throughput when conflicts are rare",
                    "No locks held during reads",
                    "Simple to implement"
                ],
                "cons": [
                    "User experience: need to retry on conflict",
                    "Not suitable for high-contention scenarios",
                    "Can lead to starvation if retries keep failing"
                ],
                "when_to_use": "Low to medium contention scenarios",
                "implementation": "Add 'version' column, check version hasn't changed before update",
                "example_sql": "UPDATE tickets SET sold=true WHERE id=123 AND version=5; UPDATE version to 6"
            },
            {
                "name": "Pessimistic Locking",
                "description": "Acquire lock before modifying, hold until commit",
                "pros": [
                    "Guaranteed to succeed once lock is acquired",
                    "No retry logic needed",
                    "Suitable for high-contention scenarios"
                ],
                "cons": [
                    "Lower throughput (locks block other operations)",
                    "Risk of deadlocks",
                    "Can hurt performance at scale"
                ],
                "when_to_use": "High contention, critical operations (payments, inventory)",
                "implementation": "SELECT ... FOR UPDATE in SQL, distributed locks in Redis",
                "example_sql": "BEGIN; SELECT * FROM tickets WHERE id=123 FOR UPDATE; UPDATE tickets SET sold=true WHERE id=123; COMMIT;"
            },
            {
                "name": "Distributed Locks",
                "description": "Use external coordination service to acquire locks across multiple nodes",
                "pros": [
                    "Works across distributed systems",
                    "Prevents race conditions in microservices",
                    "Can set TTL to prevent deadlocks"
                ],
                "cons": [
                    "Added complexity and latency",
                    "Single point of failure (the lock service)",
                    "Lock contention becomes bottleneck"
                ],
                "when_to_use": "Microservices need coordination, distributed systems",
                "technologies": ["Redis SETNX", "ZooKeeper", "etcd", "Redlock algorithm"]
            },
            {
                "name": "Queue-Based Serialization",
                "description": "Serialize all writes through a queue processed by a single consumer",
                "pros": [
                    "No conflicts possible (single writer)",
                    "Durable (queue persists requests)",
                    "Can handle traffic spikes"
                ],
                "cons": [
                    "Added latency (async processing)",
                    "Single consumer is bottleneck",
                    "More complex architecture"
                ],
                "when_to_use": "Write-heavy systems, can tolerate async processing",
                "technologies": ["SQS", "Kafka", "RabbitMQ", "Lambda consumers"]
            }
        ],
        "ticketmaster_example": "Use pessimistic locking or Redis distributed lock when user clicks 'Reserve'. Lock the seat for 10 minutes while payment processes. Release lock on successful payment or timeout."
    },
    "multi_step_processes": {
        "title": "Multi-Step Processes",
        "problem": "How to handle operations that span multiple services or databases while maintaining consistency",
        "use_cases": [
            "E-commerce checkout (inventory, payment, shipping)",
            "Hotel booking (reservation, payment, confirmation)",
            "Order fulfillment (order, payment, inventory, shipping)",
            "Account transfers (debit one account, credit another)"
        ],
        "approaches": [
            {
                "name": "Saga Pattern",
                "description": "Break transaction into local transactions with compensating actions for rollback",
                "pros": [
                    "Works across distributed systems",
                    "No distributed transactions needed",
                    "Each service maintains its own database"
                ],
                "cons": [
                    "Eventual consistency",
                    "Complex compensation logic",
                    "Partial failures visible to users"
                ],
                "types": [
                    {
                        "variant": "Choreography",
                        "description": "Each service listens to events and triggers next step",
                        "pros": ["Decoupled", "No orchestrator needed"],
                        "cons": ["Hard to track progress", "Circular dependencies possible"]
                    },
                    {
                        "variant": "Orchestration",
                        "description": "Central orchestrator coordinates all steps",
                        "pros": ["Clear flow", "Easy to track", "Centralized error handling"],
                        "cons": ["Orchestrator is single point of failure", "Orchestrator can become complex"]
                    }
                ],
                "when_to_use": "Distributed systems, microservices architecture",
                "technologies": ["AWS Step Functions", "Temporal", "Apache Camel"]
            },
            {
                "name": "Two-Phase Commit (2PC)",
                "description": "Coordinator asks all participants to prepare, then commit if all succeed",
                "pros": [
                    "Strong consistency guarantees",
                    "All-or-nothing atomicity",
                    "No partial state visible"
                ],
                "cons": [
                    "Blocking protocol (low throughput)",
                    "Coordinator is single point of failure",
                    "High latency"
                ],
                "when_to_use": "Rarely - only when strong consistency absolutely required",
                "note": "Avoid 2PC in interviews unless explicitly asked. Mention it, then propose better alternatives."
            },
            {
                "name": "Outbox Pattern",
                "description": "Write to database and outbox table in same transaction, separate process publishes events",
                "pros": [
                    "Ensures events are published exactly once",
                    "No dual-write problem",
                    "Uses local transactions"
                ],
                "cons": [
                    "Added complexity",
                    "Slight delay in event publishing",
                    "Requires change data capture or polling"
                ],
                "when_to_use": "Need to guarantee event publishing after database write",
                "technologies": ["DynamoDB Streams", "PostgreSQL + Debezium", "Transactional outbox table"]
            }
        ],
        "example_flow": {
            "scenario": "E-commerce checkout with Saga (Orchestration)",
            "steps": [
                "1. Orchestrator starts: CreateOrder",
                "2. OrderService: Reserve inventory (local transaction)",
                "3. PaymentService: Process payment (local transaction)",
                "4. ShippingService: Create shipment (local transaction)",
                "5. If any step fails: Orchestrator triggers compensations in reverse order",
                "   - Cancel shipment -> Refund payment -> Release inventory"
            ]
        }
    },
    "scaling_reads": {
        "title": "Scaling Reads",
        "problem": "How to handle massive read traffic without overwhelming your database",
        "use_cases": [
            "Social media feeds",
            "Product catalogs",
            "Content sites",
            "Search results"
        ],
        "strategies": [
            {
                "name": "Caching Layer (Redis/Memcached)",
                "description": "Store frequently accessed data in memory",
                "latency_improvement": "100x (100ms DB query -> 1ms cache hit)",
                "when_to_use": "Read-heavy workloads (100:1 read-to-write ratio or higher)",
                "cache_patterns": ["Cache-aside", "Write-through", "Write-behind"],
                "considerations": ["Cache invalidation strategy", "TTL selection", "Cache warming"]
            },
            {
                "name": "Read Replicas",
                "description": "Route read queries to replica databases",
                "latency_improvement": "Reduces primary DB load, maintains query latency",
                "when_to_use": "Read-heavy, can tolerate replication lag (eventual consistency)",
                "considerations": ["Replication lag (typically <1s)", "Read-your-own-writes issues", "Failover strategy"]
            },
            {
                "name": "CDN (CloudFront, Cloudflare)",
                "description": "Cache static assets and responses at edge locations",
                "latency_improvement": "10x (500ms origin -> 50ms edge)",
                "when_to_use": "Static content, geographically distributed users",
                "cache_keys": ["URL path", "Query params", "Headers (auth, region)"],
                "considerations": ["Cache-Control headers", "Purge/invalidation", "Geo-targeting"]
            },
            {
                "name": "Materialized Views / Denormalization",
                "description": "Pre-compute and store query results",
                "latency_improvement": "100x (complex joins -> single table scan)",
                "when_to_use": "Complex aggregations, repeated expensive queries",
                "tradeoffs": ["Write amplification", "Storage overhead", "Stale data"]
            },
            {
                "name": "Database Indexing",
                "description": "Create indexes on frequently queried columns",
                "latency_improvement": "10-100x (full table scan -> index seek)",
                "when_to_use": "Always for foreign keys, WHERE clauses, JOIN conditions",
                "considerations": ["Write overhead", "Storage cost", "Covering indexes"]
            }
        ],
        "layered_approach": {
            "description": "Combine multiple strategies for maximum effectiveness",
            "layers": [
                "1. CDN (edge cache) - 90% of requests",
                "2. Application cache (Redis) - 9% of requests",
                "3. Database read replicas - 1% of requests",
                "4. Primary database - writes only"
            ],
            "result": "99%+ of reads never touch primary database"
        }
    },
    "scaling_writes": {
        "title": "Scaling Writes",
        "problem": "How to handle high write throughput without bottlenecking on a single database",
        "use_cases": [
            "Analytics ingestion",
            "IoT sensor data",
            "Logging systems",
            "Chat messages",
            "Location updates"
        ],
        "strategies": [
            {
                "name": "Database Sharding",
                "description": "Partition data across multiple database instances",
                "throughput_improvement": "Linear scaling (2 shards = 2x writes)",
                "sharding_keys": ["User ID", "Tenant ID", "Geographic region", "Time range"],
                "challenges": ["Cross-shard queries", "Rebalancing", "Hot shards"],
                "when_to_use": "Single DB maxed out (>10K writes/sec)"
            },
            {
                "name": "Write-Ahead Log (WAL)",
                "description": "Append writes to log before applying to database",
                "throughput_improvement": "5-10x (sequential writes vs random)",
                "when_to_use": "High-throughput writes, need durability",
                "technologies": ["Kafka", "Kinesis", "Database WAL (PostgreSQL, MySQL)"]
            },
            {
                "name": "Async Processing with Queues",
                "description": "Accept writes to queue, process in background",
                "throughput_improvement": "Unlimited (queue absorbs spikes)",
                "when_to_use": "Can tolerate eventual consistency, traffic spikes",
                "technologies": ["SQS", "RabbitMQ", "Kafka", "Kinesis"],
                "considerations": ["At-least-once delivery", "Ordering guarantees", "Dead letter queues"]
            },
            {
                "name": "Batch Writes",
                "description": "Group multiple writes into single database transaction",
                "throughput_improvement": "10-50x (reduces transaction overhead)",
                "when_to_use": "High-volume inserts (analytics, logs)",
                "example": "Batch 1000 log entries into single INSERT"
            },
            {
                "name": "Time-Series Optimization",
                "description": "Use time-series databases optimized for append-only writes",
                "throughput_improvement": "100x over traditional RDBMS",
                "when_to_use": "Time-stamped data (metrics, logs, events)",
                "technologies": ["InfluxDB", "TimescaleDB", "Amazon Timestream"]
            }
        ],
        "example_architecture": {
            "scenario": "IoT sensor data (1M devices, 1 write/sec each = 1M writes/sec)",
            "design": [
                "1. Devices write to Kinesis Data Streams (partitioned by deviceId)",
                "2. Lambda consumers batch process 1000 records at a time",
                "3. Write to TimescaleDB sharded by time range (monthly)",
                "4. Cold data archived to S3 after 90 days"
            ],
            "result": "Handles 1M writes/sec with <1s latency"
        }
    },
    "handling_large_blobs": {
        "title": "Handling Large Blobs (Files, Videos, Images)",
        "problem": "How to upload, store, and serve large files efficiently",
        "use_cases": [
            "Dropbox-like file storage",
            "YouTube video uploads",
            "Image sharing (Instagram)",
            "Document management"
        ],
        "strategies": [
            {
                "name": "Direct Upload to S3 (Presigned URLs)",
                "description": "Client uploads directly to S3, bypassing application servers",
                "benefits": [
                    "No double network hop",
                    "Application servers don't handle large files",
                    "S3 scales infinitely"
                ],
                "flow": [
                    "1. Client requests presigned URL from API",
                    "2. API generates presigned URL (valid 5-15min)",
                    "3. Client uploads directly to S3 using presigned URL",
                    "4. Client notifies API of completion",
                    "5. API stores metadata in database"
                ],
                "when_to_use": "Always for large files (>5MB)"
            },
            {
                "name": "Multipart Upload",
                "description": "Split large files into chunks, upload in parallel",
                "benefits": [
                    "Resumable uploads (retry only failed chunks)",
                    "Parallel transfers (saturate bandwidth)",
                    "Progress indicators"
                ],
                "chunk_size": "5-10 MB per chunk",
                "when_to_use": "Files >100 MB",
                "technologies": ["S3 Multipart Upload API", "Resumable upload protocols"]
            },
            {
                "name": "CDN for Downloads",
                "description": "Serve files from edge locations close to users",
                "benefits": [
                    "10x faster downloads (edge vs origin)",
                    "Reduced origin load",
                    "Better user experience globally"
                ],
                "when_to_use": "Public files, high download volume",
                "technologies": ["CloudFront", "Cloudflare", "Akamai"]
            },
            {
                "name": "Compression & Optimization",
                "description": "Compress files before storage/transfer",
                "benefits": [
                    "3-10x storage savings (text, logs)",
                    "Faster transfers",
                    "Lower bandwidth costs"
                ],
                "considerations": [
                    "Compress text files, not already-compressed formats (images, video)",
                    "Client-side compression before upload",
                    "Serve compressed versions (gzip, br)"
                ]
            },
            {
                "name": "Chunking for Streaming",
                "description": "Split video into chunks for adaptive bitrate streaming",
                "benefits": [
                    "Start playback before full download",
                    "Adaptive quality based on bandwidth",
                    "Seek without downloading entire file"
                ],
                "when_to_use": "Video streaming",
                "technologies": ["HLS (HTTP Live Streaming)", "DASH", "AWS MediaConvert"]
            }
        ],
        "example_design": {
            "scenario": "Video upload platform (YouTube-like)",
            "flow": [
                "1. Client chunks 1GB video into 100x 10MB chunks",
                "2. Client requests presigned URLs for all chunks",
                "3. Client uploads chunks in parallel to S3",
                "4. S3 triggers Lambda on upload completion",
                "5. Lambda starts transcoding job (MediaConvert)",
                "6. Transcoded videos stored in S3, served via CloudFront CDN",
                "7. Metadata (title, description, thumbnail) in DynamoDB"
            ]
        }
    },
    "managing_long_running_tasks": {
        "title": "Managing Long-Running Tasks",
        "problem": "How to handle operations that take minutes or hours without blocking requests",
        "use_cases": [
            "Video transcoding",
            "Data exports (CSV, PDF)",
            "Batch processing",
            "Machine learning training",
            "Database migrations"
        ],
        "strategies": [
            {
                "name": "Async Job Queue",
                "description": "Accept request immediately, process in background worker",
                "flow": [
                    "1. API accepts request, creates Job record (status=pending)",
                    "2. API publishes job to queue (SQS, Kafka)",
                    "3. API returns jobId to client immediately",
                    "4. Worker polls queue, processes job",
                    "5. Worker updates Job status (processing, completed, failed)",
                    "6. Client polls GET /jobs/{jobId} for status"
                ],
                "when_to_use": "Tasks taking >5 seconds",
                "technologies": ["SQS + Lambda", "Celery (Python)", "Sidekiq (Ruby)", "BullMQ (Node.js)"]
            },
            {
                "name": "Workflow Orchestration",
                "description": "Coordinate multi-step long-running processes with retries and error handling",
                "benefits": [
                    "Visual workflow tracking",
                    "Automatic retries",
                    "Timeouts and error handling",
                    "Resumable on failure"
                ],
                "when_to_use": "Complex multi-step processes",
                "technologies": ["AWS Step Functions", "Temporal", "Apache Airflow"]
            },
            {
                "name": "Status Tracking & Notifications",
                "description": "Keep users informed of progress",
                "methods": [
                    {
                        "approach": "Polling",
                        "description": "Client repeatedly checks job status",
                        "pros": ["Simple", "Works everywhere"],
                        "cons": ["Wastes bandwidth", "Higher latency"]
                    },
                    {
                        "approach": "WebSocket / SSE",
                        "description": "Server pushes status updates to client",
                        "pros": ["Real-time", "Efficient"],
                        "cons": ["Requires persistent connection"]
                    },
                    {
                        "approach": "Webhook / Email",
                        "description": "Notify user when complete",
                        "pros": ["No client waiting", "Works for hours-long jobs"],
                        "cons": ["Requires user-provided callback URL or email"]
                    }
                ]
            },
            {
                "name": "Progress Tracking",
                "description": "Show % complete to user",
                "implementation": [
                    "Worker periodically updates Job.progress field (0-100%)",
                    "Client polls progress or receives updates via WebSocket",
                    "Show progress bar in UI"
                ],
                "example": "Video transcoding: track % of frames processed"
            }
        ],
        "example_design": {
            "scenario": "Data export system (generate 100MB CSV from database)",
            "flow": [
                "1. User clicks 'Export' button",
                "2. API creates Export job (status=pending), returns jobId",
                "3. API publishes job to SQS queue",
                "4. Lambda worker picks up job from queue",
                "5. Worker streams database results to S3 in chunks",
                "6. Worker updates job status to 'completed', stores S3 URL",
                "7. Client polls GET /exports/{jobId}, receives download URL when ready",
                "8. User downloads file from S3 via presigned URL"
            ],
            "latency": "Request returns in <100ms, export completes in 30-60 seconds"
        }
    }
}
