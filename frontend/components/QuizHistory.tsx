"use client";

import { useState, useEffect } from "react";
import {
  QuizSession,
  getQuizHistory,
  deleteQuizSession,
  calculateScore,
  formatDuration,
} from "@/lib/quizStorage";
import styles from "./PracticeMode.module.css";

interface QuizHistoryProps {
  onReview: (session: QuizSession) => void;
  onStartNew: () => void;
}

export default function QuizHistory({
  onReview,
  onStartNew,
}: QuizHistoryProps) {
  const [sessions, setSessions] = useState<QuizSession[]>([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = () => {
    const history = getQuizHistory();
    setSessions(history);
  };

  const handleDelete = (sessionId: string) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this quiz session?"
    );
    if (confirmDelete) {
      deleteQuizSession(sessionId);
      loadHistory();
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (sessions.length === 0) {
    return (
      <div className={styles.historyEmpty}>
        <div className={styles.emptyIcon}>📊</div>
        <h3>No Quiz History Yet</h3>
        <p>
          Complete your first quiz to start tracking your progress over time.
        </p>
        <button className={styles.primaryButton} onClick={onStartNew}>
          Start Your First Quiz
        </button>
      </div>
    );
  }

  const completedSessions = sessions.filter((s) => s.completed);
  const incompleteSessions = sessions.filter((s) => !s.completed);

  return (
    <div className={styles.historyContainer}>
      <div className={styles.historyHeader}>
        <h3>Quiz History</h3>
        <p>
          Track your progress and review past quiz sessions. Total sessions:{" "}
          {sessions.length}
        </p>
      </div>

      {incompleteSessions.length > 0 && (
        <div className={styles.historySection}>
          <h4 className={styles.sectionTitle}>⏸ Incomplete Sessions</h4>
          <div className={styles.historyTable}>
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Questions</th>
                  <th>Progress</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {incompleteSessions.map((session) => {
                  const answeredCount = Object.keys(session.answers).length;
                  const totalQuestions = session.questions.length;
                  const progress = Math.round(
                    (answeredCount / totalQuestions) * 100
                  );

                  return (
                    <tr key={session.id}>
                      <td>{formatDate(session.date)}</td>
                      <td>
                        {answeredCount}/{totalQuestions}
                      </td>
                      <td>
                        <div className={styles.progressBar}>
                          <div
                            className={styles.progressFill}
                            style={{ width: `${progress}%` }}
                          />
                        </div>
                        <span className={styles.progressText}>
                          {progress}%
                        </span>
                      </td>
                      <td>
                        <button
                          className={styles.deleteButton}
                          onClick={() => handleDelete(session.id)}
                          title="Delete session"
                        >
                          🗑
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {completedSessions.length > 0 && (
        <div className={styles.historySection}>
          <h4 className={styles.sectionTitle}>✅ Completed Sessions</h4>
          <div className={styles.historyTable}>
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Questions</th>
                  <th>Time</th>
                  <th>Score</th>
                  <th>Grade</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {completedSessions.map((session) => {
                  const score = session.assessmentScores
                    ? calculateScore(session.assessmentScores)
                    : null;

                  return (
                    <tr key={session.id}>
                      <td>{formatDate(session.date)}</td>
                      <td>{session.questions.length}</td>
                      <td>{formatDuration(session.timeTaken)}</td>
                      <td>
                        {score ? `${score.percentage}%` : "N/A"}
                      </td>
                      <td>
                        <span
                          className={`${styles.gradeBadge} ${
                            styles[`grade${score?.grade || "F"}`]
                          }`}
                        >
                          {score?.grade || "N/A"}
                        </span>
                      </td>
                      <td className={styles.actionButtons}>
                        <button
                          className={styles.reviewButton}
                          onClick={() => onReview(session)}
                          title="Review details"
                        >
                          👁 Review
                        </button>
                        <button
                          className={styles.deleteButton}
                          onClick={() => handleDelete(session.id)}
                          title="Delete session"
                        >
                          🗑
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className={styles.historyActions}>
        <button className={styles.primaryButton} onClick={onStartNew}>
          Start New Quiz
        </button>
      </div>
    </div>
  );
}
