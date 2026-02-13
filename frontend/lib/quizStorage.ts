import { QuizQuestion } from "./api";

export interface AssessmentScore {
  criterion: string;
  score: "strong" | "adequate" | "weak";
}

export interface AssessmentScores {
  deliveryFramework: AssessmentScore[];
  competencies: AssessmentScore[];
  technologySpecific: AssessmentScore[];
}

export interface QuizAnswer {
  questionId: string;
  selectedAnswer?: string;
  notes?: string;
}

export interface QuizSession {
  version: number;
  id: string;
  date: string;
  mode: "practice";
  questions: QuizQuestion[];
  answers: Record<string, QuizAnswer>;
  assessmentScores?: AssessmentScores;
  timeAllocated: number;
  timeTaken: number;
  completed: boolean;
  timerStartTime?: number;
}

export interface FlashcardAnswer {
  questionId: string;
  userAnswer: string;
  isCorrect: boolean;
  selfAssessed?: boolean;
}

export interface FlashcardSession {
  version: number;
  id: string;
  date: string;
  mode: "quiz";
  flashcards: any[];
  answers: Record<string, FlashcardAnswer>;
  correctCount: number;
  incorrectCount: number;
  timeAllocated: number;
  timeTaken: number;
  completed: boolean;
  answerMode: "multiple-choice" | "write-in";
  timerStartTime?: number;
}

export interface TestDesign {
  functionalRequirements: string[];
  nonFunctionalRequirements: string[];
  outOfScope: string[];
  entities: Array<{ name: string; fields: string[] }>;
  apiEndpoints: Array<{ method: string; path: string; description: string }>;
  highLevelDesign: string;
  components: string[];
  deepDives: Array<{ topic: string; notes: string }>;
  tradeoffs: string;
  scalingConsiderations: string;
  failureModes: string;
}

export interface TestSession {
  version: number;
  id: string;
  date: string;
  mode: "test";
  scenario: any;
  design: TestDesign;
  assessmentScores?: AssessmentScores;
  timeAllocated: number;
  timeTaken: number;
  completed: boolean;
  timerStartTime?: number;
}

const PRACTICE_STORAGE_KEY = "practice_sessions";
const QUIZ_STORAGE_KEY = "quiz_sessions";
const TEST_STORAGE_KEY = "test_sessions";
const MAX_SESSIONS = 50;
const ACTIVE_PRACTICE_KEY = "active_practice_session";
const ACTIVE_QUIZ_KEY = "active_quiz_session";
const ACTIVE_TEST_KEY = "active_test_session";
const CURRENT_VERSION = 1;

function migrateQuizSession(session: any): QuizSession {
  if (!session.version || session.version < CURRENT_VERSION) {
    return { ...session, version: CURRENT_VERSION };
  }
  return session;
}

function migrateFlashcardSession(session: any): FlashcardSession {
  if (!session.version || session.version < CURRENT_VERSION) {
    return { ...session, version: CURRENT_VERSION };
  }
  return session;
}

function migrateTestSession(session: any): TestSession {
  if (!session.version || session.version < CURRENT_VERSION) {
    return { ...session, version: CURRENT_VERSION };
  }
  return session;
}

export function saveQuizSession(session: QuizSession): void {
  try {
    const sessions = getQuizHistory();

    const existingIndex = sessions.findIndex((s) => s.id === session.id);
    if (existingIndex >= 0) {
      sessions[existingIndex] = session;
    } else {
      sessions.unshift(session);
    }

    if (sessions.length > MAX_SESSIONS) {
      sessions.splice(MAX_SESSIONS);
    }

    localStorage.setItem(PRACTICE_STORAGE_KEY, JSON.stringify(sessions));
  } catch (error) {
    console.error("Failed to save practice session:", error);
  }
}

export function getQuizHistory(): QuizSession[] {
  try {
    const stored = localStorage.getItem(PRACTICE_STORAGE_KEY);
    if (!stored) return [];

    const sessions = JSON.parse(stored) as any[];
    return sessions
      .map(migrateQuizSession)
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  } catch (error) {
    console.error("Failed to load practice history:", error);
    return [];
  }
}

