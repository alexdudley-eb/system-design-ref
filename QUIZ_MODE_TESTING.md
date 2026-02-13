# Quiz Mode Testing Guide

## Overview

The Quiz Mode feature is now fully implemented. This guide provides instructions for testing all functionality end-to-end.

## Starting the Application

Make sure both backend and frontend are running:

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Testing Checklist

### 1. Quiz Setup Screen ✓

**Steps:**
1. Open the app at `http://localhost:3000`
2. Click the **🎯 Quiz Me** button in the header
3. Modal should open with setup screen

**Verify:**
- [ ] Setup screen displays with configuration options
- [ ] Can select question count (1, 3, 5)
- [ ] Can select time limit (15, 30, 45, 60 minutes)
- [ ] "What to Expect" section displays information
- [ ] "Start Quiz" button is enabled
- [ ] Clicking "Start Quiz" loads questions

### 2. Quiz Question Screen ✓

**Steps:**
1. Start a quiz with 3 questions and 30 minutes
2. Observe the question display

**Verify:**
- [ ] Question counter shows "Question 1 of 3"
- [ ] Question type badge shows "📊 Scenario" or "💡 Technology Selection"
- [ ] Timer displays in MM:SS format and counts down
- [ ] Technology questions show multiple choice options
- [ ] Scenario questions show full scenario details
- [ ] Notes textarea is available for both question types
- [ ] Progress dots at bottom show current question
- [ ] Navigation buttons work (Previous/Next)

### 3. Timer Functionality ✓

**Steps:**
1. Start a quiz
2. Let timer run for various durations

**Verify:**
- [ ] Timer counts down every second
- [ ] Timer shows warning state (yellow) when <5 minutes remain
- [ ] Timer shows critical state (red/pulsing) when <1 minute remains
- [ ] Timer pauses when switching to another tab
- [ ] Timer resumes when returning to tab
- [ ] Alert shows when time reaches 0:00
- [ ] Quiz auto-submits when timer expires

### 4. Question Navigation ✓

**Steps:**
1. Start a quiz with 5 questions
2. Test all navigation methods

**Verify:**
- [ ] "Next" button moves to next question
- [ ] "Previous" button moves to previous question
- [ ] Progress dots can be clicked to jump to questions
- [ ] Answered questions show green dot
- [ ] Current question shows larger blue dot
- [ ] Unanswered questions show gray dot
- [ ] "Finish Quiz" button appears on last question
- [ ] Answers are saved when navigating between questions

### 5. Answer Persistence ✓

**Steps:**
1. Start a quiz
2. Answer question 1
3. Navigate to question 2
4. Navigate back to question 1

**Verify:**
- [ ] Previously selected answer is still selected
- [ ] Previously entered notes are still present
- [ ] Can modify answers and notes
- [ ] Changes are saved automatically

### 6. Quiz Resume ✓

**Steps:**
1. Start a quiz
2. Answer 2 out of 5 questions
3. Close the modal
4. Re-open Quiz Mode

**Verify:**
- [ ] Confirmation prompt asks to save progress
- [ ] After reopening, quiz resumes where you left off
- [ ] Previously answered questions show as completed
- [ ] Timer continues from where it left off
- [ ] All previous answers are preserved

### 7. Self-Assessment Screen ✓

**Steps:**
1. Complete a quiz (answer questions and click "Finish Quiz")
2. Assessment screen should appear

**Verify:**
- [ ] Assessment sections display based on question types:
  - Delivery Framework (for scenario questions)
  - Assessment Rubric Competencies (always shown)
  - Technology-Specific (for tech questions)
- [ ] Each criterion has Strong/Adequate/Weak radio buttons
- [ ] All criteria default to "Adequate"
- [ ] Can change scores for each criterion
- [ ] "Complete Assessment" button is visible
- [ ] Clicking button proceeds to results

### 8. Results Screen ✓

**Steps:**
1. Complete assessment
2. Review results screen

**Verify:**
- [ ] Grade circle shows letter grade (A-F) and percentage
- [ ] Result cards show:
  - Questions answered (percentage)
  - Time taken
  - Time status (under/over)
- [ ] Strengths section lists "Strong" criteria (if any)
- [ ] Areas for Improvement lists "Weak" criteria (if any)
- [ ] Question breakdown shows all questions:
  - Question number and type
  - Answered/Skipped status
  - Your notes (if provided)
  - For tech questions: your answer vs correct answer
  - Explanation for tech questions
- [ ] "View Quiz History" button works
- [ ] "Start New Quiz" button works

### 9. Quiz History Screen ✓

**Steps:**
1. Complete multiple quizzes
2. Click "View Quiz History" from results

**Verify:**
- [ ] Completed sessions table shows:
  - Date/time
  - Question count
  - Time taken
  - Score percentage
  - Grade badge (color-coded)
- [ ] Incomplete sessions (if any) show separately:
  - Progress bar
  - Percentage completed
- [ ] "Review" button opens results for that session
- [ ] Delete button (🗑) removes session
- [ ] Confirmation prompt before deletion
- [ ] "Start New Quiz" button clears history view

### 10. Technology Questions ✓

**Steps:**
1. Start a quiz until you get a technology question
2. Test functionality

