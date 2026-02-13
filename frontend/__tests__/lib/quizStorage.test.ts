import {
  saveQuizSession,
  getQuizHistory,
  calculateScore,
  generateSessionId,
  saveTimerState,
  getTimerState,
  calculateRemainingTime,
  clearTimerState,
  QuizSession,
  AssessmentScores,
} from "@/lib/quizStorage";

describe("quizStorage", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  describe("generateSessionId", () => {
    it("generates unique IDs", () => {
      const id1 = generateSessionId();
      const id2 = generateSessionId();

      expect(id1).toBeDefined();
      expect(id2).toBeDefined();
      expect(id1).not.toBe(id2);
    });

    it("generates IDs with correct format", () => {
      const id = generateSessionId();
      expect(id).toMatch(/^quiz_\d+_[a-z0-9]+$/);
    });
  });

  describe("calculateScore", () => {
    it("calculates correct percentage for all strong scores", () => {
      const scores: AssessmentScores = {
        deliveryFramework: [
          { criterion: "Requirements", score: "strong" },
          { criterion: "Design", score: "strong" },
        ],
        competencies: [{ criterion: "Problem", score: "strong" }],
        technologySpecific: [],
      };

      const result = calculateScore(scores);
      expect(result.percentage).toBe(100);
      expect(result.grade).toBe("A");
    });

    it("calculates correct percentage for mixed scores", () => {
      const scores: AssessmentScores = {
        deliveryFramework: [
          { criterion: "Requirements", score: "strong" },
          { criterion: "Design", score: "adequate" },
        ],
        competencies: [{ criterion: "Problem", score: "weak" }],
        technologySpecific: [],
      };

      const result = calculateScore(scores);
      expect(result.percentage).toBe(50);
      expect(result.grade).toBe("F");
    });

    it("calculates correct percentage for all weak scores", () => {
      const scores: AssessmentScores = {
        deliveryFramework: [
          { criterion: "Requirements", score: "weak" },
          { criterion: "Design", score: "weak" },
        ],
        competencies: [{ criterion: "Problem", score: "weak" }],
        technologySpecific: [],
      };

      const result = calculateScore(scores);
      expect(result.percentage).toBe(0);
      expect(result.grade).toBe("F");
    });

    it("assigns correct grades for various percentages", () => {
      const createScores = (
        strongCount: number,
        adequateCount: number,
        weakCount: number,
      ): AssessmentScores => ({
        deliveryFramework: [
          ...Array(Math.min(strongCount, 10))
            .fill(null)
            .map((_, i) => ({
              criterion: `Strong ${i}`,
              score: "strong" as const,
            })),
          ...Array(Math.min(adequateCount, 10))
            .fill(null)
            .map((_, i) => ({
              criterion: `Adequate ${i}`,
              score: "adequate" as const,
            })),
          ...Array(Math.min(weakCount, 10))
            .fill(null)
            .map((_, i) => ({
              criterion: `Weak ${i}`,
              score: "weak" as const,
            })),
        ],
        competencies: [],
        technologySpecific: [],
      });

      const gradeA = calculateScore(createScores(9, 1, 0));
      expect(gradeA.percentage).toBeGreaterThanOrEqual(90);
      expect(gradeA.grade).toBe("A");

      const gradeB = calculateScore(createScores(8, 0, 2));
      expect(gradeB.percentage).toBeGreaterThanOrEqual(80);
      expect(gradeB.percentage).toBeLessThan(90);
      expect(gradeB.grade).toBe("B");

      const gradeC = calculateScore(createScores(7, 0, 3));
      expect(gradeC.percentage).toBeGreaterThanOrEqual(70);
      expect(gradeC.percentage).toBeLessThan(80);
      expect(gradeC.grade).toBe("C");

      const gradeD = calculateScore(createScores(6, 0, 4));
      expect(gradeD.percentage).toBeGreaterThanOrEqual(60);
      expect(gradeD.percentage).toBeLessThan(70);
      expect(gradeD.grade).toBe("D");

      const gradeF = calculateScore(createScores(3, 2, 5));
      expect(gradeF.percentage).toBeLessThan(60);
      expect(gradeF.grade).toBe("F");
    });
  });

  describe("timer persistence", () => {
    it("saves and retrieves timer state", () => {
      const sessionId = "test-session-1";
      const startTime = Date.now();

      saveTimerState(sessionId, startTime);
      const retrieved = getTimerState(sessionId);

      expect(retrieved).toBe(startTime);
    });

    it("returns null for non-existent timer state", () => {
      const retrieved = getTimerState("non-existent-session");
      expect(retrieved).toBeNull();
    });

    it("clears timer state", () => {
      const sessionId = "test-session-2";
      const startTime = Date.now();

      saveTimerState(sessionId, startTime);
      expect(getTimerState(sessionId)).toBe(startTime);

      clearTimerState(sessionId);
      expect(getTimerState(sessionId)).toBeNull();
    });

    it("calculates remaining time correctly", () => {
      const totalSeconds = 1800;
      const startTime = Date.now() - 300000;

      const remaining = calculateRemainingTime(startTime, totalSeconds);

      expect(remaining).toBeGreaterThanOrEqual(1499);
      expect(remaining).toBeLessThanOrEqual(1500);
    });

    it("returns 0 when time has elapsed", () => {
      const totalSeconds = 60;
      const startTime = Date.now() - 120000;

      const remaining = calculateRemainingTime(startTime, totalSeconds);

      expect(remaining).toBe(0);
    });

    it("handles timer started in the future", () => {
      const totalSeconds = 1800;
      const startTime = Date.now() + 1000;

      const remaining = calculateRemainingTime(startTime, totalSeconds);

      expect(remaining).toBeGreaterThanOrEqual(totalSeconds);
      expect(remaining).toBeLessThanOrEqual(totalSeconds + 2);
    });
  });

  describe("version migration", () => {
    it("adds version to old sessions", () => {
      const oldSession = {
        id: "old-1",
        date: new Date().toISOString(),
        mode: "practice" as const,
        questions: [],
        answers: {},
        timeAllocated: 1800,
        timeTaken: 0,
        completed: false,
      };

      localStorage.setItem("practice_sessions", JSON.stringify([oldSession]));

      const sessions = getQuizHistory();
      expect(sessions[0].version).toBe(1);
    });

    it("preserves version on already-migrated sessions", () => {
      const newSession: QuizSession = {
        version: 1,
        id: "new-1",
        date: new Date().toISOString(),
        mode: "practice",
        questions: [],
        answers: {},
        timeAllocated: 1800,
        timeTaken: 0,
        completed: false,
      };

      saveQuizSession(newSession);

      const sessions = getQuizHistory();
      expect(sessions[0].version).toBe(1);
    });

    it("handles mixed old and new sessions", () => {
      const oldSession = {
        id: "old-1",
        date: new Date().toISOString(),
        mode: "practice" as const,
        questions: [],
        answers: {},
        timeAllocated: 1800,
        timeTaken: 0,
        completed: false,
      };

      const newSession: QuizSession = {
        version: 1,
        id: "new-1",
        date: new Date().toISOString(),
        mode: "practice",
        questions: [],
        answers: {},
        timeAllocated: 1800,
        timeTaken: 0,
        completed: false,
      };

      localStorage.setItem(
        "practice_sessions",
        JSON.stringify([oldSession, newSession]),
      );

      const sessions = getQuizHistory();
      expect(sessions).toHaveLength(2);
      expect(sessions.every((s) => s.version === 1)).toBe(true);
    });
  });

  describe("session storage", () => {
    it("saves and retrieves quiz sessions", () => {
      const session: QuizSession = {
        version: 1,
        id: "test-1",
        date: new Date().toISOString(),
        mode: "practice",
        questions: [],
        answers: {},
        timeAllocated: 1800,
        timeTaken: 0,
        completed: false,
      };

      saveQuizSession(session);
      const sessions = getQuizHistory();

      expect(sessions).toHaveLength(1);
      expect(sessions[0].id).toBe("test-1");
    });

    it("sorts sessions by date descending", () => {
      const now = new Date();
      const session1: QuizSession = {
        version: 1,
        id: "oldest",
        date: new Date(now.getTime() - 2000).toISOString(),
        mode: "practice",
        questions: [],
        answers: {},
        timeAllocated: 1800,
        timeTaken: 0,
        completed: false,
      };

      const session2: QuizSession = {
        version: 1,
        id: "newest",
        date: now.toISOString(),
        mode: "practice",
        questions: [],
        answers: {},
        timeAllocated: 1800,
        timeTaken: 0,
        completed: false,
      };

      saveQuizSession(session1);
      saveQuizSession(session2);

      const sessions = getQuizHistory();
      expect(sessions[0].id).toBe("newest");
      expect(sessions[1].id).toBe("oldest");
    });
  });
});
