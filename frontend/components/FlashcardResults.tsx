"use client";

import { FlashcardSession, formatDuration, formatTime } from "@/lib/quizStorage";
import styles from "./QuizMeMode.module.css";

interface FlashcardResultsProps {
  session: FlashcardSession;
  onStartNew: () => void;
  onViewHistory: () => void;
}

export default function FlashcardResults({
  session,
  onStartNew,
  onViewHistory,
}: FlashcardResultsProps) {
  const totalQuestions = session.flashcards.length;
  const correctCount = session.correctCount;
  const incorrectCount = session.incorrectCount;
  const percentage = Math.round((correctCount / totalQuestions) * 100);
  const averageTimePerQuestion = Math.round(session.timeTaken / totalQuestions);

  const getGrade = (percent: number): string => {
    if (percent >= 90) return "A";
    if (percent >= 80) return "B";
    if (percent >= 70) return "C";
    if (percent >= 60) return "D";
    return "F";
  };

  const grade = getGrade(percentage);

  return (
    <div className={styles.resultsContainer}>
      <div className={styles.resultsHeader}>
        <div className={styles.resultsBanner}>
          <div className={styles.gradeCircle}>
            <span className={styles.gradeText}>{grade}</span>
            <span className={styles.percentageText}>{percentage}%</span>
          </div>
          <div className={styles.bannerText}>
            <h3>Quiz Complete!</h3>
            <p>
              {correctCount} correct out of {totalQuestions} questions
            </p>
            <p className={styles.answerModeTag}>
              {session.answerMode === 'multiple-choice' 
                ? '📝 Multiple Choice Mode' 
                : '✍️ Write-in Mode'}
            </p>
          </div>
        </div>
      </div>

      <div className={styles.resultsGrid}>
        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>✓</div>
          <div>
            <div className={styles.resultCardValue}>{correctCount}</div>
            <div className={styles.resultCardLabel}>Correct Answers</div>
          </div>
        </div>

        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>✗</div>
          <div>
            <div className={styles.resultCardValue}>{incorrectCount}</div>
            <div className={styles.resultCardLabel}>Incorrect Answers</div>
          </div>
        </div>

        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>⏱</div>
          <div>
            <div className={styles.resultCardValue}>
              {formatDuration(session.timeTaken)}
            </div>
            <div className={styles.resultCardLabel}>Total Time</div>
          </div>
        </div>

        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>⚡</div>
          <div>
            <div className={styles.resultCardValue}>{averageTimePerQuestion}s</div>
            <div className={styles.resultCardLabel}>Avg Time per Question</div>
          </div>
        </div>
      </div>

      <div className={styles.resultSection}>
        <h4>Question Breakdown</h4>
        <div className={styles.questionBreakdown}>
          {session.flashcards.map((card, index) => {
            const answer = session.answers[card.id];
            const isCorrect = answer?.isCorrect || false;

            return (
              <div key={card.id} className={styles.breakdownItem}>
                <div className={styles.breakdownHeader}>
                  <span className={styles.breakdownNumber}>Q{index + 1}</span>
                  <span className={styles.breakdownType}>{card.category}</span>
                  <span
                    className={`${styles.breakdownStatus} ${
                      isCorrect ? styles.statusAnswered : styles.statusSkipped
                    }`}
                  >
                    {isCorrect ? "✓ Correct" : "✗ Incorrect"}
                    {answer?.selfAssessed && (
                      <span className={styles.selfAssessedBadge}> (Self-assessed)</span>
                    )}
                  </span>
                </div>

                <div className={styles.breakdownContent}>
                  <p className={styles.breakdownQuestion}>{card.question}</p>

                  {answer && (
                    <div className={styles.breakdownAnswer}>
                      <strong>Your Answer:</strong>
                      <p>{answer.userAnswer}</p>
                    </div>
                  )}

                  <div className={styles.breakdownCorrectAnswer}>
                    <strong>Correct Answer:</strong>
                    <p>{card.answer}</p>
                  </div>

                  {card.key_points && card.key_points.length > 0 && (
                    <div className={styles.breakdownKeyPoints}>
                      <strong>Key Points:</strong>
                      <ul>
                        {card.key_points.map((point: string, idx: number) => (
                          <li key={idx}>{point}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className={styles.resultsActions}>
        <button className={styles.secondaryButton} onClick={onViewHistory}>
          View History
        </button>
        <button className={styles.primaryButton} onClick={onStartNew}>
          Start New Quiz
        </button>
      </div>
    </div>
  );
}