export function getQuizSession(id: string): QuizSession | null {
  try {
    const sessions = getQuizHistory();
    return sessions.find((s) => s.id === id) || null;
  } catch (error) {
    console.error("Failed to load practice session:", error);
    return null;
  }
}

export function deleteQuizSession(id: string): void {
  try {
    const sessions = getQuizHistory();
    const filtered = sessions.filter((s) => s.id !== id);
    localStorage.setItem(PRACTICE_STORAGE_KEY, JSON.stringify(filtered));
  } catch (error) {
    console.error("Failed to delete practice session:", error);
  }
}

export function saveActiveSession(session: QuizSession): void {
  try {
    localStorage.setItem(ACTIVE_PRACTICE_KEY, JSON.stringify(session));
  } catch (error) {
    console.error("Failed to save active practice session:", error);
  }
}

export function getActiveSession(): QuizSession | null {
  try {
    const stored = localStorage.getItem(ACTIVE_PRACTICE_KEY);
    if (!stored) return null;
    return JSON.parse(stored) as QuizSession;
  } catch (error) {
    console.error("Failed to load active practice session:", error);
    return null;
  }
}

export function clearActiveSession(): void {
  try {
    localStorage.removeItem(ACTIVE_PRACTICE_KEY);
  } catch (error) {
    console.error("Failed to clear active practice session:", error);
  }
}

export function saveFlashcardSession(session: FlashcardSession): void {
  try {
    const sessions = getFlashcardHistory();

    const existingIndex = sessions.findIndex((s) => s.id === session.id);
    if (existingIndex >= 0) {
      sessions[existingIndex] = session;
    } else {
      sessions.unshift(session);
    }

    if (sessions.length > MAX_SESSIONS) {
      sessions.splice(MAX_SESSIONS);
    }

    localStorage.setItem(QUIZ_STORAGE_KEY, JSON.stringify(sessions));
  } catch (error) {
    console.error("Failed to save flashcard session:", error);
  }
}

export function getFlashcardHistory(): FlashcardSession[] {
  try {
    const stored = localStorage.getItem(QUIZ_STORAGE_KEY);
    if (!stored) return [];

    const sessions = JSON.parse(stored) as any[];
    return sessions
      .map(migrateFlashcardSession)
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  } catch (error) {
    console.error("Failed to load flashcard history:", error);
    return [];
  }
}

export function deleteFlashcardSession(id: string): void {
  try {
    const sessions = getFlashcardHistory();
    const filtered = sessions.filter((s) => s.id !== id);
    localStorage.setItem(QUIZ_STORAGE_KEY, JSON.stringify(filtered));
  } catch (error) {
    console.error("Failed to delete flashcard session:", error);
  }
}

export function saveActiveFlashcardSession(session: FlashcardSession): void {
  try {
    localStorage.setItem(ACTIVE_QUIZ_KEY, JSON.stringify(session));
  } catch (error) {
    console.error("Failed to save active flashcard session:", error);
  }
}

export function getActiveFlashcardSession(): FlashcardSession | null {
  try {
    const stored = localStorage.getItem(ACTIVE_QUIZ_KEY);
    if (!stored) return null;
    return JSON.parse(stored) as FlashcardSession;
  } catch (error) {
    console.error("Failed to load active flashcard session:", error);
    return null;
  }
}

export function clearActiveFlashcardSession(): void {
  try {
    localStorage.removeItem(ACTIVE_QUIZ_KEY);
  } catch (error) {
    console.error("Failed to clear active flashcard session:", error);
  }
}

export function saveTestSession(session: TestSession): void {
  try {
    const sessions = getTestHistory();

    const existingIndex = sessions.findIndex((s) => s.id === session.id);
    if (existingIndex >= 0) {
      sessions[existingIndex] = session;
    } else {
      sessions.unshift(session);
    }

    if (sessions.length > MAX_SESSIONS) {
      sessions.splice(MAX_SESSIONS);
    }

    localStorage.setItem(TEST_STORAGE_KEY, JSON.stringify(sessions));
  } catch (error) {
    console.error("Failed to save test session:", error);
  }
}

