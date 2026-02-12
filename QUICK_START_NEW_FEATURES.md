# Quick Start: New Features Guide

## What's New? 🚀

Your System Design Reference app just got **5 major upgrades** based on Hello Interview's proven interview framework.

## 1. Click "📚 Reference" Button

Located in the header, next to "💡 Scenarios"

### Four Tabs:

#### 📊 Numbers to Know
- **L1 cache**: 0.5ns
- **RAM**: 100ns
- **SSD**: 150μs
- **Network (datacenter)**: 0.5ms
- **Network (SF→NYC)**: 40ms
- Plus throughput, capacity, storage, availability metrics

**Use Case**: "With 100ns RAM access and 10GB/s bandwidth, we can serve 100M reads/sec from memory"

---

#### 🎯 Delivery Framework
45-minute interview structure:

1. **Requirements** (5-10 min) → Clarify functional/non-functional
2. **High-Level Design** (10-15 min) → System diagram + components
3. **Deep Dives** (15-20 min) → Schema, scaling, caching, failures
4. **Wrap-Up** (5 min) → Alternatives, trade-offs

**Use Case**: Stay on track during interview, don't waste time

---

#### 📋 Assessment Rubric
How interviewers evaluate you:

- **Problem Navigation** (30%) - Did you break down the problem well?
- **Solution Design** (30%) - Is your architecture sound?
- **Technical Excellence** (25%) - Right tech choices?
- **Communication** (15%) - Clear explanations?

Plus: Mid-Level vs Senior vs Staff+ expectations

**Use Case**: Know what interviewers are looking for at each level

---

#### 🔧 Common Patterns
7 patterns that appear in almost every interview:

1. **Real-Time Updates** - WebSockets, SSE, Long Polling
2. **Contention** - Optimistic locking, distributed locks, queues
3. **Multi-Step Processes** - Sagas, 2PC, Outbox pattern
4. **Scaling Reads** - Caching, replicas, CDN, indexes
5. **Scaling Writes** - Sharding, WAL, queues, batching
6. **Large Blobs** - Presigned URLs, multipart upload, streaming
7. **Long-Running Tasks** - Job queues, orchestration, status tracking

**Use Case**: "This needs real-time updates → Use WebSockets with Redis pub/sub"

---

## 2. New Scenarios (Click "💡 Scenarios")

### 🚦 Rate Limiter
- Fixed vs sliding window
- Redis atomic operations
- Distributed rate limiting
- **Scale**: 100K+ requests/sec

### 📱 WhatsApp
- Real-time messaging at 2B users
- Offline message delivery
- WebSocket fan-out + Redis pub/sub
- **Scale**: 100 billion messages/day

### ▶️ YouTube
- Video transcoding with MediaConvert
- Adaptive streaming (HLS)
- CDN distribution
- **Scale**: 500 hours uploaded/minute

---

## Quick Reference Cheat Sheet

### When to Use What

| Problem | Pattern | Technologies |
|---------|---------|-------------|
| Real-time chat | Real-Time Updates | WebSockets + Redis pub/sub |
| Ticket sales | Dealing with Contention | Pessimistic locking + distributed locks |
| E-commerce checkout | Multi-Step Processes | Saga (orchestration) |
| Social media feed | Scaling Reads | CDN → Cache → Read Replicas |
| IoT data ingestion | Scaling Writes | Kinesis → Lambda → Time-series DB |
| Video upload | Handling Large Blobs | Presigned URLs + Multipart upload + S3 |
| Data export | Long-Running Tasks | SQS + Lambda + Status tracking |

### Essential Numbers

| Operation | Latency | Throughput |
|-----------|---------|------------|
| L1 cache | 0.5 ns | 100 GB/s |
| RAM | 100 ns | 10 GB/s |
| SSD read | 150 μs | 500 MB/s |
| Network (datacenter) | 0.5 ms | 1.25 GB/s (10 Gbps) |
| Network (cross-region) | 40-150 ms | - |

### Capacity Rules of Thumb

- QPS per server: **10K-50K** (simple CRUD)
- Redis ops: **100K+** per instance
- DB connections: **100-500** per instance
- WebSocket connections: **10K-100K** per server
- CDN cache hit ratio: **90%+** target

### Availability Targets

- **99.9%** (three nines) → 8.77 hours downtime/year
- **99.99%** (four nines) → 52.6 minutes downtime/year
- **99.999%** (five nines) → 5.26 minutes downtime/year

---

## Interview Day Workflow

### 30 Minutes Before Interview

1. Open app → Click "📚 Reference"
2. Review **Numbers to Know** (5 min)
3. Refresh **Delivery Framework** (5 min)
4. Skim **Common Patterns** (5 min)

### During Interview

1. **Requirements phase**: Reference Framework → Phase 1 questions
2. **Design phase**: Check relevant Pattern (e.g., "Scaling Reads")
3. **Capacity estimation**: Use Numbers (e.g., "10K QPS per server")
4. **Trade-offs**: Reference Pattern pros/cons

### After Interview

Review **Assessment Rubric** → Identify improvement areas for next time

---

## Example: Using New Features Together

**Interview Question**: "Design Instagram"

1. **Check Scenario** → "Feed" scenario (similar to Instagram)
2. **Open Framework** → Follow 4-phase structure
3. **Reference Patterns** → "Scaling Reads" (feed), "Handling Large Blobs" (photos)
4. **Use Numbers** → "With 100M DAU, 50 posts/day viewed = 5B reads/day = 57K QPS. Need 6 servers at 10K QPS each"
5. **Check Rubric** → Ensure covering all 4 competencies

---

## Pro Tips

### Numbers to Know
- Memorize before interview
- Use for capacity estimation credibility
- Reference during "How would you scale this?" questions

### Delivery Framework
- Timebox each phase strictly
- Ask clarifying questions in Phase 1 (don't assume)
- Leave time for Deep Dives (Phase 3)

### Assessment Rubric
- Focus on Problem Navigation (30% weight)
- Always discuss trade-offs (Technical Excellence)
- Think out loud (Communication)

### Common Patterns
- Learn when NOT to use each approach
- Mention alternatives ("We could use WebSockets OR Long Polling, but WebSockets is better here because...")
- Connect patterns to real scenarios

---

## Testing the Features

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Open browser: http://localhost:3000
# Click "📚 Reference" button
# Click "💡 Scenarios" → Try Rate Limiter, WhatsApp, YouTube
```

---

## Keyboard Shortcuts (Still Work!)

- `Cmd/Ctrl + K` → Focus search
- `Cmd/Ctrl + F` → Toggle favorites
- `Cmd/Ctrl + I` → Toggle interview/study mode
- `↑` / `↓` → Navigate tools
- `Enter` → Select tool
- `Esc` → Clear/close

---

## What This Doesn't Replace

- **Practice**: Still need to do mock interviews
- **Depth**: Hello Interview has more scenarios (25 vs our 12)
- **Video learning**: Hello Interview has video explanations
- **Guided practice**: Hello Interview has AI tutor

## What This Does Better

- **Speed**: Local, instant access, no internet needed
- **Keyboard-driven**: Navigate without mouse
- **Customizable**: Add your own notes/tools
- **Free**: No subscription required

---

**Ready to crush your interview?** Open the app, click "📚 Reference", and start exploring.

When the interview gets tough, the tough reference and execute flawlessly.
