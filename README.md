# System Design Reference App
<img width="748" height="648" alt="image" src="https://github.com/user-attachments/assets/5ab77b06-340b-4f87-87fb-2d7c10f0fbf4" />

A local FastAPI + Next.js application for quick reference during system design interviews. Features searchable tools, scenario-based suggestions, and keyboard-driven navigation.

## Features

### Core Features

- 🔍 **Full-text search** across technologies and use cases
- 🏷️ **Smart filtering** by category, CAP leaning, and consistency model
- ⌨️ **Keyboard shortcuts** for lightning-fast navigation
- 🎯 **Interview mode** for concise talking points
- 📚 **Deep study mode** with failure modes, tuning gotchas, and more
- ⭐ **Favorites** to pin your most-used tools
- 📋 **Copy answer skeleton** for quick interview prep

### NEW: Reference Library (Based on Hello Interview)

- 📊 **Numbers to Know** - Essential latency, throughput, capacity, and availability metrics
- 🎯 **Delivery Framework** - Structured 4-phase interview approach with time allocation
- 📋 **Assessment Rubric** - Understand how interviewers evaluate candidates (4 competencies)
- 🔧 **Common Patterns** - 7 critical patterns (Real-Time Updates, Contention, Multi-Step Processes, Scaling Reads/Writes, Large Blobs, Long-Running Tasks)

### NEW: Three Learning Modes

#### 🔄 Practice Mode - Learn with Full Context

- 📊 **Mixed Questions** - 70% scenario questions + 30% technology selection questions
- 🔍 **Full Details** - Complete scenario information including requirements, entities, API, architecture
- ⏱ **Configurable Timer** - 15, 30, 45, or 60 minutes with visual warnings
- ✅ **Comprehensive Assessment** - Evaluate yourself against Delivery Framework & Assessment Rubric
- 📈 **Progress Tracking** - Local history of practice sessions with scores and timing
- 🎓 **Technology Deep Dive** - Test your knowledge of when and why to use specific technologies

#### 🎯 Quiz Me - Flashcard Knowledge Testing

- ⚡ **Rapid-Fire Questions** - Quick flashcard-style questions for focused knowledge testing
- 📚 **Four Categories** - Technology (40%), Concepts (30%), Patterns (20%), Numbers (10%)
- ✍️ **Write & Reveal** - Type your answer, then reveal to check against correct answer
- ✓/✗ **Self-Assessment** - Mark yourself correct or incorrect
- 🎲 **Category Filtering** - Focus on specific areas or mix all categories
- ⏱ **Quick Sessions** - 5-20 minute sessions, 5-20 questions
- 📊 **Progress Tracking** - Track correct/incorrect answers and time per question

#### 📝 Test Mode - Interview Simulation

- 🎯 **Blank Canvas** - Design from scratch with minimal information (title, description, scale, hints)
- 🚫 **No Guidance** - You fill in all requirements, entities, API endpoints, and architecture
- 📋 **Structured Fields** - Organized tabs for Requirements, Entities & API, Architecture, Deep Dives, Notes
- ⏱ **Interview Timing** - 30, 45, or 60 minute sessions
- 🔍 **Scenario Selection** - Random or choose specific scenarios (Uber, WhatsApp, Instagram, etc.)
- ✅ **Full Assessment** - Comprehensive evaluation against interview rubric
- 📊 **Comparison View** - Review your design with detailed breakdown
- 💾 **Session History** - Track all test attempts with scores and timing

### Extended Scenario Coverage

- 💳 **Payments** - Strong consistency, idempotency, two-phase commit
- 💬 **Chat** - Real-time messaging with WebSockets
- 📰 **Feed** - Hybrid fan-out, caching strategies
- 📊 **Analytics** - Lambda architecture, streaming analytics
- 🔍 **Search** - Full-text search with OpenSearch
- 🔐 **Auth** - JWT tokens, RBAC, session management
- 🚗 **Uber** - Geospatial matching, real-time location tracking
- 🔗 **Bit.ly** - URL shortening with high read-to-write ratio
- 📦 **Dropbox** - Large file uploads, chunking, presigned URLs
- 🚦 **Rate Limiter** - Distributed rate limiting with Redis
- 📱 **WhatsApp** - Real-time messaging at scale, offline delivery
- ▶️ **YouTube** - Video transcoding, adaptive streaming, CDN