export function getTestHistory(): TestSession[] {
  try {
    const stored = localStorage.getItem(TEST_STORAGE_KEY);
    if (!stored) return [];

    const sessions = JSON.parse(stored) as any[];
    return sessions
      .map(migrateTestSession)
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  } catch (error) {
    console.error("Failed to load test history:", error);
    return [];
  }
}

export function deleteTestSession(id: string): void {
  try {
    const sessions = getTestHistory();
    const filtered = sessions.filter((s) => s.id !== id);
    localStorage.setItem(TEST_STORAGE_KEY, JSON.stringify(filtered));
  } catch (error) {
    console.error("Failed to delete test session:", error);
  }
}

export function saveActiveTestSession(session: TestSession): void {
  try {
    localStorage.setItem(ACTIVE_TEST_KEY, JSON.stringify(session));
  } catch (error) {
    console.error("Failed to save active test session:", error);
  }
}

export function getActiveTestSession(): TestSession | null {
  try {
    const stored = localStorage.getItem(ACTIVE_TEST_KEY);
    if (!stored) return null;
    return JSON.parse(stored) as TestSession;
  } catch (error) {
    console.error("Failed to load active test session:", error);
    return null;
  }
}

export function clearActiveTestSession(): void {
  try {
    localStorage.removeItem(ACTIVE_TEST_KEY);
  } catch (error) {
    console.error("Failed to clear active test session:", error);
  }
}

export function generateSessionId(): string {
  return `quiz_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

export function calculateScore(scores: AssessmentScores): {
  totalPoints: number;
  maxPoints: number;
  percentage: number;
  grade: string;
} {
  const allScores = [
    ...scores.deliveryFramework,
    ...scores.competencies,
    ...scores.technologySpecific,
  ];

  const scoreValues = {
    strong: 2,
    adequate: 1,
    weak: 0,
  };

  const totalPoints = allScores.reduce(
    (sum, item) => sum + scoreValues[item.score],
    0,
  );
  const maxPoints = allScores.length * 2;
  const percentage =
    maxPoints > 0 ? Math.round((totalPoints / maxPoints) * 100) : 0;

  let grade = "F";
  if (percentage >= 90) grade = "A";
  else if (percentage >= 80) grade = "B";
  else if (percentage >= 70) grade = "C";
  else if (percentage >= 60) grade = "D";

  return { totalPoints, maxPoints, percentage, grade };
}

export function formatDuration(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  if (hours > 0) {
    return `${hours}h ${minutes}m ${secs}s`;
  } else if (minutes > 0) {
    return `${minutes}m ${secs}s`;
  } else {
    return `${secs}s`;
  }
}

export function formatTime(seconds: number): string {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}

export function formatDate(isoDate: string): string {
  const date = new Date(isoDate);
  return date.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
}

export function saveTimerState(sessionId: string, startTime: number): void {
  try {
    localStorage.setItem(`timer_${sessionId}`, JSON.stringify(startTime));
  } catch (error) {
    console.error("Failed to save timer state:", error);
  }
}

export function getTimerState(sessionId: string): number | null {
  try {
    const stored = localStorage.getItem(`timer_${sessionId}`);
    if (!stored) return null;
    return JSON.parse(stored) as number;
  } catch (error) {
    console.error("Failed to load timer state:", error);
    return null;
  }
}

export function clearTimerState(sessionId: string): void {
  try {
    localStorage.removeItem(`timer_${sessionId}`);
  } catch (error) {
    console.error("Failed to clear timer state:", error);
  }
}

export function calculateRemainingTime(
  startTime: number,
  totalSeconds: number,
): number {
  const elapsedMs = Date.now() - startTime;
  const elapsedSeconds = Math.floor(elapsedMs / 1000);
  const remaining = Math.max(0, totalSeconds - elapsedSeconds);
  return remaining;
}
