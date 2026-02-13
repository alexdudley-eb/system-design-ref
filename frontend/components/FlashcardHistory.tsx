"use client";

import { FlashcardSession, getFlashcardHistory, deleteFlashcardSession, formatDuration, formatDate } from "@/lib/quizStorage";
import styles from "./QuizMeMode.module.css";

interface FlashcardHistoryProps {
  onReview: (session: FlashcardSession) => void;
  onStartNew: () => void;
}

export default function FlashcardHistory({ onReview, onStartNew }: FlashcardHistoryProps) {
  const sessions = getFlashcardHistory();

  const handleDelete = (id: string) => {
    if (window.confirm("Are you sure you want to delete this quiz session?")) {
      deleteFlashcardSession(id);
      window.location.reload();
    }
  };

  const getGrade = (correctCount: number, total: number): string => {
    const percent = (correctCount / total) * 100;
    if (percent >= 90) return "A";
    if (percent >= 80) return "B";
    if (percent >= 70) return "C";
    if (percent >= 60) return "D";
    return "F";
  };

  const getGradeClass = (grade: string): string => {
    switch (grade) {
      case "A":
        return styles.gradeA;
      case "B":
        return styles.gradeB;
      case "C":
        return styles.gradeC;
      default:
        return styles.gradeD;
    }
  };

  const completedSessions = sessions.filter((s) => s.completed);
  const incompleteSessions = sessions.filter((s) => !s.completed);

  return (
    <div className={styles.historyContainer}>
      <div className={styles.historyHeader}>
        <h3>Quiz History</h3>
        <p>Review your past quiz sessions and track your progress</p>
      </div>

      {sessions.length === 0 ? (
        <div className={styles.historyEmpty}>
          <div className={styles.emptyIcon}>📚</div>
          <h3>No Quiz History</h3>
          <p>Complete your first quiz to see your results here</p>
          <button className={styles.primaryButton} onClick={onStartNew}>
            Start Your First Quiz
          </button>
        </div>
      ) : (
        <>
          {completedSessions.length > 0 && (
            <div className={styles.historySection}>
              <h4 className={styles.sectionTitle}>Completed Sessions</h4>
              <div className={styles.historyTable}>
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Questions</th>
                      <th>Correct</th>
                      <th>Incorrect</th>
                      <th>Time</th>
                      <th>Score</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {completedSessions.map((session) => {
                      const totalQuestions = session.flashcards.length;
                      const percentage = Math.round((session.correctCount / totalQuestions) * 100);
                      const grade = getGrade(session.correctCount, totalQuestions);

                      return (
                        <tr key={session.id}>
                          <td>{formatDate(session.date)}</td>
                          <td>{totalQuestions}</td>
                          <td>{session.correctCount}</td>
                          <td>{session.incorrectCount}</td>
                          <td>{formatDuration(session.timeTaken)}</td>
                          <td>
                            <span className={`${styles.gradeBadge} ${getGradeClass(grade)}`}>
                              {grade} ({percentage}%)
                            </span>
                          </td>
                          <td>
                            <div className={styles.actionButtons}>
                              <button
                                className={styles.reviewButton}
                                onClick={() => onReview(session)}
                              >
                                Review
                              </button>
                              <button
                                className={styles.deleteButton}
                                onClick={() => handleDelete(session.id)}
                              >
                                Delete
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {incompleteSessions.length > 0 && (
            <div className={styles.historySection}>
              <h4 className={styles.sectionTitle}>In Progress</h4>
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
                      const totalQuestions = session.flashcards.length;
                      const answeredCount = Object.keys(session.answers).length;
                      const progressPercent = (answeredCount / totalQuestions) * 100;

                      return (
                        <tr key={session.id}>
                          <td>{formatDate(session.date)}</td>
                          <td>{totalQuestions}</td>
                          <td>
                            <div className={styles.progressBar}>
                              <div
                                className={styles.progressFill}
                                style={{ width: `${progressPercent}%` }}
                              />
                            </div>
                            <div className={styles.progressText}>
                              {answeredCount} / {totalQuestions} answered
                            </div>
                          </td>
                          <td>
                            <div className={styles.actionButtons}>
                              <button
                                className={styles.reviewButton}
                                onClick={() => onReview(session)}
                              >
                                Continue
                              </button>
                              <button
                                className={styles.deleteButton}
                                onClick={() => handleDelete(session.id)}
                              >
                                Delete
                              </button>
                            </div>
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
        </>
      )}
    </div>
  );
}