## Prerequisites

- **Python 3.11+**
- **Node 20+**
- **npm** (comes with Node)

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### 2. Frontend Setup

Open a **new terminal window**:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Add Your Data

Place your `system-design-tech-cheatsheet.xlsx` file in the `data/` directory.

If you need to refresh the database after updating the spreadsheet:

```bash
cd backend
python import_data.py --refresh
```

### 4. Understanding the Database Setup

This project uses a **two-database system** for easy collaboration:

#### `starter.db` (Version Controlled)

- Contains all curated scenarios (Uber, Bit.ly, Dropbox, etc.)
- Committed to Git and shared with the team
- Read-only reference point
- **Everyone gets this when they clone the repo**

#### `system_design_ref.db` (Your Working Copy)

- Automatically created from `starter.db` on first run
- This is where you can add your own scenarios and modifications
- **NOT** committed to Git (stays local to your machine)
- Each team member has their own independent copy

#### Resetting Your Database

If you want to get the latest scenarios from the team or start fresh:

```bash
cd backend
rm system_design_ref.db
# Restart the server - it will auto-copy from starter.db
uvicorn main:app --reload --port 8000
```

#### For Maintainers: Updating starter.db

When you want to share new scenarios with the team:

```bash
cd backend
# After adding scenarios to your working database
cp system_design_ref.db starter.db
git add starter.db
git commit -m "Add new scenarios to starter database"
git push
```

## Usage

### Keyboard Shortcuts

| Shortcut       | Action                          |
| -------------- | ------------------------------- |
| `Cmd/Ctrl + K` | Focus search bar                |
| `↑` / `↓`      | Navigate tool list              |
| `Enter`        | Select focused tool             |
| `Esc`          | Clear search / close detail     |
| `Cmd/Ctrl + F` | Toggle favorites view           |
| `Cmd/Ctrl + I` | Toggle interview/study mode     |
| `1-9`          | Jump to category (experimental) |

### Search & Filter

- Type in the search bar to find tools by name, category, or use case
- Use category chips to filter by tool type (DB, Cache, Queue, etc.)
- Toggle CAP leaning (CP, AP, Tunable)
- Select consistency model (Strong, Eventual, Causal, Session)
- Enable "AWS only" to filter cloud-specific services

### Interview Mode vs. Study Mode

- **Interview Mode (🎯)**: Shows concise one-liners, best-for, avoid-when, and key tradeoffs
- **Deep Study Mode (📚)**: Includes everything from interview mode PLUS:
  - Failure modes
  - Multi-region / DR notes
  - Tuning gotchas
  - Observability signals
  - Alternatives
  - Interview prompts

Toggle between modes with `Cmd/Ctrl + I` or the mode switcher in the header.

### Quiz Me Mode

Click **🎯 Quiz Me** in the header to practice with randomized questions:

#### How It Works

1. **Configure Your Quiz**: Choose question count (1, 3, 5) and time limit (15-60 minutes)
2. **Answer Questions**: Mix of scenario-based system design problems and technology selection questions
3. **Self-Assessment**: Evaluate yourself against the Delivery Framework and Assessment Rubric
4. **Track Progress**: Review results, identify areas for improvement, and view quiz history

#### Question Types

**Scenario Questions (70%)**:
- Full system design problems from the 12 scenarios (Uber, WhatsApp, Payments, etc.)
- Document your approach following the Delivery Framework
- Practice end-to-end system design thinking

**Technology Selection Questions (30%)**:
- Multiple choice questions testing when and why to use specific technologies
- Covers databases, caching, queues, storage, consistency models, and more
- Includes explanations for correct answers with key considerations and limitations

#### Self-Assessment Criteria

- **Delivery Framework Alignment**: Requirements, High-Level Design, Deep Dives, Trade-offs
- **Assessment Rubric Competencies**: Problem Navigation, Solution Design, Technical Excellence, Communication
- **Technology-Specific**: Correct tech choice, reasoning, pros/cons, limitations, alternatives

All quiz sessions are saved locally with your scores, timing, and notes for future review.

### Scenario Prompts

Click **💡 Scenarios** in the header to see pre-configured technology stacks for common interview scenarios:

#### Infrastructure Patterns