**Verify:**
- [ ] Question category badge shows (e.g., "Database Selection")
- [ ] Question text is clear and descriptive
- [ ] 4 options (a, b, c, d) are displayed
- [ ] Can select one option
- [ ] Notes textarea available
- [ ] In results, shows correct answer and explanation
- [ ] Key considerations listed
- [ ] Limitations mentioned

### 11. Scenario Questions ✓

**Steps:**
1. Start a quiz until you get a scenario question
2. Test functionality

**Verify:**
- [ ] Question shows "Design a [Scenario Title]"
- [ ] Instructions prompt to follow Delivery Framework
- [ ] Full scenario details embedded (ScenarioDetail component)
- [ ] Shows requirements, entities, API, high-level design, etc.
- [ ] Larger notes textarea (8 rows vs 4)
- [ ] Hint text references Delivery Framework phases

### 12. Local Storage ✓

**Steps:**
1. Complete a quiz
2. Close browser
3. Reopen browser and navigate to app

**Verify:**
- [ ] Open DevTools → Application → Local Storage
- [ ] `quiz_sessions` key contains array of sessions
- [ ] Each session has proper structure
- [ ] `active_quiz_session` exists if quiz was in progress
- [ ] History persists across browser sessions
- [ ] Maximum 50 sessions enforced

### 13. Scoring System ✓

**Steps:**
1. Complete assessment with mixed scores
2. Verify calculation

**Verify:**
- [ ] Strong = 2 points
- [ ] Adequate = 1 point
- [ ] Weak = 0 points
- [ ] Total score calculated correctly
- [ ] Percentage = (points / max points) × 100
- [ ] Grade mapping:
  - 90%+ = A
  - 80-89% = B
  - 70-79% = C
  - 60-69% = D
  - <60% = F

### 14. Edge Cases ✓

**Test these scenarios:**

**Page Refresh During Quiz:**
- [ ] Refresh browser mid-quiz
- [ ] Quiz state persists via localStorage
- [ ] Timer resets (known limitation)
- [ ] Answers are preserved

**Close Modal Mid-Quiz:**
- [ ] Confirmation prompt appears
- [ ] Can cancel to continue quiz
- [ ] Progress saved if confirmed

**No Questions Answered:**
- [ ] Can still finish quiz
- [ ] Confirmation prompt warns
- [ ] Assessment still available
- [ ] Results show 0% completion

**Timer Expires:**
- [ ] Alert notification
- [ ] Auto-proceeds to assessment
- [ ] Time taken = full allocation

**Empty History:**
- [ ] Shows empty state message
- [ ] "Start Your First Quiz" button
- [ ] No errors

### 15. API Endpoints ✓

**Test backend endpoints directly:**

```bash
# Get random question
curl http://localhost:8000/api/quiz/question

# Get scenario question
curl http://localhost:8000/api/quiz/question?question_type=scenario

# Get technology question
curl http://localhost:8000/api/quiz/question?question_type=technology

# Get 5 questions for quiz
curl http://localhost:8000/api/quiz/questions?count=5
```

**Verify:**
- [ ] Endpoints return 200 OK
- [ ] Random selection works (70/30 split)
- [ ] Scenario questions include full scenario data
- [ ] Tech questions include options, correct answer, explanation
- [ ] No duplicate questions in same session
- [ ] Count parameter works (1-10)

### 16. Responsive Design ✓

**Test on different screen sizes:**

**Desktop (1920x1080):**
- [ ] Modal is centered and max-width 1200px
- [ ] All elements properly spaced
- [ ] Readable text sizes

**Tablet (768px):**
- [ ] Modal adjusts to screen width
- [ ] Navigation stacks vertically
- [ ] Progress dots remain visible
- [ ] Tables remain readable

**Mobile (375px):**
- [ ] Modal fills screen (no border-radius)
- [ ] Setup options stack vertically
- [ ] Question content readable
- [ ] Timer visible
- [ ] Navigation fully stacked

## Known Limitations

1. **Timer Reset on Refresh**: Timer doesn't persist exact remaining time on page refresh (resets to full allocation)
2. **No Audio Alerts**: Visual-only timer warnings (audio alerts commented out in plan but not implemented)
3. **No Cross-Device Sync**: Quiz history is per-browser (localStorage only)
4. **50 Session Limit**: Older sessions auto-deleted when limit reached

## Success Criteria

All checkboxes above should be ✓ for full feature validation.

## Performance Testing

- [ ] Quiz loads in <2 seconds
- [ ] Question navigation is instant
- [ ] Timer updates smoothly (no lag)
- [ ] Assessment screen renders quickly
- [ ] Results screen with 5+ questions loads in <1 second
- [ ] History table with 20+ sessions loads in <1 second

## Browser Compatibility

Test in:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

## Accessibility Testing

- [ ] Can navigate entire quiz with keyboard only
- [ ] Tab order is logical
- [ ] Radio buttons keyboard-accessible
- [ ] Buttons have clear focus states
- [ ] Screen reader announces timer warnings
- [ ] All images/icons have appropriate alt text

## Summary

Quiz Mode is fully functional and ready for use. Follow this checklist to ensure all features work as expected. Report any issues found during testing.
