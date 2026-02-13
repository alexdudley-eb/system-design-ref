"use client";

import { TestSession, getTestHistory, deleteTestSession, formatDuration, formatDate, calculateScore } from "@/lib/quizStorage";
import styles from "./TestMode.module.css";

interface TestHistoryProps {
  onReview: (session: TestSession) => void;
  onStartNew: () => void;
}

export default function TestHistory({ onReview, onStartNew }: TestHistoryProps) {
  const sessions = getTestHistory();

  const handleDelete = (id: string) => {
    if (window.confirm("Are you sure you want to delete this test session?")) {
      deleteTestSession(id);
      window.location.reload();
    }
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
        <h3>Test History</h3>
        <p>Review your system design test sessions</p>
      </div>

      {sessions.length === 0 ? (
        <div className={styles.historyEmpty}>
          <div className={styles.emptyIcon}>📝</div>
          <h3>No Test History</h3>
          <p>Complete your first test to see results here</p>
          <button className={styles.primaryButton} onClick={onStartNew}>
            Start Your First Test
          </button>
        </div>
      ) : (
        <>
          {completedSessions.length > 0 && (
            <div className={styles.historySection}>
              <h4 className={styles.sectionTitle}>Completed Tests</h4>
              <div className={styles.historyTable}>
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Scenario</th>
                      <th>Time</th>
                      <th>Score</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {completedSessions.map((session) => {
                      const { grade, percentage } = calculateScore(session.assessmentScores!);

                      return (
                        <tr key={session.id}>
                          <td>{formatDate(session.date)}</td>
                          <td>{session.scenario.title}</td>
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
                      <th>Scenario</th>
                      <th>Time Allocated</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {incompleteSessions.map((session) => {
                      return (
                        <tr key={session.id}>
                          <td>{formatDate(session.date)}</td>
                          <td>{session.scenario.title}</td>
                          <td>{session.timeAllocated} minutes</td>
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
              Start New Test
            </button>
          </div>
        </>
      )}
    </div>
  );
}