- **Payments**: DynamoDB, PostgreSQL, SQS, Lambda, Redis - Strong consistency, idempotency
- **Chat**: DynamoDB, ElastiCache, Kinesis, Lambda, CloudFront - Real-time messaging
- **Feed**: DynamoDB, ElastiCache, S3, CloudFront, Lambda - Hybrid fan-out
- **Analytics**: S3, Athena, Redshift, Kinesis, Lambda - Lambda architecture
- **Search**: OpenSearch, DynamoDB, CloudFront, Lambda - Full-text search
- **Auth**: Cognito, DynamoDB, ElastiCache, Lambda, CloudFront - JWT + RBAC

#### Real Systems

- **Uber**: PostgreSQL, Redis, SQS, Lambda, Step Functions - Geospatial matching
- **Bit.ly**: PostgreSQL, Redis, CloudFront, Lambda - URL shortening at scale
- **Dropbox**: S3, DynamoDB, CloudFront, Lambda - Large file handling
- **Rate Limiter** (NEW): Redis, DynamoDB, API Gateway - Distributed rate limiting
- **WhatsApp** (NEW): DynamoDB, Redis, S3, CloudFront, SNS - Messaging at 2B users
- **YouTube** (NEW): S3, MediaConvert, CloudFront, DynamoDB, Kinesis - Video platform

### Reference Library (NEW!)

Click **📚 Reference** in the header to access essential interview preparation material:

#### 📊 Numbers to Know

Memorize these critical metrics for credible capacity estimation:

- **Latency**: L1 cache (0.5ns), RAM (100ns), SSD (150μs), Network cross-region (40-150ms)
- **Throughput**: Memory (10 GB/s), SSD (500 MB/s), 10 Gbps network (1.25 GB/s)
- **Capacity**: QPS per server (10K-50K), Redis ops (100K+), WebSocket connections (10K-100K)
- **Availability**: 99.9% (8.77h downtime/year), 99.99% (52.6min), 99.999% (5.26min)

#### 🎯 Delivery Framework

Structured approach to nail the interview in 45 minutes:

1. **Requirements Gathering** (5-10 min) - Clarify functional/non-functional requirements
2. **High-Level Design** (10-15 min) - Draw system diagram, explain component interactions
3. **Deep Dives** (15-20 min) - Focus on 2-3 critical areas (schema, scaling, caching, failures)
4. **Wrap-Up** (5 min) - Summarize, discuss alternatives, address concerns

#### 📋 Assessment Rubric

Understand how interviewers evaluate you across 4 competencies:

- **Problem Navigation** (30%) - Breaking down ambiguous problems, prioritizing correctly
- **Solution Design** (30%) - Well-structured, scalable architectures
- **Technical Excellence** (25%) - Knowledge of technologies, patterns, trade-offs
- **Communication & Collaboration** (15%) - Clear explanations, working with interviewer

Includes level expectations (Mid-Level, Senior, Staff+) and red/green flags.

#### 🔧 Common Patterns

Master these 7 patterns that appear in almost every system design interview:

1. **Real-Time Updates** - WebSockets, SSE, Long Polling comparison
2. **Dealing with Contention** - Optimistic/pessimistic locking, distributed locks, queues
3. **Multi-Step Processes** - Sagas (choreography vs orchestration), 2PC, Outbox pattern
4. **Scaling Reads** - Caching layers, read replicas, CDN, materialized views
5. **Scaling Writes** - Sharding, WAL, async queues, batch writes, time-series DBs
6. **Handling Large Blobs** - Presigned URLs, multipart upload, CDN, compression, streaming
7. **Managing Long-Running Tasks** - Job queues, workflow orchestration, status tracking

### Favorites

Click the **☆** star icon on any tool card to add it to your favorites. Starred tools appear at the top of your list for quick access.

### Copy Answer Skeleton

In the tool detail view, click **📋 Copy Answer** to copy a formatted answer skeleton to your clipboard. Perfect for preparing quick responses during interviews.

## Project Structure

```
system-design-ref/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── database.py             # Database connection
│   ├── import_data.py          # XLSX importer
│   ├── requirements.txt        # Python dependencies
│   ├── start.sh                # Quick start script
│   └── system_design_ref.db    # SQLite database (generated)
├── frontend/
│   ├── app/                    # Next.js app directory
│   ├── components/             # React components
│   ├── hooks/                  # Custom React hooks
│   ├── lib/                    # API client
│   ├── package.json            # Node dependencies
│   └── start.sh                # Quick start script (optional)
├── data/
│   └── system-design-tech-cheatsheet.xlsx
└── README.md
```

