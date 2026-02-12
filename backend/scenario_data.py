SCENARIO_BLUEPRINTS = {
    "payments": {
        "title": "Payment Processing System",
        "description": "A payment processing platform that handles credit/debit card transactions, manages refunds, and provides transaction history. Think Stripe or Square.",
        "requirements": {
            "functional": [
                "Process credit card and debit card payments",
                "Support refunds and partial refunds",
                "Provide transaction history per user",
                "Support idempotent payment requests to prevent double charges",
                "Webhook notifications for payment status changes",
                "Support multiple payment methods per user"
            ],
            "non_functional": [
                "Strong consistency for financial transactions",
                "PCI-DSS compliance for card data handling",
                "99.99% availability for payment processing",
                "Sub-second latency for payment authorization",
                "Exactly-once processing semantics",
                "Complete audit trail for all transactions"
            ],
            "out_of_scope": [
                "Cryptocurrency payments",
                "Cross-border currency conversion",
                "Subscription / recurring billing logic",
                "Dispute resolution workflow"
            ]
        },
        "core_entities": [
            {
                "name": "User",
                "fields": ["id (PK)", "email", "name", "createdAt"]
            },
            {
                "name": "PaymentMethod",
                "fields": ["id (PK)", "userId (index)", "type", "last4", "expiryMonth", "expiryYear", "isDefault", "tokenRef"]
            },
            {
                "name": "Transaction",
                "fields": ["id (PK)", "userId (index)", "amount", "currency", "status: pending|authorized|captured|failed|refunded", "paymentMethodId", "idempotencyKey (unique index)", "createdAt", "updatedAt"]
            },
            {
                "name": "Refund",
                "fields": ["id (PK)", "transactionId (index)", "amount", "reason", "status: pending|completed|failed", "createdAt"]
            },
            {
                "name": "AuditLog",
                "fields": ["id (PK)", "transactionId (index)", "action", "actor", "metadata (JSON)", "timestamp"]
            }
        ],
        "api": [
            {
                "method": "POST",
                "path": "/payments",
                "description": "Initiate a payment",
                "auth": "JWT token",
                "request_body": "{ amount, currency, paymentMethodId, idempotencyKey }",
                "response": "Transaction"
            },
            {
                "method": "POST",
                "path": "/payments/{id}/capture",
                "description": "Capture an authorized payment",
                "auth": "JWT token",
                "request_body": "{ amount? }",
                "response": "Transaction"
            },
            {
                "method": "POST",
                "path": "/payments/{id}/refund",
                "description": "Refund a captured payment",
                "auth": "JWT token",
                "request_body": "{ amount?, reason }",
                "response": "Refund"
            },
            {
                "method": "GET",
                "path": "/payments",
                "description": "List user transactions with pagination",
                "auth": "JWT token",
                "request_body": None,
                "response": "{ data: Transaction[], cursor, hasMore }"
            },
            {
                "method": "GET",
                "path": "/payments/{id}",
                "description": "Get transaction details",
                "auth": "JWT token",
                "request_body": None,
                "response": "Transaction"
            }
        ],
        "high_level": {
            "description": "Client communicates through an API Gateway that handles rate limiting, authentication, and routing. A Load Balancer distributes traffic to the Payment Service, which orchestrates the payment flow. The Payment Service talks to a Card Processor (Stripe/Adyen) for authorization, writes to PostgreSQL (primary + read replicas) for transaction records, and publishes events to SQS for async processing like webhooks and reconciliation. Redis stores idempotency keys and caches frequently accessed data.",
            "components": [
                "API Gateway - rate limiting, authentication, routing",
                "Load Balancer - distributes traffic across service instances",
                "Payment Service - orchestrates payment flow, validates requests",
                "Card Processor (external) - Stripe/Adyen for card authorization",
                "PostgreSQL (Replicated) - transaction records, ACID compliance",
                "Redis - idempotency key store, session cache",
                "SQS - async event processing for webhooks and reconciliation",
                "Webhook Service - delivers payment status notifications to merchants"
            ],
            "notes": [
                "Write-heavy for transactions, read-heavy for history",
                "Idempotency keys stored in Redis with TTL (24h) to prevent double charges",
                "Two-phase commit pattern: authorize then capture",
                "All state changes produce audit log entries"
            ]
        },
        "deep_dive": {
            "flows": [
                {
                    "name": "Payment Processing Flow",
                    "steps": [
                        "Client sends POST /payments with idempotencyKey",
                        "API Gateway authenticates, rate-limits, routes to Payment Service",
                        "Payment Service checks Redis for existing idempotencyKey",
                        "If key exists, return cached response (idempotent replay)",
                        "If new, validate payment method and amount",
                        "Create Transaction record with status=pending in PostgreSQL",
                        "Send authorization request to Card Processor",
                        "On success: update Transaction status=authorized, store result in Redis under idempotencyKey",
                        "Publish PaymentAuthorized event to SQS",
                        "Return Transaction to client"
                    ]
                },
                {
                    "name": "Refund Flow",
                    "steps": [
                        "Client sends POST /payments/{id}/refund",
                        "Payment Service loads Transaction, validates status=captured",
                        "Creates Refund record with status=pending",
                        "Sends refund request to Card Processor",
                        "On success: update Refund status=completed, Transaction status=refunded",
                        "Publish RefundCompleted event to SQS",
                        "Webhook Service notifies merchant"
                    ]
                }
            ],
            "caching": "Redis stores idempotency keys with 24h TTL. Frequently accessed transaction lookups cached with short TTL (60s). Read replicas handle GET /payments list queries to reduce primary DB load.",
            "scaling": "Payment Service scales horizontally behind the load balancer. PostgreSQL uses read replicas for transaction history queries. SQS decouples webhook delivery so payment latency is not affected by downstream consumers. Redis cluster for high-throughput idempotency checks.",
            "notes": [
                "Use distributed locks (Redis SETNX) to prevent race conditions on concurrent payment requests with same idempotencyKey",
                "Card tokenization happens client-side (Stripe Elements / Adyen Drop-in) so raw card numbers never touch our servers",
                "Dead letter queue for failed webhook deliveries with exponential backoff retry",
                "Daily reconciliation job compares our records against Card Processor settlement reports"
            ]
        },
        "tools": ["Amazon DynamoDB", "Amazon RDS for PostgreSQL", "Amazon SQS (Standard)", "AWS Lambda", "Amazon ElastiCache (Redis/Valkey)"],
        "reasoning": "Strong consistency for transactions, async processing for reconciliation, caching for fraud checks"
    },

    "chat": {
        "title": "Real-Time Chat Application",
        "description": "A real-time messaging platform supporting 1:1 and group conversations with message history, read receipts, and online presence. Think Slack or WhatsApp.",
        "requirements": {
            "functional": [
                "Send and receive messages in real time (1:1 and group)",
                "Persist message history with pagination",
                "Show online/offline presence indicators",
                "Support read receipts and typing indicators",
                "Push notifications for offline users",
                "Support media attachments (images, files)"
            ],
            "non_functional": [
                "Sub-100ms message delivery latency",
                "High availability over strict consistency",
                "Messages should be eventually consistent (delivered at least once)",
                "Support 100K+ concurrent WebSocket connections per node",
                "Message ordering guaranteed within a conversation",
                "Graceful handling of network partitions"
            ],
            "out_of_scope": [
                "End-to-end encryption",
                "Voice/video calling",
                "Message search across all conversations",
                "Bot framework / integrations"
            ]
        },
        "core_entities": [
            {
                "name": "User",
                "fields": ["id (PK)", "username", "email", "avatarUrl", "lastSeenAt"]
            },
            {
                "name": "Conversation",
                "fields": ["id (PK)", "type: direct|group", "name?", "createdAt", "updatedAt"]
            },
            {
                "name": "ConversationMember",
                "fields": ["conversationId (PK)", "userId (PK)", "joinedAt", "lastReadMessageId"]
            },
            {
                "name": "Message",
                "fields": ["id (PK)", "conversationId (partition key)", "senderId", "body", "mediaUrl?", "createdAt (sort key)", "status: sent|delivered|read"]
            }
        ],
        "api": [
            {
                "method": "POST",
                "path": "/conversations",
                "description": "Create a new conversation (1:1 or group)",
                "auth": "JWT token",
                "request_body": "{ participantIds, name?, type }",
                "response": "Conversation"
            },
            {
                "method": "POST",
                "path": "/conversations/{id}/messages",
                "description": "Send a message (also broadcast via WebSocket)",
                "auth": "JWT token",
                "request_body": "{ body, mediaUrl? }",
                "response": "Message"
            },
            {
                "method": "GET",
                "path": "/conversations/{id}/messages",
                "description": "Fetch message history with cursor pagination",
                "auth": "JWT token",
                "request_body": None,
                "response": "{ data: Message[], cursor, hasMore }"
            },
            {
                "method": "PUT",
                "path": "/conversations/{id}/read",
                "description": "Mark conversation as read up to a message",
                "auth": "JWT token",
                "request_body": "{ lastReadMessageId }",
                "response": "200 OK"
            },
            {
                "method": "WS",
                "path": "/ws",
                "description": "WebSocket connection for real-time events (messages, typing, presence)",
                "auth": "JWT token (query param or first frame)",
                "request_body": None,
                "response": "Bidirectional stream"
            }
        ],
        "high_level": {
            "description": "Clients connect via WebSocket through an API Gateway / Load Balancer. A Chat Service manages WebSocket connections and message routing. When a user sends a message, the Chat Service writes it to DynamoDB (partitioned by conversationId, sorted by timestamp), publishes to a Kinesis stream for fan-out, and pushes to all online recipients via their WebSocket connections. Offline users get push notifications via SNS. Redis (ElastiCache) stores presence state and acts as a pub/sub layer for cross-node message routing. Media attachments go to S3 behind CloudFront.",
            "components": [
                "API Gateway / ALB - WebSocket upgrade, authentication, routing",
                "Chat Service (stateful) - manages WebSocket connections, routes messages",
                "DynamoDB - message storage, partitioned by conversationId",
                "Kinesis - real-time message fan-out stream",
                "ElastiCache (Redis) - presence tracking, pub/sub for cross-node delivery",
                "S3 + CloudFront - media attachment storage and CDN delivery",
                "SNS / Push Service - push notifications for offline users",
                "Lambda - async processors for notifications, read receipts"
            ],
            "notes": [
                "Very read-heavy: users scroll through history far more than they send messages",
                "WebSocket connections are stateful, so need sticky sessions or a pub/sub layer for cross-node routing",
                "DynamoDB single-table design: PK=conversationId, SK=timestamp for efficient range queries",
                "Fan-out on write: message goes to all online members immediately"
            ]
        },
        "deep_dive": {
            "flows": [
                {
                    "name": "Send Message Flow",
                    "steps": [
                        "Client sends message via WebSocket frame",
                        "Chat Service validates sender is member of conversation",
                        "Write message to DynamoDB with conversationId partition key",
                        "Publish message event to Redis pub/sub channel for this conversation",
                        "All Chat Service nodes subscribed to this channel receive the event",
                        "Each node pushes message to connected recipients via WebSocket",
                        "For offline members: publish to SNS for push notification",
                        "Publish to Kinesis for async processing (analytics, search indexing)"
                    ]
                },
                {
                    "name": "Presence Tracking",
                    "steps": [
                        "On WebSocket connect: set user presence key in Redis with TTL (30s)",
                        "Client sends heartbeat every 15s, refreshing the TTL",
                        "On WebSocket disconnect: let TTL expire (handles ungraceful disconnects)",
                        "Presence check: GET key from Redis, exists = online",
                        "Publish presence changes to relevant conversation channels"
                    ]
                }
            ],
            "caching": "ElastiCache (Redis) for presence state (SET with TTL), recent conversation list per user, and pub/sub for cross-node message delivery. DynamoDB DAX for hot conversation message reads.",
            "scaling": "Chat Service scales horizontally with Redis pub/sub handling cross-node message routing. DynamoDB auto-scales with on-demand capacity. Kinesis scales with shard splitting. Use connection draining on deploy to gracefully migrate WebSocket connections.",
            "notes": [
                "Redis pub/sub channel per conversation avoids broadcasting all messages to all nodes",
                "Use DynamoDB TTL for ephemeral data like typing indicators (auto-expire after 5s)",
                "Message ordering: DynamoDB sort key is timestamp + tiebreaker (messageId) to handle concurrent sends",
                "Connection state: maintain in-memory map of userId -> WebSocket on each Chat Service node"
            ]
        },
        "tools": ["Amazon DynamoDB", "Amazon ElastiCache (Redis/Valkey)", "Amazon Kinesis Data Streams", "AWS Lambda", "Amazon CloudFront"],
        "reasoning": "Low latency reads, real-time message delivery, global distribution"
    },

    "feed": {
        "title": "Social Media News Feed",
        "description": "A social media feed that aggregates posts from followed users, ranked by relevance and recency. Think Twitter/X home timeline or Instagram feed.",
        "requirements": {
            "functional": [
                "Users can create posts (text, images, video)",
                "Users can follow/unfollow other users",
                "Home feed shows posts from followed users, ranked by relevance",
                "Support likes, comments, and shares on posts",
                "Infinite scroll pagination for feed",
                "Real-time feed updates for new posts"
            ],
            "non_functional": [
                "Feed generation under 200ms latency",
                "High availability over strict consistency (eventual consistency OK)",
                "Support users following 1000s of accounts",
                "Support celebrity accounts with millions of followers",
                "Feed should feel fresh: new posts appear within seconds",
                "99.9% availability"
            ],
            "out_of_scope": [
                "Ad insertion and ranking",
                "Content moderation / spam detection",
                "Direct messaging",
                "Stories / ephemeral content"
            ]
        },
        "core_entities": [
            {
                "name": "User",
                "fields": ["id (PK)", "username", "displayName", "avatarUrl", "followerCount", "followingCount"]
            },
            {
                "name": "Follow",
                "fields": ["followerId (PK)", "followeeId (SK)", "createdAt"]
            },
            {
                "name": "Post",
                "fields": ["id (PK)", "authorId (index)", "content", "mediaUrls[]", "likeCount", "commentCount", "createdAt"]
            },
            {
                "name": "FeedItem",
                "fields": ["userId (PK)", "postId (SK)", "authorId", "score", "createdAt"]
            },
            {
                "name": "Like",
                "fields": ["userId (PK)", "postId (SK)", "createdAt"]
            }
        ],
        "api": [
            {
                "method": "POST",
                "path": "/posts",
                "description": "Create a new post",
                "auth": "JWT token",
                "request_body": "{ content, mediaUrls[]? }",
                "response": "Post"
            },
            {
                "method": "GET",
                "path": "/feed",
                "description": "Get personalized home feed with cursor pagination",
                "auth": "JWT token",
                "request_body": None,
                "response": "{ data: Post[], cursor, hasMore }"
            },
            {
                "method": "POST",
                "path": "/users/{id}/follow",
                "description": "Follow a user",
                "auth": "JWT token",
                "request_body": None,
                "response": "200 OK"
            },
            {
                "method": "DELETE",
                "path": "/users/{id}/follow",
                "description": "Unfollow a user",
                "auth": "JWT token",
                "request_body": None,
                "response": "200 OK"
            },
            {
                "method": "POST",
                "path": "/posts/{id}/like",
                "description": "Like a post",
                "auth": "JWT token",
                "request_body": None,
                "response": "200 OK"
            }
        ],
        "high_level": {
            "description": "Client communicates through an API Gateway. A Post Service handles CRUD for posts, storing them in DynamoDB. When a post is created, a Fan-Out Service reads the author's follower list and writes FeedItems to each follower's pre-computed feed in DynamoDB. For celebrity accounts (>100K followers), fan-out is skipped; instead, their posts are fetched at read-time and merged. ElastiCache (Redis) caches the top N feed items per user for fast reads. Media goes to S3 behind CloudFront CDN.",
            "components": [
                "API Gateway - authentication, rate limiting, routing",
                "Post Service - CRUD for posts, publish events",
                "Fan-Out Service (Lambda) - distributes posts to follower feeds",
                "Feed Service - reads and merges pre-computed feed with celebrity posts",
                "DynamoDB - posts table, feed table, follows table",
                "ElastiCache (Redis) - cached feed per user (top 200 items)",
                "S3 + CloudFront - media storage and CDN",
                "SQS/Kinesis - async fan-out queue"
            ],
            "notes": [
                "Hybrid fan-out model: fan-out on write for normal users, fan-out on read for celebrities",
                "Very read-heavy: feed reads outnumber writes 100:1",
                "Pre-computed feed trades storage for read latency",
                "Celebrity threshold is configurable (e.g. >100K followers = fan-out on read)"
            ]
        },
        "deep_dive": {
            "flows": [
                {
                    "name": "Post Creation + Fan-Out",
                    "steps": [
                        "Client sends POST /posts",
                        "Post Service writes post to DynamoDB posts table",
                        "Post Service publishes PostCreated event to SQS",
                        "Fan-Out Service (Lambda) picks up the event",
                        "If author has < 100K followers: fetch follower list, batch-write FeedItems to each follower's feed",
                        "If author has >= 100K followers: skip fan-out (handled at read time)",
                        "Invalidate cached feeds in Redis for affected followers"
                    ]
                },
                {
                    "name": "Feed Read Flow",
                    "steps": [
                        "Client sends GET /feed",
                        "Feed Service checks Redis for cached feed",
                        "If cache hit: return cached items",
                        "If cache miss: read pre-computed FeedItems from DynamoDB",
                        "Fetch posts from any followed celebrities (fan-out on read)",
                        "Merge, rank by score (recency + engagement), and paginate",
                        "Write merged result to Redis cache with short TTL (60s)",
                        "Return feed to client"
                    ]
                }
            ],
            "caching": "Redis caches the top 200 feed items per user with 60s TTL. Post metadata cached with longer TTL (5min). Cache invalidation on new fan-out writes. CDN caches media assets at edge.",
            "scaling": "DynamoDB on-demand capacity handles traffic spikes. Fan-out is async via SQS + Lambda, so post creation latency is not affected. Redis cluster for feed cache. For viral posts, ElastiCache absorbs read spikes that would otherwise hammer DynamoDB.",
            "notes": [
                "Celebrity fan-out on read adds ~50ms to feed latency but saves massive write amplification",
                "Use DynamoDB batch writes (25 items/batch) for fan-out efficiency",
                "Feed ranking score: time_decay * (1 + log(likes + 1) + log(comments + 1))",
                "Unfollow triggers async cleanup: remove FeedItems from the unfollowed user in background"
            ]
        },
        "tools": ["Amazon DynamoDB", "Amazon ElastiCache (Redis/Valkey)", "Amazon S3", "Amazon CloudFront", "AWS Lambda"],
        "reasoning": "Fast reads with eventual consistency, CDN for media, scalable fan-out"
    },

    "analytics": {
        "title": "Real-Time Analytics Platform",
        "description": "An analytics platform that ingests high-volume event streams, stores raw data for ad-hoc querying, and powers real-time dashboards. Think Mixpanel or Amplitude.",
        "requirements": {
            "functional": [
                "Ingest millions of events per second (page views, clicks, custom events)",
                "Query event data with flexible filters and time ranges",
                "Real-time dashboards with auto-refreshing metrics",
                "Support aggregations: count, sum, average, percentiles, unique counts",
                "Pre-built funnel and retention analysis",
                "Export raw event data for external analysis"
            ],
            "non_functional": [
                "High availability over consistency for event ingestion",
                "Event ingestion latency < 100ms (fire and forget)",
                "Dashboard query latency < 5s for common queries",
                "No data loss: at-least-once delivery for all events",
                "Cost-efficient storage for petabyte-scale historical data",
                "Support 30-day, 90-day, and 1-year retention tiers"
            ],
            "out_of_scope": [
                "User-level profile management",
                "A/B testing framework",
                "Alerting and anomaly detection",
                "Cross-device identity resolution"
            ]
        },
        "core_entities": [
            {
                "name": "Event",
                "fields": ["eventId (PK)", "eventType", "userId", "sessionId", "properties (JSON)", "timestamp", "receivedAt"]
            },
            {
                "name": "EventAggregate",
                "fields": ["metricKey (PK)", "timeBucket (SK)", "count", "sum", "min", "max", "uniqueUsers (HLL)"]
            },
            {
                "name": "Dashboard",
                "fields": ["id (PK)", "ownerId", "title", "widgets (JSON)", "createdAt", "updatedAt"]
            },
            {
                "name": "Query",
                "fields": ["id (PK)", "dashboardId?", "sql", "filters (JSON)", "timeRange", "cachedResultUrl?"]
            }
        ],
        "api": [
            {
                "method": "POST",
                "path": "/events",
                "description": "Ingest a batch of events (fire and forget)",
                "auth": "API key",
                "request_body": "{ events: [{ eventType, userId?, properties, timestamp }] }",
                "response": "202 Accepted"
            },
            {
                "method": "POST",
                "path": "/queries",
                "description": "Run an analytics query",
                "auth": "JWT token",
                "request_body": "{ eventType, aggregation, filters?, timeRange, groupBy? }",
                "response": "{ data: Row[], metadata }"
            },
            {
                "method": "GET",
                "path": "/dashboards/{id}",
                "description": "Get dashboard with widget definitions",
                "auth": "JWT token",
                "request_body": None,
                "response": "Dashboard"
            },
            {
                "method": "POST",
                "path": "/exports",
                "description": "Request raw data export as CSV/Parquet",
                "auth": "JWT token",
                "request_body": "{ eventType, timeRange, format }",
                "response": "{ exportId, status, downloadUrl? }"
            }
        ],
        "high_level": {
            "description": "Events are ingested via a lightweight API that immediately writes to Kinesis (or Kafka). A real-time processing layer (Lambda / Kinesis Data Analytics) computes streaming aggregates and writes to DynamoDB for dashboard queries. Raw events are batched and written to S3 (data lake) in Parquet format. For ad-hoc queries, Athena queries S3 directly. For heavy analytical workloads, Redshift loads data from S3 for complex aggregations. Pre-computed aggregates in DynamoDB power the real-time dashboards.",
            "components": [
                "Ingestion API - lightweight, stateless, returns 202 immediately",
                "Kinesis Data Streams - event buffering and ordering",
                "Lambda (stream processor) - computes real-time aggregates",
                "DynamoDB - pre-computed aggregates for dashboards",
                "S3 (Data Lake) - raw event storage in Parquet format",
                "Kinesis Firehose - batches events from stream to S3",
                "Athena - serverless SQL queries over S3 data lake",
                "Redshift - data warehouse for complex analytical queries",
                "CloudFront - caches dashboard assets and export downloads"
            ],
            "notes": [
                "Lambda architecture: real-time path (Kinesis -> Lambda -> DynamoDB) + batch path (S3 -> Athena/Redshift)",
                "Ingestion is pure append, no updates or deletes in the hot path",
                "S3 partitioned by date/hour for efficient Athena queries",
                "HyperLogLog (HLL) for approximate unique user counts at scale"
            ]
        },
        "deep_dive": {
            "flows": [
                {
                    "name": "Event Ingestion Pipeline",
                    "steps": [
                        "Client SDK batches events and sends POST /events",
                        "Ingestion API validates schema, returns 202 Accepted immediately",
                        "Events written to Kinesis Data Stream (partitioned by userId for ordering)",
                        "Kinesis Firehose consumer batches events into Parquet files on S3 (every 60s or 128MB)",
                        "Lambda consumer reads from Kinesis, computes incremental aggregates",
                        "Lambda updates DynamoDB aggregate table (atomic increment on counts)",
                        "Aggregate rows keyed by metricKey + timeBucket (e.g. page_view:2024-03-15:14)"
                    ]
                },
                {
                    "name": "Dashboard Query Flow",
                    "steps": [
                        "User opens dashboard, widgets fire queries",
                        "For real-time metrics: read pre-computed aggregates from DynamoDB",
                        "For ad-hoc queries: run Athena SQL over S3 data lake",
                        "For heavy aggregations: query Redshift (nightly loaded from S3)",
                        "Results cached in Redis with TTL matching dashboard refresh interval",
                        "Return data to dashboard widget for rendering"
                    ]
                }
            ],
            "caching": "Redis caches query results with configurable TTL (real-time widgets: 10s, historical: 5min). DynamoDB DAX for hot aggregate reads. Athena query results cached in S3 for repeat queries.",
            "scaling": "Kinesis scales with shard splitting for throughput. Lambda auto-scales consumers. S3 is effectively unlimited storage. Athena is serverless (pay per query). Redshift scales with node addition. Ingestion API is stateless and horizontally scalable.",
            "notes": [
                "Use Kinesis enhanced fan-out for dedicated read throughput per consumer",
                "S3 lifecycle policies: move data from Standard -> IA -> Glacier based on retention tier",
                "Partition S3 by date/hour: s3://analytics/events/year=2024/month=03/day=15/hour=14/",
                "Late-arriving events: Lambda handles out-of-order events by re-aggregating the affected time bucket"
            ]
        },
        "tools": ["Amazon S3", "Amazon Athena", "Amazon Redshift", "Amazon Kinesis Data Streams", "AWS Lambda"],
        "reasoning": "Data lake for raw events, OLAP for aggregations, real-time streaming"
    },

    "search": {
        "title": "Full-Text Search Platform",
        "description": "A search service that powers fast, relevant full-text search across large content catalogs with autocomplete, filters, and ranking. Think Elasticsearch-powered product or content search.",
        "requirements": {
            "functional": [
                "Full-text search with relevance ranking across documents",
                "Autocomplete / typeahead suggestions as user types",
                "Faceted filtering (category, price range, date, etc.)",
                "Support fuzzy matching and typo tolerance",
                "Search result highlighting of matched terms",
                "Index new and updated content within seconds"
            ],
            "non_functional": [
                "Search latency < 100ms at p99",
                "Autocomplete latency < 50ms",
                "High availability: search must always be available",
                "Support 10M+ documents in the index",
                "Eventual consistency OK: new content searchable within 5s",
                "Graceful degradation under load (return partial results)"
            ],
            "out_of_scope": [
                "Natural language understanding / semantic search",
                "Personalized ranking per user",
                "Image or video search",
                "Search analytics dashboard"
            ]
        },
        "core_entities": [
            {
                "name": "Document",
                "fields": ["id (PK)", "title", "body", "category", "tags[]", "authorId", "createdAt", "updatedAt"]
            },
            {
                "name": "SearchIndex",
                "fields": ["Managed by OpenSearch: inverted index on title, body, tags"]
            },
            {
                "name": "SuggestionEntry",
                "fields": ["prefix", "completions[]", "weight"]
            },
            {
                "name": "SearchLog",
                "fields": ["id (PK)", "query", "userId?", "resultCount", "clickedDocId?", "timestamp"]
            }
        ],
        "api": [
            {
                "method": "GET",
                "path": "/search?q={term}&category={cat}&page={n}",
                "description": "Full-text search with optional filters and pagination",
                "auth": "Optional JWT token",
                "request_body": None,
                "response": "{ hits: Document[], total, facets, took_ms }"
            },
            {
                "method": "GET",
                "path": "/suggest?q={prefix}",
                "description": "Autocomplete suggestions",
                "auth": None,
                "request_body": None,
                "response": "{ suggestions: string[] }"
            },
            {
                "method": "POST",
                "path": "/documents",
                "description": "Index a new document (internal / admin)",
                "auth": "API key",
                "request_body": "{ title, body, category, tags[] }",
                "response": "Document"
            },
            {
                "method": "PUT",
                "path": "/documents/{id}",
                "description": "Update an existing document in the index",
                "auth": "API key",
                "request_body": "{ title?, body?, category?, tags[]? }",
                "response": "Document"
            }
        ],
        "high_level": {
            "description": "Clients send search queries through an API Gateway to a Search Service. The Search Service queries OpenSearch (managed Elasticsearch) for full-text search with BM25 ranking. Source-of-truth document data lives in DynamoDB. When documents are created or updated, a change event flows through a DynamoDB Stream to a Lambda that indexes the document in OpenSearch. CloudFront caches popular search results at the edge. Autocomplete is powered by OpenSearch's completion suggester or a separate Redis-backed trie.",
            "components": [
                "API Gateway - rate limiting, routing",
                "Search Service - query building, result formatting",
                "OpenSearch (managed) - full-text search, inverted index, ranking",
                "DynamoDB - source of truth for document data",
                "DynamoDB Streams + Lambda - change data capture for index sync",
                "CloudFront - edge caching for popular queries",
                "Redis - autocomplete prefix trie, query result cache"
            ],
            "notes": [
                "Very read-heavy: search queries vastly outnumber document writes",
                "OpenSearch handles tokenization, stemming, and relevance scoring",
                "Dual write problem avoided: DynamoDB is source of truth, OpenSearch is derived index",
                "CloudFront caches search results for common queries (cache key = normalized query + filters)"
            ]
        },
        "deep_dive": {
            "flows": [
                {
                    "name": "Search Query Flow",
                    "steps": [
                        "Client sends GET /search?q=term&category=tech",
                        "CloudFront checks edge cache for this query",
                        "On cache miss: route to Search Service",
                        "Search Service builds OpenSearch DSL query with filters and boosting",
                        "OpenSearch executes query: tokenize -> match inverted index -> score with BM25 -> apply filters",
                        "Results returned with highlights and facet counts",
                        "Search Service enriches results with DynamoDB data if needed",
                        "Response cached at CloudFront edge with short TTL (30s)"
                    ]
                },
                {
                    "name": "Document Indexing Flow",
                    "steps": [
                        "Document created/updated in DynamoDB via internal API",
                        "DynamoDB Stream captures the change event",
                        "Lambda reads the stream event, transforms to OpenSearch document format",
                        "Lambda sends index/update request to OpenSearch",
                        "Document becomes searchable within 1-5 seconds (near real-time)",
                        "Autocomplete suggestions updated if title/tags changed"
                    ]
                }
            ],
            "caching": "CloudFront caches top search queries at edge (30s TTL). Redis caches autocomplete prefix results (5min TTL). OpenSearch has internal request cache for repeated queries. DynamoDB DAX for hot document reads.",
            "scaling": "OpenSearch cluster scales with data nodes for throughput and replicas for read capacity. DynamoDB auto-scales. Lambda handles indexing spikes. CloudFront absorbs traffic spikes for popular queries, protecting the backend.",
            "notes": [
                "Use OpenSearch index aliases for zero-downtime reindexing",
                "Implement circuit breaker: if OpenSearch is slow, return cached results or degrade gracefully",
                "Autocomplete uses edge n-grams or completion suggester for sub-50ms latency",
                "Log all queries to SearchLog for future relevance tuning (click-through rate analysis)"
            ]
        },
        "tools": ["Amazon OpenSearch Service", "Amazon DynamoDB", "Amazon CloudFront", "AWS Lambda"],
        "reasoning": "Full-text search, metadata storage, edge caching for popular queries"
    },

    "auth": {
        "title": "Authentication & Authorization Service",
        "description": "A centralized auth platform handling user registration, login, token management, RBAC permissions, and session management. Think Auth0 or AWS Cognito.",
        "requirements": {
            "functional": [
                "User registration with email verification",
                "Login with email/password and OAuth providers (Google, GitHub)",
                "JWT access tokens + refresh token rotation",
                "Role-based access control (RBAC) with granular permissions",
                "Session management with revocation",
                "Password reset flow via email"
            ],
            "non_functional": [
                "Authentication latency < 200ms",
                "Token validation must be stateless (JWT verification without DB call)",
                "Rate limiting on login attempts (brute force protection)",
                "Passwords stored with bcrypt (cost factor 12+)",
                "99.99% availability: auth is on the critical path for all services",
                "Support for multi-region deployment (low-latency globally)"
            ],
            "out_of_scope": [
                "Multi-factor authentication (MFA / 2FA)",
                "SAML / enterprise SSO integration",
                "Fine-grained attribute-based access control (ABAC)",
                "User profile management beyond auth"
            ]
        },
        "core_entities": [
            {
                "name": "User",
                "fields": ["id (PK)", "email (unique index)", "passwordHash", "emailVerified", "createdAt", "updatedAt"]
            },
            {
                "name": "OAuthAccount",
                "fields": ["id (PK)", "userId (index)", "provider: google|github", "providerUserId", "accessToken", "refreshToken"]
            },
            {
                "name": "Role",
                "fields": ["id (PK)", "name (unique)", "permissions[]"]
            },
            {
                "name": "UserRole",
                "fields": ["userId (PK)", "roleId (SK)", "grantedAt", "grantedBy"]
            },
            {
                "name": "RefreshToken",
                "fields": ["tokenHash (PK)", "userId (index)", "expiresAt", "revokedAt?", "deviceInfo", "createdAt"]
            },
            {
                "name": "Session",
                "fields": ["id (PK)", "userId (index)", "ipAddress", "userAgent", "lastActiveAt", "expiresAt"]
            }
        ],
        "api": [
            {
                "method": "POST",
                "path": "/auth/register",
                "description": "Register a new user account",
                "auth": None,
                "request_body": "{ email, password, name }",
                "response": "{ userId, message: 'Verification email sent' }"
            },
            {
                "method": "POST",
                "path": "/auth/login",
                "description": "Login with credentials, returns token pair",
                "auth": None,
                "request_body": "{ email, password }",
                "response": "{ accessToken, refreshToken, expiresIn }"
            },
            {
                "method": "POST",
                "path": "/auth/refresh",
                "description": "Rotate refresh token, get new access token",
                "auth": "Refresh token in body",
                "request_body": "{ refreshToken }",
                "response": "{ accessToken, refreshToken, expiresIn }"
            },
            {
                "method": "POST",
                "path": "/auth/logout",
                "description": "Revoke refresh token and end session",
                "auth": "JWT token",
                "request_body": "{ refreshToken }",
                "response": "200 OK"
            },
            {
                "method": "GET",
                "path": "/auth/me",
                "description": "Get current user info and permissions",
                "auth": "JWT token",
                "request_body": None,
                "response": "{ user, roles, permissions[] }"
            },
            {
                "method": "POST",
                "path": "/auth/password-reset",
                "description": "Request password reset email",
                "auth": None,
                "request_body": "{ email }",
                "response": "200 OK (always, to prevent email enumeration)"
            }
        ],
        "high_level": {
            "description": "Clients hit an API Gateway that rate-limits login attempts and routes to the Auth Service. The Auth Service handles registration, login, and token management. User records live in DynamoDB (global table for multi-region). Passwords are hashed with bcrypt before storage. On login, the Auth Service issues a short-lived JWT access token (15min) and a longer-lived refresh token (stored in DynamoDB). ElastiCache (Redis) stores active sessions and a token revocation blocklist. Cognito handles OAuth provider integration. Lambda processes async tasks like sending verification emails via SES.",
            "components": [
                "API Gateway - rate limiting (login), routing, WAF",
                "Auth Service - registration, login, token management, RBAC",
                "Cognito - OAuth provider integration (Google, GitHub)",
                "DynamoDB (Global Table) - user records, refresh tokens, roles",
                "ElastiCache (Redis) - session store, token revocation blocklist",
                "Lambda - async email sending, cleanup jobs",
                "SES - transactional emails (verification, password reset)",
                "CloudFront - JWKS endpoint caching for token verification"
            ],
            "notes": [
                "Auth is on the critical path: every API call in every service verifies the JWT",
                "JWT verification is stateless: services only need the public key (JWKS) to verify",
                "Refresh token rotation: each refresh invalidates the old token (detect token theft)",
                "DynamoDB Global Tables for multi-region: low-latency auth worldwide"
            ]
        },
        "deep_dive": {
            "flows": [
                {
                    "name": "Login Flow",
                    "steps": [
                        "Client sends POST /auth/login with email + password",
                        "API Gateway checks rate limit (5 attempts per email per 15min)",
                        "Auth Service looks up user by email in DynamoDB",
                        "Compare password against stored bcrypt hash",
                        "On match: generate JWT access token (signed with RS256 private key, 15min expiry)",
                        "Generate refresh token (random 256-bit token), hash it, store in DynamoDB with TTL",
                        "Create Session record in Redis with user metadata",
                        "Return { accessToken, refreshToken, expiresIn } to client"
                    ]
                },
                {
                    "name": "Token Refresh Flow",
                    "steps": [
                        "Client sends POST /auth/refresh with refreshToken",
                        "Auth Service hashes the token, looks up in DynamoDB",
                        "Verify token is not expired and not revoked",
                        "Revoke the current refresh token (mark revokedAt)",
                        "Issue new access token + new refresh token (rotation)",
                        "Store new refresh token hash in DynamoDB",
                        "If old token was already revoked: potential token theft detected, revoke ALL user tokens"
                    ]
                },
                {
                    "name": "Token Verification (other services)",
                    "steps": [
                        "Service receives request with Authorization: Bearer <jwt>",
                        "Fetch JWKS public key (cached locally or from CloudFront-backed endpoint)",
                        "Verify JWT signature, expiry, issuer, audience",
                        "Optionally check Redis blocklist for revoked tokens (for immediate revocation)",
                        "Extract userId and permissions from JWT claims",
                        "Proceed with authorized request"
                    ]
                }
            ],
            "caching": "Redis stores active sessions, token revocation blocklist (SET with TTL matching token expiry), and rate limit counters (INCR with TTL). JWKS endpoint cached at CloudFront edge and locally in services (refresh every 5min).",
            "scaling": "Auth Service scales horizontally (stateless after JWT issuance). DynamoDB Global Tables replicate user data across regions. Redis cluster for session store. CloudFront caches JWKS globally so token verification never hits the Auth Service.",
            "notes": [
                "RS256 (asymmetric) for JWT signing: only Auth Service has the private key, all services verify with the public key",
                "Refresh token rotation prevents token replay attacks",
                "Bcrypt cost factor 12+ ensures password hashing takes ~250ms (resistant to brute force)",
                "Rate limiting at API Gateway level, not application level, to protect against DDoS"
            ]
        },
        "tools": ["Amazon DynamoDB", "Amazon ElastiCache (Redis/Valkey)", "AWS Lambda", "Amazon CloudFront", "AWS IAM"],
        "reasoning": "Identity management, session storage, token caching, global availability"
    },

    "uber": {
        "title": "Uber Ride-Sharing Platform",
        "description": "A ride-sharing platform that connects passengers with drivers who offer transportation services in personal vehicles. It allows users to book rides on-demand from their smartphones, matching them with a nearby driver.",
        "requirements": {
            "functional": [
                "Riders should be able to input a start location and a destination and get a fare estimate",
                "Riders should be able to request a ride based on the estimated fare",
                "Upon request, riders should be matched with a driver who is nearby and available",
                "Drivers should be able to accept/decline a request and navigate to pickup/drop-off"
            ],
            "non_functional": [
                "The system should prioritize low latency matching (< 1 minute to match or failure)",
                "The system should ensure strong consistency in ride matching to prevent any driver from being assigned multiple rides simultaneously",
                "The system should be able to handle high throughput, especially during peak hours or special events (100k requests from same location)"
            ],
            "out_of_scope": [
                "Riders should be able to rate their ride and driver post-trip",
                "Drivers should be able to rate passengers",
                "Riders should be able to schedule rides in advance",
                "Riders should be able to request different categories of rides (e.g., X, XL, Comfort)"
            ]
        },
        "core_entities": [
            {
                "name": "Rider",
                "fields": ["id (PK)", "name", "email", "phone", "paymentMethods[]", "createdAt"]
            },
            {
                "name": "Driver",
                "fields": ["id (PK)", "name", "email", "phone", "vehicleInfo (JSON)", "availabilityStatus", "currentLocation (lat, long)", "rating", "createdAt"]
            },
            {
                "name": "Fare",
                "fields": ["id (PK)", "pickupLocation (lat, long)", "destination (lat, long)", "estimatedFare", "estimatedETA", "distance", "createdAt"]
            },
            {
                "name": "Ride",
                "fields": ["id (PK)", "riderId (index)", "driverId (index)", "fareId", "status: requested|matched|accepted|inProgress|completed|cancelled", "pickupLocation", "destination", "actualFare", "pickupTime", "dropoffTime", "createdAt", "updatedAt"]
            },
            {
                "name": "Location",
                "fields": ["driverId (PK)", "latitude", "longitude", "heading", "speed", "timestamp", "accuracy"]
            }
        ],
        "api": [
            {
                "method": "POST",
                "path": "/fare",
                "description": "Get fare estimate for a ride",
                "auth": "JWT token (rider)",
                "request_body": "{ pickupLocation: {lat, long}, destination: {lat, long} }",
                "response": "Fare"
            },
            {
                "method": "POST",
                "path": "/rides",
                "description": "Request a ride based on fare estimate",
                "auth": "JWT token (rider)",
                "request_body": "{ fareId }",
                "response": "Ride"
            },
            {
                "method": "POST",
                "path": "/drivers/location",
                "description": "Update driver location (called every 3-5 seconds)",
                "auth": "JWT token (driver) in session",
                "request_body": "{ lat, long, heading?, speed? }",
                "response": "200 OK"
            },
            {
                "method": "PATCH",
                "path": "/rides/{rideId}",
                "description": "Accept or decline a ride request",
                "auth": "JWT token (driver)",
                "request_body": "{ status: 'accepted' | 'declined' }",
                "response": "Ride"
            },
            {
                "method": "GET",
                "path": "/rides/{rideId}",
                "description": "Get ride details",
                "auth": "JWT token",
                "request_body": None,
                "response": "Ride"
            }
        ],
        "high_level": {
            "description": "Rider and Driver Clients communicate through an API Gateway. The Ride Service handles fare estimation and ride state management. The Location Service receives driver location updates every 3-5 seconds and stores them in a spatial index (e.g., Geohash in Redis or PostgreSQL + PostGIS). The Ride Matching Service uses this spatial index to find nearby available drivers when a ride is requested. A Notification Service (via APN/FCM) alerts drivers to new ride requests. When a driver accepts, the ride status updates and navigation coordinates are provided. SQS queues handle ride requests to ensure no dropped requests during peak demand. Temporal/Step Functions manage the timeout workflow if drivers don't respond.",
            "components": [
                "API Gateway - authentication, rate limiting, routing",
                "Rider Client - iOS/Android app for requesting rides",
                "Driver Client - iOS/Android app for receiving requests and location updates",
                "Ride Service - fare estimation, ride CRUD, state management",
                "Location Service - receives and stores driver locations with spatial indexing",
                "Ride Matching Service - proximity-based driver matching algorithm",
                "Notification Service - pushes ride requests to drivers (APN/FCM)",
                "PostgreSQL with PostGIS - driver locations with geospatial queries",
                "Redis - driver availability state, ride request locks, geohash indexing",
                "SQS - queues ride requests to prevent drops during peak load",
                "Temporal/Step Functions - manage driver response timeout workflows",
                "Third-Party Mapping API - Google Maps for routing and distance calculation"
            ],
            "notes": [
                "Write-heavy for location updates: ~2M writes/second with 10M drivers updating every 5s",
                "Read-heavy for proximity searches during ride matching",
                "Strong consistency required for ride matching to prevent double-booking drivers",
                "Spatial indexing (Geohash, S2, or PostGIS) critical for sub-second proximity queries",
                "Client-side intelligence reduces location update frequency based on movement"
            ]
        },
        "deep_dive": {
            "flows": [
                {
                    "name": "Fare Estimation Flow",
                    "steps": [
                        "Rider enters pickup and destination in client app",
                        "Client sends POST /fare with coordinates",
                        "API Gateway authenticates and routes to Ride Service",
                        "Ride Service calls Third-Party Mapping API to calculate distance and travel time",
                        "Apply pricing model (base fare + distance + time + surge multiplier)",
                        "Create Fare entity in database with estimated price and ETA",
                        "Return Fare to client for rider review"
                    ]
                },
                {
                    "name": "Ride Request & Matching Flow",
                    "steps": [
                        "Rider accepts fare and sends POST /rides with fareId",
                        "API Gateway routes to Ride Matching Service",
                        "Create Ride record with status=requested",
                        "Publish ride request to SQS queue for durability",
                        "Ride Matching Service queries Location Service for nearby available drivers using geospatial index",
                        "Rank drivers by proximity, availability, rating",
                        "Acquire distributed lock (Redis SETNX) on top driver to prevent concurrent assignment",
                        "Update driver status to 'pending' in Redis",
                        "Send push notification to driver via Notification Service (APN/FCM)",
                        "Start Temporal workflow with 10-second timeout for driver response",
                        "If driver accepts: update Ride status=accepted, release lock",
                        "If driver declines or times out: release lock, notify next driver in ranked list",
                        "Return Ride to rider with match status"
                    ]
                },
                {
                    "name": "Driver Location Update Flow",
                    "steps": [
                        "Driver Client detects movement via GPS sensors",
                        "Client uses on-device logic to determine if update is needed (movement threshold, time elapsed)",
                        "Send POST /drivers/location with lat, long",
                        "API Gateway authenticates driver from JWT session",
                        "Location Service receives update",
                        "Update Location table with latest coordinates and timestamp",
                        "Update spatial index (Redis Geohash or PostGIS geography) for proximity queries",
                        "Location data TTL set to 2 minutes (auto-expire stale locations)"
                    ]
                },
                {
                    "name": "Driver Accept/Decline Flow",
                    "steps": [
                        "Driver receives push notification with rideId",
                        "Driver opens app, views ride details",
                        "Driver sends PATCH /rides/{rideId} with accept/decline",
                        "Ride Service verifies driver is assigned to this ride",
                        "If accept: update Ride status=accepted, complete Temporal workflow",
                        "If decline: mark driver unavailable temporarily, trigger next driver in queue",
                        "Return updated Ride with pickup location coordinates to driver",
                        "Driver uses client GPS for navigation to pickup"
                    ]
                }
            ],
            "caching": "Redis stores driver availability state (SET with driver ID, TTL 2min), geohash index for spatial queries, and distributed locks (SETNX) for ride assignment. Location data cached with short TTL. Ride request queue in SQS ensures durability.",
            "scaling": "Location Service scales horizontally to handle 2M+ writes/second. Redis cluster with sharding for geospatial data. PostgreSQL read replicas for ride history queries. SQS decouples ride matching from request ingestion. Temporal scales workflow execution for timeout management. API Gateway auto-scales with traffic. Notification Service batches push requests.",
            "notes": [
                "Geospatial indexing: Geohash (Redis) or PostGIS (PostgreSQL) for sub-100ms proximity queries on 10M+ driver locations",
                "Client-side optimizations: only send location updates when driver moves >50m or 30s elapsed, reducing write load by ~60%",
                "Distributed locking: Redis SETNX with TTL prevents race conditions on driver assignment during concurrent ride requests",
                "Temporal workflow handles driver timeout: if no response in 10s, automatically moves to next driver",
                "SQS dead letter queue for failed ride requests with retry logic",
                "Surge pricing: real-time calculation based on supply/demand ratio in geohashed zones",
                "PostGIS ST_Distance function for accurate proximity calculations accounting for earth curvature",
                "Location Service uses write-through cache: update Redis + PostgreSQL in parallel for durability"
            ]
        },
        "tools": ["Amazon RDS for PostgreSQL", "Amazon ElastiCache (Redis/Valkey)", "Amazon SQS (Standard)", "AWS Lambda", "AWS Step Functions"],
        "reasoning": "Geospatial queries for driver matching, high-frequency location updates, distributed locking for consistency, durable queues for peak load"
    },

    "bitly": {
        "title": "URL Shortener (Bit.ly)",
        "description": "A URL shortening service that converts long URLs into shorter, manageable links. It provides quick redirection and supports custom aliases and expiration dates.",
        "requirements": {
            "functional": [
                "Users should be able to submit a long URL and receive a shortened version",
                "Users should be able to specify a custom alias for their shortened URL (optional)",
                "Users should be able to specify an expiration date for their shortened URL (optional)",
                "Users should be able to access the original URL by using the shortened URL"
            ],
            "non_functional": [
                "The system should ensure uniqueness for the short codes (each short code maps to exactly one long URL)",
                "The redirection should occur with minimal delay (< 100ms)",
                "The system should be reliable and available 99.99% of the time (availability > consistency)",
                "The system should scale to support 1B shortened URLs and 100M DAU",
                "Read-to-write ratio heavily skewed: 1000 reads per 1 write"
            ],
            "out_of_scope": [
                "User authentication and account management",
                "Analytics on link clicks (e.g., click counts, geographic data)",
                "Data consistency in real-time analytics",
                "Advanced security features like spam detection and malicious URL filtering"
            ]
        },
        "core_entities": [
            {
                "name": "URLMapping",
                "fields": ["shortCode (PK, index)", "longUrl", "customAlias?", "expirationDate?", "createdAt", "userId?", "clickCount"]
            },
            {
                "name": "User",
                "fields": ["id (PK)", "email", "name", "createdAt"]
            }
        ],
        "api": [
            {
                "method": "POST",
                "path": "/urls",
                "description": "Shorten a URL",
                "auth": "Optional JWT token",
                "request_body": "{ long_url, custom_alias?, expiration_date? }",
                "response": "{ short_url }"
            },
            {
                "method": "GET",
                "path": "/{short_code}",
                "description": "Redirect to original URL",
                "auth": None,
                "request_body": None,
                "response": "HTTP 302 Redirect to original long URL"
            }
        ],
        "high_level": {
            "description": "Client submits long URLs through an API Gateway to a Write Service, which generates unique short codes using a counter stored in Redis. The short code is generated via base62 encoding of an auto-incrementing counter. The mapping is stored in a database (PostgreSQL or DynamoDB). When users access a shortened URL, the request goes to a Read Service which looks up the short code in a cache (Redis/ElastiCache) first, then falls back to the database if needed. The system uses HTTP 302 redirects to send users to the original URL. Read and Write services are separated to scale independently based on the 1000:1 read-to-write ratio.",
            "components": [
                "Client - web/mobile application",
                "API Gateway - rate limiting, routing",
                "Load Balancer - distributes traffic across service instances",
                "Write Service - handles URL shortening, generates short codes",
                "Read Service - handles redirects, optimized for high throughput",
                "Redis (centralized) - stores counter for short code generation, atomic increment",
                "ElastiCache (Redis) - caches URL mappings for fast lookups",
                "PostgreSQL or DynamoDB - persistent storage for URL mappings",
                "CDN (CloudFront) - edge caching for popular short URLs"
            ],
            "notes": [
                "Extremely read-heavy: 1000 reads per write (redirects vastly outnumber URL creations)",
                "Short code generation uses base62 encoding (a-z, A-Z, 0-9) of counter for uniqueness",
                "8-character base62 code supports 62^8 = 218 trillion unique URLs",
                "HTTP 302 (temporary redirect) preferred over 301 to maintain control and enable analytics",
                "Caching strategy critical for performance: Redis cache with TTL for hot URLs"
            ]
        },
        "deep_dive": {
            "flows": [
                {
                    "name": "URL Shortening Flow",
                    "steps": [
                        "Client sends POST /urls with long_url, optional custom_alias, expiration_date",
                        "API Gateway routes to Write Service",
                        "Write Service validates long URL format",
                        "If custom_alias provided: check database for uniqueness, use if available",
                        "If no custom_alias: request next counter value from Redis (atomic INCR)",
                        "Encode counter value to base62 string (62^8 combinations with 8 chars)",
                        "Store mapping in database: shortCode -> longUrl, expirationDate, createdAt",
                        "Return short URL to client (e.g., short.ly/abc123)"
                    ]
                },
                {
                    "name": "URL Redirect Flow",
                    "steps": [
                        "User clicks shortened URL (e.g., short.ly/abc123)",
                        "Browser sends GET /abc123",
                        "CDN checks edge cache for this short code",
                        "On CDN miss: request routes through Load Balancer to Read Service",
                        "Read Service checks Redis cache for short code",
                        "On cache hit: retrieve long URL from Redis",
                        "On cache miss: query database for shortCode, store result in Redis (with TTL)",
                        "Verify expiration date hasn't passed",
                        "Return HTTP 302 redirect with Location header set to long URL",
                        "Browser automatically follows redirect to original URL"
                    ]
                }
            ],
            "caching": "Redis cache stores short code -> long URL mappings with configurable TTL (1 hour for normal URLs, 24 hours for popular URLs). Cache hit rate target: 95%+. CDN caches responses at edge for ultra-popular URLs (viral links). Cache invalidation on expiration or manual deletion.",
            "scaling": "Read Service scales horizontally to handle 1000:1 read-to-write ratio. Write Service scales modestly. Redis counter uses batching: each Write Service instance requests batches of 1000 counter values to reduce Redis load. Database uses read replicas for query distribution. CDN absorbs traffic spikes for viral links. Load balancer distributes requests across service instances.",
            "notes": [
                "Base62 encoding: counter 12345 -> base62 'dnh' (using charset: a-z, A-Z, 0-9)",
                "Counter batching: Write Service requests 1000 counter values at once from Redis, uses locally, reducing network calls by 1000x",
                "Redis replication for counter: Redis Enterprise with automatic failover, periodic snapshots to durable storage",
                "Custom alias collision handling: check database first, return error if taken",
                "HTTP 302 vs 301: 302 prevents browser caching, maintains control over redirects, enables future analytics",
                "Database sizing: 1B URLs * 500 bytes/row = 500GB, easily fits in single PostgreSQL instance",
                "Expiration handling: background job periodically scans and deletes expired URLs, or use TTL feature in DynamoDB",
                "Short code uniqueness guaranteed: single Redis counter with atomic increment ensures global uniqueness across all Write Service instances"
            ]
        },
        "tools": ["Amazon RDS for PostgreSQL", "Amazon ElastiCache (Redis/Valkey)", "Amazon CloudFront", "AWS Lambda", "Amazon DynamoDB"],
        "reasoning": "High read throughput with caching, unique ID generation, simple key-value lookups, edge caching for viral links"
    },

    "dropbox": {
        "title": "Cloud File Storage (Dropbox)",
        "description": "A cloud-based file storage service that allows users to store and share files, providing secure and reliable access from anywhere, on any device. Supports automatic file syncing across devices.",
        "requirements": {
            "functional": [
                "Users should be able to upload a file from any device",
                "Users should be able to download a file from any device",
                "Users should be able to share a file with other users and view files shared with them",
                "Users can automatically sync files across devices"
            ],
            "non_functional": [
                "The system should be highly available (prioritizing availability over consistency)",
                "The system should support files as large as 50GB",
                "The system should be secure and reliable. We should be able to recover files if they are lost or corrupted",
                "The system should make upload, download, and sync times as fast as possible (low latency)"
            ],
            "out_of_scope": [
                "Users should be able to edit files",
                "Users should be able to view files without downloading them",
                "The system should have a storage limit per user",
                "The system should support file versioning",
                "The system should scan files for viruses and malware"
            ]
        },
        "core_entities": [
            {
                "name": "File",
                "fields": ["Raw binary data stored in S3"]
            },
            {
                "name": "FileMetadata",
                "fields": ["id (PK, fingerprint/hash)", "name", "size", "mimeType", "uploadedBy (index)", "status: uploading|uploaded|failed", "chunks[] (id, status, ETag)", "createdAt", "updatedAt", "s3Key", "uploadId (multipart)"]
            },
            {
                "name": "User",
                "fields": ["id (PK)", "email", "name", "createdAt"]
            },
            {
                "name": "SharedFiles",
                "fields": ["fileId (PK)", "userId (SK)", "sharedBy", "permissions", "sharedAt"]
            }
        ],
        "api": [
            {
                "method": "POST",
                "path": "/files",
                "description": "Initiate file upload (returns presigned URLs for chunks)",
                "auth": "JWT token",
                "request_body": "{ fileFingerprint, fileName, fileSize, mimeType, chunkFingerprints[] }",
                "response": "{ fileId, uploadId, presignedUrls[] }"
            },
            {
                "method": "PATCH",
                "path": "/files/{fileId}/chunks",
                "description": "Update chunk upload status",
                "auth": "JWT token",
                "request_body": "{ chunkId, status, ETag }",
                "response": "200 OK"
            },
            {
                "method": "GET",
                "path": "/files/{fileId}",
                "description": "Get file metadata and presigned download URL",
                "auth": "JWT token",
                "request_body": None,
                "response": "{ fileMetadata, downloadUrl }"
            },
            {
                "method": "POST",
                "path": "/files/{fileId}/share",
                "description": "Share file with other users",
                "auth": "JWT token",
                "request_body": "{ userEmails[] }",
                "response": "200 OK"
            },
            {
                "method": "GET",
                "path": "/files/{fileId}/changes",
                "description": "Check for file changes for sync",
                "auth": "JWT token",
                "request_body": None,
                "response": "{ fileMetadata, changedChunks[] }"
            }
        ],
        "high_level": {
            "description": "Clients (web, mobile, desktop) interact through an API Gateway with a File Service that manages metadata in DynamoDB. Files are stored directly in S3 using presigned URLs - clients upload/download directly to/from S3, bypassing application servers for the actual data transfer. For large files, multipart upload with chunking is used: files are split into 5-10MB chunks on the client, each chunk uploaded with its own presigned URL, and S3 combines them. A client-side Sync Agent monitors local file changes and polls/websocket for remote changes. CDN (CloudFront) caches popular files at the edge for fast downloads. Shared file permissions are managed via a SharedFiles table. File fingerprinting (SHA-256) enables deduplication and resumable uploads.",
            "components": [
                "Client (web/mobile/desktop) - uploader/downloader with Sync Agent",
                "API Gateway - authentication, rate limiting, routing",
                "Load Balancer - distributes traffic across File Service instances",
                "File Service - manages metadata, generates presigned URLs, validates permissions",
                "DynamoDB - stores file metadata, chunks status, shared file ACLs",
                "S3 - blob storage for actual file data (with encryption at rest)",
                "CloudFront CDN - edge caching for downloads",
                "WebSocket Service - pushes real-time sync notifications for fresh files",
                "Lambda - async processing for share notifications, cleanup jobs"
            ],
            "notes": [
                "Direct S3 upload/download via presigned URLs avoids double network hop through app servers",
                "Chunking enables resumable uploads, progress indicators, and parallel transfers",
                "File fingerprinting (SHA-256) used as fileId for deduplication",
                "Hybrid sync: WebSocket for fresh files (<24h), polling for stale files",
                "Eventual consistency: clients may see slightly stale data briefly after upload"
            ]
        },
        "deep_dive": {
            "flows": [
                {
                    "name": "Large File Upload with Chunking",
                    "steps": [
                        "Client chunks file into 5-10MB pieces, calculates SHA-256 fingerprint for each chunk and entire file",
                        "Client sends GET /files/{fileFingerprint} to check if file already exists (deduplication)",
                        "If not exists: Client sends POST /files to initiate multipart upload",
                        "File Service calls S3 CreateMultipartUpload API, gets uploadId",
                        "File Service generates presigned URLs for each chunk (with uploadId and partNumber)",
                        "File Service creates FileMetadata record in DynamoDB with status='uploading', stores chunk list",
                        "File Service returns uploadId and presigned URLs to client",
                        "Client uploads each chunk directly to S3 using presigned URLs (in parallel)",
                        "After each chunk upload, client sends PATCH /files/{fileId}/chunks with chunkId and ETag",
                        "File Service verifies chunk upload via S3 ListParts API, updates DynamoDB chunk status",
                        "Once all chunks uploaded: File Service calls S3 CompleteMultipartUpload",
                        "File Service updates FileMetadata status='uploaded'",
                        "S3 combines all chunks into single object"
                    ]
                },
                {
                    "name": "File Download Flow",
                    "steps": [
                        "Client sends GET /files/{fileId}",
                        "File Service checks SharedFiles table to verify user has access",
                        "File Service checks CloudFront CDN cache for file",
                        "On CDN hit: return cached file URL",
                        "On CDN miss: File Service generates presigned S3 URL with 5min expiration",
                        "Return presigned URL to client",
                        "Client downloads directly from S3 (or CloudFront if cached)",
                        "CloudFront caches file at edge for future requests"
                    ]
                },
                {
                    "name": "File Sharing Flow",
                    "steps": [
                        "User sends POST /files/{fileId}/share with list of user emails",
                        "File Service looks up user IDs from emails",
                        "File Service writes entries to SharedFiles table: fileId + userId + permissions",
                        "File Service publishes share notification event to SNS/SQS",
                        "Lambda consumer sends email notifications to shared users",
                        "Shared users can now access file via GET /files/{fileId} (permission check passes)"
                    ]
                },
                {
                    "name": "Automatic File Sync (Local -> Remote)",
                    "steps": [
                        "Client-side Sync Agent monitors local Dropbox folder with FileSystemWatcher",
                        "Detects file modification event",
                        "Calculates file fingerprint, compares with local cache",
                        "If changed: queues file for upload",
                        "Uses multipart upload flow to send to S3",
                        "Updates local cache with new fingerprint and timestamp",
                        "WebSocket Service notifies other devices of this user about the change"
                    ]
                },
                {
                    "name": "Automatic File Sync (Remote -> Local)",
                    "steps": [
                        "For fresh files (<24h): Client maintains WebSocket connection to sync service",
                        "Server pushes notification when file changes: { fileId, newFingerprint, updatedAt }",
                        "Client receives notification, checks if file differs from local copy",
                        "If different: initiates download via GET /files/{fileId}",
                        "For stale files: Client polls GET /files/{fileId}/changes every 5 minutes",
                        "Server returns list of files with updatedAt > lastSyncTime",
                        "Client downloads changed files"
                    ]
                }
            ],
            "caching": "CloudFront CDN caches files at edge locations with TTL (1 hour for normal files, 24 hours for popular files). DynamoDB DAX caches hot metadata reads. Presigned URLs have short 5-minute TTL for security. Client-side cache stores file fingerprints to detect local changes.",
            "scaling": "File Service scales horizontally behind load balancer. S3 auto-scales for storage and throughput. DynamoDB on-demand capacity handles metadata writes. CloudFront distributes download load globally. WebSocket Service uses Redis pub/sub for cross-node message routing. Multipart upload parallelizes chunk transfers to maximize bandwidth.",
            "notes": [
                "Presigned URLs: client uploads/downloads directly to S3, bypassing app servers for 50GB files",
                "Chunking math: 50GB file / 100Mbps = 4000s = 1.11 hours, needs resumability",
                "File fingerprinting: SHA-256 hash used as unique fileId, enables deduplication",
                "Multipart upload: S3 API for uploading files in parts, each part 5MB-5GB",
                "Chunk parallelization: upload multiple chunks simultaneously to saturate bandwidth",
                "Compression: client compresses text files before upload (not media files), must compress before encrypt",
                "Encryption: HTTPS in transit, S3 server-side encryption at rest with unique keys per file",
                "Signed URLs for security: bearer tokens with 5min expiration, prevents unauthorized sharing",
                "Conflict resolution: last write wins strategy, can be improved with operational transforms",
                "S3 ListParts API: verify chunk uploads in progress, returns ETags for all uploaded parts"
            ]
        },
        "tools": ["Amazon S3", "Amazon DynamoDB", "Amazon CloudFront", "AWS Lambda", "Amazon API Gateway"],
        "reasoning": "Blob storage for files, metadata storage, CDN for fast downloads, presigned URLs for direct upload/download"
    }
}
