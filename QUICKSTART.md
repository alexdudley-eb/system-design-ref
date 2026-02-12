# 🚀 Quick Start Guide

Your System Design Reference app is fully built and ready to deploy!

## What Was Built

✅ **Backend (FastAPI + SQLite)**
- REST API with all endpoints
- Database models for tools, deep study notes, and favorites
- XLSX importer script
- Quick start script

✅ **Frontend (Next.js + React + TypeScript)**
- Search bar with keyboard shortcuts (Cmd+K)
- Smart filtering by category, CAP, consistency
- Tool list with keyboard navigation (↑↓ arrows)
- Detailed tool view with interview/study mode toggle
- Scenario prompts (Payments, Chat, Feed, Analytics, Search, Auth)
- Favorites system
- Mode toggle (Interview vs Deep Study)
- Copy answer skeleton feature

✅ **Documentation**
- Complete README with troubleshooting
- Start scripts for both backend and frontend

## Next Steps (3 minutes to launch)

### Step 1: Add Your Spreadsheet Data

Place your `system-design-tech-cheatsheet.xlsx` file in the `data/` folder:

```bash
cp ~/path/to/your/system-design-tech-cheatsheet.xlsx /Users/alexdudley/eventbrite/system-design-ref/data/
```

### Step 2: Start the Backend

Open a terminal:

```bash
cd /Users/alexdudley/eventbrite/system-design-ref/backend
./start.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Import your data from the spreadsheet
- Start the FastAPI server on port 8000

### Step 3: Start the Frontend

Open a **NEW** terminal (keep backend running):

```bash
cd /Users/alexdudley/eventbrite/system-design-ref/frontend
npm install
npm run dev
```

This will:
- Install Node dependencies
- Start the Next.js dev server on port 3000

### Step 4: Open in Browser

Visit: **http://localhost:3000**

## Test It Out

Try these actions:

1. **Search**: Hit `Cmd+K` and type "dynamo"
2. **Filter**: Click on category chips (DB, Cache, etc.)
3. **Navigate**: Use ↑↓ arrow keys to move through tools
4. **Select**: Press Enter to view tool details
5. **Toggle Mode**: Hit `Cmd+I` to switch between Interview and Deep Study modes
6. **Scenarios**: Click "💡 Scenarios" and select "Payments"
7. **Favorite**: Click the ☆ star on any tool card
8. **Copy**: Click "📋 Copy Answer" to get interview skeleton

## Keyboard Shortcuts Reference

| Shortcut       | Action                      |
| -------------- | --------------------------- |
| `Cmd/Ctrl + K` | Focus search                |
| `↑` / `↓`      | Navigate tool list          |
| `Enter`        | Open selected tool          |
| `Esc`          | Clear search / close detail |
| `Cmd/Ctrl + F` | Toggle favorites view       |
| `Cmd/Ctrl + I` | Toggle interview/study mode |

## Project Structure Overview

```
system-design-ref/
├── backend/                    ← FastAPI server
│   ├── main.py                 ← API endpoints
│   ├── models.py               ← Database models
│   ├── import_data.py          ← XLSX → SQLite
│   └── start.sh                ← Run this first
├── frontend/                   ← Next.js app
│   ├── app/                    ← Pages
│   ├── components/             ← UI components
│   ├── hooks/                  ← React hooks
│   ├── lib/api.ts              ← Backend API client
│   └── start.sh                ← Quick start (optional)
├── data/                       ← Put your .xlsx here
└── README.md                   ← Full documentation
```

## If Something Goes Wrong

**Backend won't start?**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python import_data.py
uvicorn main:app --reload --port 8000
```

**Frontend won't start?**
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

**Data not showing?**
- Make sure the `.xlsx` file is in the `data/` folder
- Check that it has "Quick Reference" and "Deep Study" sheets
- Run: `python backend/import_data.py --refresh`

**CORS errors?**
- Ensure backend is on port 8000
- Ensure frontend is on port 3000
- Make sure both are running simultaneously

## Interview Day Setup

For actual interview use:

1. **Two terminals**: One for backend, one for frontend
2. **Backend terminal**: `cd backend && ./start.sh`
3. **Frontend terminal**: `cd frontend && npm run dev`
4. **Browser**: Open `http://localhost:3000`
5. **Position**: Second monitor if allowed
6. **Mode**: Switch to Interview mode (`Cmd+I`)
7. **Navigate**: Use keyboard shortcuts exclusively

---

**Mission complete. All systems operational and ready to execute. When the interviewer asks about distributed systems, you don't guess—you reference, articulate, and dominate.**