## API Endpoints

### Tools

- `GET /api/tools` - List all tools with optional filters
  - Query params: `category`, `cap_leaning`, `consistency_model`, `aws_only`
- `GET /api/tools/search?q=<query>` - Full-text search
- `GET /api/tools/:id` - Get detailed info for a single tool

### Scenarios

- `GET /api/scenarios/:type` - Get suggested stack for scenario
  - Types: `payments`, `chat`, `feed`, `analytics`, `search`, `auth`

### Favorites

- `GET /api/favorites` - List favorited tools
- `POST /api/favorites/:tool_id` - Add tool to favorites
- `DELETE /api/favorites/:tool_id` - Remove from favorites

### Utility

- `GET /api/categories` - List all available categories

## Updating Data

To update your reference data:

1. Edit `system-design-tech-cheatsheet.xlsx`
2. Ensure it has "Quick Reference" and "Deep Study" sheets
3. Run the importer with refresh flag:
   ```bash
   cd backend
   python import_data.py --refresh
   ```
4. Restart the backend server

## Troubleshooting

### Backend won't start

- Make sure you've activated the virtual environment: `source venv/bin/activate`
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify the database exists: `python import_data.py`

### Frontend won't start

- Make sure you've installed dependencies: `npm install`
- Check Node version: `node --version` (should be 20+)
- Try deleting `node_modules` and `.next` folders, then reinstall

### Database import fails

- Verify the XLSX file exists at `../data/system-design-tech-cheatsheet.xlsx`
- Check that the file has "Quick Reference" and "Deep Study" sheets
- Ensure column headers match expected format (Technology, Category, etc.)

### CORS errors

- Make sure the backend is running on port 8000
- Make sure the frontend is running on port 3000
- Check that both servers are running simultaneously

### Changes not appearing

- For backend changes: restart the FastAPI server
- For frontend changes: refresh the browser (Next.js auto-reloads)
- For data changes: re-run `python import_data.py --refresh`

## Production Build

To create an optimized production build:

```bash
cd frontend
npm run build
npm start
```

The production server will run on port 3000.

## Interview Setup Workflow

For actual interview use:

1. Open two terminal windows
2. **Terminal 1** (Backend):
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --port 8000
   ```
3. **Terminal 2** (Frontend):
   ```bash
   cd frontend
   npm run dev
   ```
4. Open browser to `http://localhost:3000`
5. Position on second monitor (if allowed during interview)
6. Use keyboard shortcuts for fast navigation
7. Switch to interview mode (`Cmd+I`) for concise talking points

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite, openpyxl
- **Frontend**: Next.js 14, React 18, TypeScript
- **Styling**: CSS Modules with CSS custom properties

## What's New (Inspired by Hello Interview)

This version includes major improvements based on the comprehensive [Hello Interview System Design Guide](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction):

✅ **Numbers to Know** - Critical metrics for capacity estimation (latency, throughput, availability)  
✅ **Delivery Framework** - 4-phase structured interview approach with time allocation  
✅ **Assessment Rubric** - Understand interviewer evaluation criteria across 4 competencies  
✅ **Common Patterns** - 7 essential patterns (real-time updates, contention, scaling reads/writes, etc.)  
✅ **3 New Scenarios** - Rate Limiter, WhatsApp, YouTube (brings total to 12 scenarios)

These additions ensure you have both **tactical knowledge** (tools, technologies) and **strategic preparation** (interview structure, assessment criteria, common patterns).

## Future Enhancements

- [ ] Semantic search with embeddings
- [x] "Quiz me" mode for practice (random scenario + timer + self-assessment checklist) ✅
- [ ] Spaced repetition for quiz questions
- [ ] Difficulty levels (Junior, Mid-Level, Senior, Staff+)
- [ ] Export quiz history as PDF/markdown
- [ ] Export favorites as markdown
- [ ] Dark mode
- [ ] Mobile responsive improvements
- [ ] Offline mode with static export
- [ ] More scenarios from Hello Interview (Ticketmaster, Yelp, News Aggregator, etc.)

## License

MIT

---

**Built for crushing system design interviews. Study hard, deploy with confidence, lock and load—because when the pressure's on, you execute flawlessly.**
