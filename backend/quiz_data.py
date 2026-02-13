TECHNOLOGY_QUIZ_QUESTIONS = [
    {
        "id": "db-selection-1",
        "category": "Database Selection",
        "question": "You're building a social media feed with 100M users. Requirements: 10K reads/sec, 1K writes/sec, eventual consistency acceptable, need to store posts with nested comments. Which database would you choose?",
        "options": [
            {"id": "a", "text": "PostgreSQL with read replicas"},
            {"id": "b", "text": "DynamoDB"},
            {"id": "c", "text": "MongoDB"},
            {"id": "d", "text": "Redis"}
        ],
        "correct_answer": "b",
        "explanation": "DynamoDB is ideal because: 1) Scales horizontally for high read/write load, 2) Document model fits nested comments, 3) Eventual consistency acceptable per requirements, 4) Single-digit millisecond latency. PostgreSQL would struggle at 10K reads/sec without heavy caching.",
        "key_considerations": [
            "Read/write ratio",
            "Data structure (nested documents)",
            "Consistency requirements",
            "Scale requirements"
        ],
        "limitations": "DynamoDB cons: Higher cost at scale, Limited query flexibility (no JOINs), Eventual consistency could show stale data"
    },
    {
        "id": "cache-selection-1",
        "category": "Caching Strategy",
        "question": "Your API serves product catalog data (100K products, each ~5KB). Read pattern: 80% requests for top 1000 products, updates happen every 5 minutes. What caching strategy would you use?",
        "options": [
            {"id": "a", "text": "Redis with TTL of 5 minutes for all products"},
            {"id": "b", "text": "CDN edge caching with 1 hour TTL"},
            {"id": "c", "text": "In-memory LRU cache (application level) with 10 minute TTL"},
            {"id": "d", "text": "No caching, optimize database queries instead"}
        ],
        "correct_answer": "c",
        "explanation": "In-memory LRU cache is optimal because: 1) Sub-millisecond latency for cache hits, 2) LRU naturally keeps hot items (top 1000 products), 3) 10min TTL balances freshness with cache effectiveness, 4) No network hop to external cache. CDN works for static content but not ideal for frequently updated catalogs.",
        "key_considerations": [
            "Access pattern (80/20 rule)",
            "Update frequency",
            "Latency requirements",
            "Cache invalidation complexity"
        ],
        "limitations": "In-memory cache: Limited by server RAM, Not shared across instances (need Redis for multi-server), Lost on restart"
    },
    {
        "id": "queue-selection-1",
        "category": "Message Queue",
        "question": "You need to process 50K order confirmations per minute with strict ordering per customer. Failed messages must be retried up to 3 times. Which queue system fits best?",
        "options": [
            {"id": "a", "text": "Amazon SQS Standard Queue"},
            {"id": "b", "text": "Amazon SQS FIFO Queue"},
            {"id": "c", "text": "Amazon Kinesis Data Streams"},
            {"id": "d", "text": "Apache Kafka"}
        ],
        "correct_answer": "b",
        "explanation": "SQS FIFO Queue is the right choice because: 1) Guarantees strict ordering within message group (per customer), 2) Built-in deduplication, 3) Retry logic with Dead Letter Queue support, 4) Scales to 3000 messages/sec per FIFO queue (can use multiple queues). Kinesis/Kafka are overkill for this use case and require custom retry logic.",
        "key_considerations": [
            "Ordering requirements (per customer)",
            "Throughput needs (50K/min = ~830/sec, well within FIFO limits)",
            "Retry mechanism",
            "Simplicity vs features"
        ],
        "limitations": "FIFO Queue: 3000 msg/sec limit per queue (use multiple queues with sharding if needed), Higher latency than Standard Queue (~ms vs ~100ms)"
    },
    {
        "id": "storage-selection-1",
        "category": "Object Storage",
        "question": "Your video platform needs to store user uploads (avg 500MB per video, 1M videos/month). Videos accessed frequently in first week, rarely after 30 days. What storage strategy minimizes cost?",
        "options": [
            {"id": "a", "text": "S3 Standard for all videos"},
            {"id": "b", "text": "S3 Intelligent-Tiering with lifecycle policies"},
            {"id": "c", "text": "S3 Standard + lifecycle transition to S3 Glacier after 30 days"},
            {"id": "d", "text": "EBS volumes with snapshots"}
        ],
        "correct_answer": "b",
        "explanation": "S3 Intelligent-Tiering is optimal because: 1) Automatically moves objects between access tiers based on usage patterns, 2) No retrieval fees (unlike Glacier), 3) Perfect for unpredictable access patterns, 4) Minimal operational overhead. Option C works but has retrieval delays and costs for Glacier access.",
        "key_considerations": [
            "Access patterns over time",
            "Cost optimization (storage vs retrieval)",
            "Retrieval latency requirements",
            "Operational complexity"
        ],
        "limitations": "Intelligent-Tiering: Small monthly monitoring fee per object, Not cost-effective for objects <128KB, 30-day minimum before automatic archival"
    },
    {
        "id": "consistency-selection-1",
        "category": "Consistency Model",
        "question": "Banking app transfers money between accounts. Requirements: No double-spending, both accounts must update atomically, can tolerate 100ms latency. What consistency model is required?",
        "options": [
            {"id": "a", "text": "Eventual consistency with conflict resolution"},
            {"id": "b", "text": "Strong consistency with ACID transactions"},
            {"id": "c", "text": "Causal consistency"},
            {"id": "d", "text": "Read-your-writes consistency"}
        ],
        "correct_answer": "b",
        "explanation": "Strong consistency with ACID is mandatory because: 1) Financial transactions require atomic updates (both accounts or neither), 2) No tolerance for temporary inconsistency (no double-spending), 3) Isolation prevents race conditions, 4) 100ms latency budget allows for synchronous writes. Eventual consistency would allow temporary double-spending.",
        "key_considerations": [
            "Financial correctness requirements",
            "Atomicity needs",
            "Latency budget",
            "Regulatory compliance"
        ],
        "limitations": "Strong consistency: Lower throughput, Higher latency, Reduced availability during partitions (CAP theorem trade-off)"
    },
    {
        "id": "cdn-selection-1",
        "category": "Content Delivery",
        "question": "Static website with global users (40% US, 30% EU, 30% Asia). 500GB of images, videos, CSS/JS. Pages update weekly. What CDN strategy works best?",
        "options": [
            {"id": "a", "text": "Single origin server in US with aggressive browser caching"},
            {"id": "b", "text": "CloudFront with S3 origin, TTL of 7 days"},
            {"id": "c", "text": "CloudFront with regional S3 buckets as origins"},
            {"id": "d", "text": "Multi-region load balancer without CDN"}
        ],
        "correct_answer": "b",
        "explanation": "CloudFront with S3 origin is ideal because: 1) Edge locations cache content near users globally, 2) S3 provides durable, scalable origin storage, 3) 7-day TTL matches update frequency, 4) Simple architecture, cost-effective. Option C adds unnecessary complexity for static content.",
        "key_considerations": [
            "Global distribution needs",
            "Update frequency (weekly = long TTL acceptable)",
            "Cost (data transfer, storage)",
            "Simplicity"
        ],
        "limitations": "CDN: Stale content during TTL (use cache invalidation for urgent updates), Costs for frequent invalidations, Cold start latency for unpopular content"
    },
    {
        "id": "search-selection-1",
        "category": "Search Technology",
        "question": "E-commerce site needs full-text search across 10M products with faceted filtering (category, price, brand), autocomplete, and typo tolerance. Which technology fits?",
        "options": [
            {"id": "a", "text": "PostgreSQL with LIKE queries"},
            {"id": "b", "text": "DynamoDB with scan operations"},
            {"id": "c", "text": "OpenSearch (Elasticsearch)"},
            {"id": "d", "text": "Redis with sorted sets"}
        ],
        "correct_answer": "c",
        "explanation": "OpenSearch is purpose-built for this because: 1) Full-text search with relevance ranking, 2) Faceted filtering (aggregations), 3) Built-in autocomplete and fuzzy matching, 4) Horizontal scaling for 10M+ documents. PostgreSQL full-text search doesn't scale well beyond millions of rows.",
        "key_considerations": [
            "Full-text search capabilities",
            "Faceted filtering requirements",
            "Scale (10M products)",
            "Typo tolerance (fuzzy matching)"
        ],
        "limitations": "OpenSearch: Higher operational complexity, Memory-intensive, Eventual consistency (index lag), Higher cost than relational DB"
    },
    {
        "id": "realtime-selection-1",
        "category": "Real-Time Communication",
        "question": "Building a live dashboard showing order metrics updated every second. 5000 concurrent users watching. What real-time tech would you use?",
        "options": [
            {"id": "a", "text": "Short polling (1 second interval)"},
            {"id": "b", "text": "Long polling"},
            {"id": "c", "text": "WebSockets"},
            {"id": "d", "text": "Server-Sent Events (SSE)"}
        ],
        "correct_answer": "d",
        "explanation": "Server-Sent Events is optimal because: 1) One-way server-to-client push (perfect for dashboard), 2) Automatic reconnection, 3) Lower overhead than WebSockets for unidirectional data, 4) Works over HTTP (easier through firewalls). WebSockets is overkill for one-way data flow.",
        "key_considerations": [
            "Data flow direction (server to client only)",
            "Connection overhead",
            "Browser support",
            "Simplicity"
        ],
        "limitations": "SSE: One-way only (can't send from client), Browser connection limits (6 per domain), Less browser support than WebSockets"
    },
    {
        "id": "auth-selection-1",
        "category": "Authentication",
        "question": "Mobile app + web app need authentication. Sessions last 30 days, support multiple devices, need to revoke tokens. What auth approach?",
        "options": [
            {"id": "a", "text": "JWT tokens stored in localStorage"},
            {"id": "b", "text": "Session cookies with server-side session store"},
            {"id": "c", "text": "JWT with refresh tokens + Redis blacklist"},
            {"id": "d", "text": "API keys with rate limiting"}
        ],
        "correct_answer": "c",
        "explanation": "JWT with refresh tokens + Redis blacklist is ideal because: 1) Stateless JWTs reduce DB load, 2) Short-lived access tokens (15min) limit exposure, 3) Long-lived refresh tokens (30 days) for good UX, 4) Redis blacklist enables token revocation, 5) Works seamlessly for mobile + web. Session cookies don't work well with mobile apps.",
        "key_considerations": [
            "Multi-platform support (mobile + web)",
            "Revocation needs",
            "Scalability (stateless preferred)",
            "Security (short-lived tokens)"
        ],
        "limitations": "JWT approach: Cannot revoke JWTs without blacklist, Larger payload than session IDs, Need to handle refresh token rotation for security"
    },
    {
        "id": "batch-processing-1",
        "category": "Batch Processing",
        "question": "Generate daily sales reports from 50GB of transaction data. Reports take 2 hours to compute, must be ready by 8am daily. What processing approach?",
        "options": [
            {"id": "a", "text": "Lambda function triggered at 6am"},
            {"id": "b", "text": "Scheduled Fargate task with Step Functions"},
            {"id": "c", "text": "EMR Spark job scheduled with EventBridge"},
            {"id": "d", "text": "EC2 cron job"}
        ],
        "correct_answer": "c",
        "explanation": "EMR Spark job is optimal because: 1) Designed for large dataset processing (50GB), 2) Distributed computing reduces 2hr runtime significantly, 3) Cost-effective (pay only during job), 4) EventBridge provides reliable scheduling. Lambda has 15min timeout. Fargate works but less efficient than Spark for large data.",
        "key_considerations": [
            "Data volume (50GB)",
            "Processing time (2 hours)",
            "Cost optimization",
            "Scheduling reliability"
        ],
        "limitations": "EMR: Higher cold start time (5-10min to provision cluster), More complex setup, Minimum billing increments (per-second after 1 min)"
    },
    {
        "id": "rate-limiting-1",
        "category": "Rate Limiting",
        "question": "API needs rate limiting: 100 requests/min per user, 10K requests/min globally. Distributed across 20 servers. What rate limiting approach?",
        "options": [
            {"id": "a", "text": "In-memory counter per server (5K req/min per server)"},
            {"id": "b", "text": "Redis with sliding window counter"},
            {"id": "c", "text": "DynamoDB with conditional writes"},
            {"id": "d", "text": "API Gateway throttling"}
        ],
        "correct_answer": "b",
        "explanation": "Redis with sliding window is optimal because: 1) Centralized state across all 20 servers, 2) Sub-millisecond latency for counter operations, 3) Sliding window provides accurate rate limiting, 4) Scales to high throughput. In-memory counters per server can't enforce global limit. API Gateway throttling works but less flexible.",
        "key_considerations": [
            "Distributed enforcement (20 servers)",
            "Per-user and global limits",
            "Accuracy vs performance trade-off",
            "Latency impact"
        ],
        "limitations": "Redis rate limiting: Single point of failure (use Redis Cluster for HA), Network latency to Redis, Memory usage for tracking many users"
    },
    {
        "id": "data-partition-1",
        "category": "Data Partitioning",
        "question": "Multi-tenant SaaS app with 10K customers, largest customer has 10M records. Need to query by tenant_id efficiently. What partitioning strategy?",
        "options": [
            {"id": "a", "text": "Partition by tenant_id (one partition per tenant)"},
            {"id": "b", "text": "Partition by date"},
            {"id": "c", "text": "Partition by hash(tenant_id) with 100 partitions"},
            {"id": "d", "text": "No partitioning, just index on tenant_id"}
        ],
        "correct_answer": "c",
        "explanation": "Hash partitioning with 100 partitions is best because: 1) Distributes large tenants across multiple partitions (avoids hot partitions), 2) Queries by tenant_id efficiently routed, 3) Better load balancing than one-partition-per-tenant, 4) Scales as tenants grow. Pure tenant_id partitioning creates unbalanced partitions (small vs large tenants).",
        "key_considerations": [
            "Tenant size variance (some huge, many small)",
            "Query pattern (always by tenant_id)",
            "Hot partition avoidance",
            "Future scalability"
        ],
        "limitations": "Hash partitioning: Cross-tenant queries are inefficient, Need to maintain hash function consistency, Rebalancing on partition count change is complex"
    },
    {
        "id": "async-processing-1",
        "category": "Async Processing",
        "question": "User uploads CSV (1M rows), needs to validate + insert into DB. User expects confirmation email when done (takes 5 min). How to handle?",
        "options": [
            {"id": "a", "text": "Synchronous API call, user waits 5 minutes"},
            {"id": "b", "text": "Lambda async invocation with SNS notification"},
            {"id": "c", "text": "SQS queue + worker + SNS for email"},
            {"id": "d", "text": "Step Functions workflow"}
        ],
        "correct_answer": "c",
        "explanation": "SQS queue + worker + SNS is optimal because: 1) API responds immediately with job_id, 2) SQS provides durable job queue, 3) Workers process uploads asynchronously, 4) SNS sends email on completion, 5) Can scale workers based on queue depth. Lambda has 15min timeout (might not be enough for 1M rows). Step Functions works but more complex.",
        "key_considerations": [
            "Processing time (5 minutes)",
            "User experience (don't block)",
            "Reliability (durable queue)",
            "Notification mechanism"
        ],
        "limitations": "Async pattern: More complex than synchronous, Need job status tracking, User must wait for email (can't see results immediately)"
    },
    {
        "id": "caching-invalidation-1",
        "category": "Cache Invalidation",
        "question": "Product prices update every 30 seconds. Cached in Redis (1 min TTL). Need to ensure users never see prices >30 sec old. What strategy?",
        "options": [
            {"id": "a", "text": "Reduce Redis TTL to 30 seconds"},
            {"id": "b", "text": "Cache invalidation on price update + 1 min TTL as backup"},
            {"id": "c", "text": "Pub/Sub notification to invalidate cache entries"},
            {"id": "d", "text": "No caching, optimize database queries"}
        ],
        "correct_answer": "b",
        "explanation": "Active invalidation + TTL backup is best because: 1) Invalidate cache on price update (ensures <30sec staleness), 2) 1min TTL catches any missed invalidations, 3) Best of both worlds (freshness + resilience), 4) Cache hit ratio remains high. Option A alone doesn't guarantee 30sec freshness if updates happen mid-TTL.",
        "key_considerations": [
            "Staleness requirement (30 seconds)",
            "Cache effectiveness (hit ratio)",
            "Reliability (handle missed invalidations)",
            "Update frequency"
        ],
        "limitations": "Invalidation approach: Race condition (update DB then cache - brief inconsistency), Network delays can cause missed invalidations, Added complexity in update logic"
    },
    {
        "id": "disaster-recovery-1",
        "category": "Disaster Recovery",
        "question": "Financial app requires 99.99% availability, RPO of 1 hour, RTO of 15 minutes. What DR strategy?",
        "options": [
            {"id": "a", "text": "Daily database backups to S3"},
            {"id": "b", "text": "Multi-AZ deployment within single region"},
            {"id": "c", "text": "Multi-region active-passive with hourly snapshots"},
            {"id": "d", "text": "Multi-region active-active"}
        ],
        "correct_answer": "c",
        "explanation": "Multi-region active-passive with hourly snapshots meets requirements because: 1) RTO 15min: passive region can activate quickly, 2) RPO 1hr: hourly snapshots acceptable, 3) 99.99% availability: region failure doesn't cause outage, 4) Cost-effective vs active-active. Multi-AZ only protects against AZ failure, not region failure.",
        "key_considerations": [
            "Availability requirement (99.99% = 52min downtime/year)",
            "RPO (data loss tolerance)",
            "RTO (recovery time)",
            "Cost vs reliability trade-off"
        ],
        "limitations": "Active-passive: Passive region costs (underutilized resources), 15min RTO requires automation and testing, Cross-region data transfer costs, Complexity in failover orchestration"
    },
    {
        "id": "monitoring-selection-1",
        "category": "Observability",
        "question": "Microservices app (20 services) needs to trace requests across services, identify slow endpoints. What observability stack?",
        "options": [
            {"id": "a", "text": "CloudWatch Logs only"},
            {"id": "b", "text": "CloudWatch Logs + Metrics + Alarms"},
            {"id": "c", "text": "CloudWatch + X-Ray for distributed tracing"},
            {"id": "d", "text": "Prometheus + Grafana + Jaeger"}
        ],
        "correct_answer": "c",
        "explanation": "CloudWatch + X-Ray is optimal for AWS because: 1) X-Ray provides distributed tracing across services, 2) Service map visualizes dependencies, 3) Trace analysis identifies slow endpoints, 4) Integrates with CloudWatch for unified monitoring, 5) Low operational overhead. Prometheus/Grafana/Jaeger works but higher operational cost.",
        "key_considerations": [
            "Distributed tracing needs",
            "Service dependency mapping",
            "Performance bottleneck identification",
            "Operational overhead"
        ],
        "limitations": "X-Ray: Requires code instrumentation, Adds latency (~ms per request), Sampling may miss rare issues, Cost scales with request volume"
    },
    {
        "id": "file-upload-1",
        "category": "File Upload",
        "question": "Users upload videos (100MB-2GB each). Need to show upload progress, resume failed uploads. What upload strategy?",
        "options": [
            {"id": "a", "text": "POST to API server, stream to S3"},
            {"id": "b", "text": "Presigned URL for direct S3 upload (single PUT)"},
            {"id": "c", "text": "S3 multipart upload with presigned URLs"},
            {"id": "d", "text": "Upload to CloudFront with origin as S3"}
        ],
        "correct_answer": "c",
        "explanation": "S3 multipart upload is ideal because: 1) Splits large files into chunks (5MB each), 2) Chunks upload in parallel (faster), 3) Resume failed uploads (only retry failed chunks), 4) Progress tracking (report chunks completed), 5) Direct to S3 (no API server bottleneck). Single PUT doesn't support resume.",
        "key_considerations": [
            "File size (100MB-2GB)",
            "Resume capability",
            "Progress tracking",
            "Upload speed (parallelization)"
        ],
        "limitations": "Multipart upload: More complex client code, Need to clean up incomplete multipart uploads (S3 lifecycle policy), Minimum chunk size 5MB (except last chunk)"
    },
    {
        "id": "api-versioning-1",
        "category": "API Design",
        "question": "REST API with 10K mobile clients. Need to introduce breaking changes while supporting old clients for 6 months. What versioning strategy?",
        "options": [
            {"id": "a", "text": "URI versioning (/v1/users, /v2/users)"},
            {"id": "b", "text": "Header versioning (Accept: application/vnd.api.v1+json)"},
            {"id": "c", "text": "Query parameter (?version=1)"},
            {"id": "d", "text": "No versioning, only additive changes"}
        ],
        "correct_answer": "a",
        "explanation": "URI versioning is best because: 1) Clear and explicit (easy to see version in URL), 2) Works with all clients (no special headers), 3) Easy to route to different codebases, 4) Can deprecate /v1 after 6 months, 5) Most widely adopted pattern. Header versioning works but harder to test/debug.",
        "key_considerations": [
            "Breaking changes required",
            "Client upgrade timeline (6 months)",
            "Clarity and discoverability",
            "Deprecation strategy"
        ],
        "limitations": "URI versioning: URL duplication, Multiple versions to maintain, Hard to version individual endpoints differently, Cache keys include version"
    },
    {
        "id": "idempotency-1",
        "category": "Idempotency",
        "question": "Payment API must prevent duplicate charges if client retries due to network timeout. Request contains amount, currency, customer_id. How to ensure idempotency?",
        "options": [
            {"id": "a", "text": "Check if payment already exists for customer_id"},
            {"id": "b", "text": "Client generates idempotency key, store in DB before processing"},
            {"id": "c", "text": "Use database transaction with isolation level"},
            {"id": "d", "text": "Distributed lock on customer_id"}
        ],
        "correct_answer": "b",
        "explanation": "Idempotency key is the standard pattern because: 1) Client generates unique key (UUID) per logical operation, 2) Server checks if key exists in DB before processing, 3) If exists, return cached response, 4) If not, process payment and store key + response, 5) Handles retries, network issues, crashes. Option A doesn't work (customer can make multiple legitimate payments).",
        "key_considerations": [
            "Prevent duplicate charges (financial correctness)",
            "Handle network retries",
            "Client vs server responsibility",
            "Storage of idempotency keys"
        ],
        "limitations": "Idempotency keys: Need to store keys (storage cost), TTL management (how long to keep keys), Client must generate and resend same key on retry"
    },
    {
        "id": "geo-replication-1",
        "category": "Geo-Replication",
        "question": "Global e-commerce app. US users and EU users (GDPR requires EU data stay in EU). Need fast reads globally. What architecture?",
        "options": [
            {"id": "a", "text": "Single database in US with read replicas in EU"},
            {"id": "b", "text": "DynamoDB Global Tables with replication"},
            {"id": "c", "text": "Separate databases per region (US DB, EU DB)"},
            {"id": "d", "text": "Aurora Global Database"}
        ],
        "correct_answer": "c",
        "explanation": "Separate databases per region is required because: 1) GDPR compliance - EU data cannot leave EU, 2) Data sovereignty requirements, 3) Fast local reads (no cross-region latency), 4) Clear data isolation. Global Tables and Aurora Global replicate across regions (violates GDPR). Option A stores EU data in US (non-compliant).",
        "key_considerations": [
            "Regulatory compliance (GDPR)",
            "Data sovereignty",
            "Read latency",
            "Operational complexity"
        ],
        "limitations": "Regional isolation: Cannot query across regions (need separate systems), User must be associated with region, Cross-border scenarios are complex (user moves countries)"
    },
    {
        "id": "connection-pooling-1",
        "category": "Connection Management",
        "question": "Lambda functions connecting to RDS PostgreSQL. Getting 'too many connections' errors during traffic spikes (1K concurrent Lambdas). Database max_connections=100. What solution?",
        "options": [
            {"id": "a", "text": "Increase max_connections to 1000"},
            {"id": "b", "text": "Use RDS Proxy for connection pooling"},
            {"id": "c", "text": "Reduce Lambda concurrency to 100"},
            {"id": "d", "text": "Switch to Aurora Serverless"}
        ],
        "correct_answer": "b",
        "explanation": "RDS Proxy is designed for this because: 1) Pools connections from many Lambdas to fewer DB connections, 2) Handles Lambda's connection lifecycle (creates/destroys rapidly), 3) Reduces DB connection overhead, 4) Improves failover time. Increasing max_connections helps but doesn't scale (1K connections kill DB performance).",
        "key_considerations": [
            "Lambda connection patterns (burst, short-lived)",
            "Database connection limits",
            "Performance (too many connections degrade DB)",
            "Serverless architecture best practices"
        ],
        "limitations": "RDS Proxy: Added latency (~1ms), Additional cost, Only works with MySQL/PostgreSQL, Doesn't solve slow queries"
    },
    {
        "id": "secret-management-1",
        "category": "Security",
        "question": "Application needs database password, API keys for 3rd party services. Keys rotate monthly. How to manage secrets securely?",
        "options": [
            {"id": "a", "text": "Environment variables in application code"},
            {"id": "b", "text": "AWS Systems Manager Parameter Store"},
            {"id": "c", "text": "AWS Secrets Manager with automatic rotation"},
            {"id": "d", "text": "Encrypted file in S3"}
        ],
        "correct_answer": "c",
        "explanation": "Secrets Manager is optimal because: 1) Automatic rotation (scheduled monthly), 2) Encryption at rest (KMS), 3) Fine-grained access control (IAM), 4) Audit logging (who accessed what when), 5) Integration with RDS for DB passwords. Parameter Store doesn't have built-in rotation. Environment variables expose secrets in logs/config.",
        "key_considerations": [
            "Rotation requirements (monthly)",
            "Encryption and access control",
            "Audit trail",
            "Automation vs manual management"
        ],
        "limitations": "Secrets Manager: Higher cost than Parameter Store, API calls for each secret retrieval (cache locally), Rotation requires Lambda function for custom secrets"
    },
    {
        "id": "blue-green-deployment-1",
        "category": "Deployment Strategy",
        "question": "Deploying API update to production. Need zero downtime, quick rollback if issues detected. 10K requests/second. What deployment strategy?",
        "options": [
            {"id": "a", "text": "In-place deployment with health checks"},
            {"id": "b", "text": "Blue-green deployment with instant traffic switch"},
            {"id": "c", "text": "Canary deployment (10% -> 50% -> 100% over 1 hour)"},
            {"id": "d", "text": "Rolling deployment (10 instances at a time)"}
        ],
        "correct_answer": "c",
        "explanation": "Canary deployment is safest because: 1) Gradually increases traffic to new version (10% -> 50% -> 100%), 2) Monitors error rates at each stage, 3) Auto-rollback if errors spike, 4) Limits blast radius (only 10% impacted initially), 5) Production validation with real traffic. Blue-green switches all traffic at once (higher risk). Rolling is slow and harder to rollback.",
        "key_considerations": [
            "Zero downtime requirement",
            "Risk mitigation (gradual rollout)",
            "Rollback speed",
            "Production validation"
        ],
        "limitations": "Canary: Longer deployment time (1 hour), More complex automation, Need good monitoring/metrics, Stateful apps are harder (session stickiness)"
    },
    {
        "id": "cost-optimization-1",
        "category": "Cost Optimization",
        "question": "Batch job runs nightly (2-4 hours), processes 100GB data. Currently using on-demand EC2 c5.9xlarge ($1.53/hr). How to reduce cost by 70%?",
        "options": [
            {"id": "a", "text": "Switch to Reserved Instances (1 year commitment)"},
            {"id": "b", "text": "Switch to Spot Instances with fallback to on-demand"},
            {"id": "c", "text": "Switch to Savings Plans"},
            {"id": "d", "text": "Use Lambda instead"}
        ],
        "correct_answer": "b",
        "explanation": "Spot Instances are perfect because: 1) Batch jobs are interruptible (can retry), 2) 70%+ discount vs on-demand, 3) Nightly jobs have flexible timing (can wait for spot capacity), 4) Fallback to on-demand ensures completion. Reserved/Savings Plans save ~40% (not 70%). Lambda has 15min timeout and memory limits.",
        "key_considerations": [
            "Job characteristics (batch, interruptible)",
            "Cost savings target (70%)",
            "Timing flexibility",
            "Fault tolerance"
        ],
        "limitations": "Spot Instances: Can be terminated with 2-min notice, Need spot instance interruption handling, Availability not guaranteed, Must implement checkpointing for long jobs"
    },
    {
        "id": "stream-processing-1",
        "category": "Stream Processing",
        "question": "IoT sensors send 50K events/second. Need real-time analytics (windowed aggregations, 1-minute windows). Store raw data for 7 days. What architecture?",
        "options": [
            {"id": "a", "text": "API Gateway -> Lambda -> DynamoDB"},
            {"id": "b", "text": "Kinesis Data Streams -> Kinesis Analytics -> S3"},
            {"id": "c", "text": "SQS -> Lambda -> RDS"},
            {"id": "d", "text": "Kafka -> Spark Streaming -> Redshift"}
        ],
        "correct_answer": "b",
        "explanation": "Kinesis stack is purpose-built for this because: 1) Data Streams handles 50K events/sec easily, 2) Kinesis Analytics provides SQL for windowed aggregations, 3) Built-in 1-min tumbling windows, 4) S3 for durable 7-day storage, 5) Fully managed, low operational overhead. Kafka+Spark works but higher ops cost. Lambda has concurrency limits.",
        "key_considerations": [
            "Throughput (50K events/sec)",
            "Real-time analytics needs",
            "Window aggregations",
            "Retention period (7 days)"
        ],
        "limitations": "Kinesis: 1MB/sec per shard limit (need ~50 shards), Kinesis Analytics SQL is limited vs full programming, Higher cost than self-managed Kafka, 7-day max retention in Kinesis (must archive to S3)"
    },
    {
        "id": "schema-evolution-1",
        "category": "Schema Design",
        "question": "Event-driven system with 20 microservices. Events published to SNS. New field added to event schema - old consumers should not break. What schema strategy?",
        "options": [
            {"id": "a", "text": "JSON with optional new fields (additive changes only)"},
            {"id": "b", "text": "Protocol Buffers with schema registry"},
            {"id": "c", "text": "Avro with schema registry"},
            {"id": "d", "text": "GraphQL subscriptions"}
        ],
        "correct_answer": "a",
        "explanation": "JSON with additive-only changes is simplest because: 1) Old consumers ignore unknown fields (backward compatible), 2) New consumers can use new fields, 3) No schema registry overhead for simple use case, 4) Works with SNS natively. Protobuf/Avro are overkill unless extreme performance/size needs. Key principle: never remove fields, only add optional fields.",
        "key_considerations": [
            "Backward compatibility (old consumers must work)",
            "Microservices independence",
            "Operational simplicity",
            "Schema evolution patterns"
        ],
        "limitations": "JSON additive: Discipline required (no breaking changes), No compile-time validation, Larger payload than binary formats (Protobuf/Avro), Typos not caught until runtime"
    },
    {
        "id": "data-lake-1",
        "category": "Data Architecture",
        "question": "Company needs to store raw logs from 50 services (1TB/day), enable ad-hoc queries by data analysts, and feed ML models. What data architecture?",
        "options": [
            {"id": "a", "text": "Store everything in RDS PostgreSQL"},
            {"id": "b", "text": "S3 data lake + Athena for queries + SageMaker for ML"},
            {"id": "c", "text": "DynamoDB for storage + OpenSearch for queries"},
            {"id": "d", "text": "Redshift for everything"}
        ],
        "correct_answer": "b",
        "explanation": "S3 data lake is optimal because: 1) Cheapest storage for 1TB/day (~$23/month in S3 vs $115/day in RDS), 2) Athena for ad-hoc SQL queries on S3, 3) SageMaker reads from S3 for ML, 4) Decouple storage from compute, 5) Schema-on-read flexibility. Redshift works but expensive for raw data storage.",
        "key_considerations": [
            "Volume (1TB/day = 365TB/year)",
            "Query patterns (ad-hoc, not transactional)",
            "ML integration",
            "Cost at scale"
        ],
        "limitations": "Data lake: Query latency higher than dedicated DB (seconds vs milliseconds), Need data cataloging (AWS Glue), Schema management is manual, ETL complexity for structured analysis"
    },
    {
        "id": "circuit-breaker-1",
        "category": "Resilience Pattern",
        "question": "Microservice A calls Service B (payment processor). When B is down, A should fail fast rather than timing out (30 sec) on each request. What pattern?",
        "options": [
            {"id": "a", "text": "Retry with exponential backoff"},
            {"id": "b", "text": "Circuit breaker pattern"},
            {"id": "c", "text": "Request timeout reduction (30s -> 1s)"},
            {"id": "d", "text": "Load balancer health checks"}
        ],
        "correct_answer": "b",
        "explanation": "Circuit breaker is designed for this because: 1) Detects failure threshold (e.g., 5 failures), 2) Opens circuit (fails fast, no calls to B), 3) After timeout, half-opens (test 1 request), 4) Closes if successful (resume normal), 5) Prevents cascading failures. Timeout reduction helps but still wastes 1s per request. Retry makes problem worse.",
        "key_considerations": [
            "Fail fast (don't wait 30s)",
            "Prevent cascading failures",
            "Automatic recovery detection",
            "User experience during downstream outage"
        ],
        "limitations": "Circuit breaker: Needs tuning (failure threshold, timeout), False positives (temporary glitches trip circuit), All requests fail during open state (can't differentiate), Added complexity"
    }
]
