"use client";

import {
  QuizSession,
  calculateScore,
  formatDuration,
} from "@/lib/quizStorage";
import styles from "./PracticeMode.module.css";

interface QuizResultsProps {
  session: QuizSession;
  onStartNew: () => void;
  onViewHistory: () => void;
}

export default function QuizResults({
  session,
  onStartNew,
  onViewHistory,
}: QuizResultsProps) {
  if (!session.assessmentScores) {
    return <div>No assessment data available</div>;
  }

  const score = calculateScore(session.assessmentScores);
  const answeredCount = Object.keys(session.answers).length;
  const totalQuestions = session.questions.length;
  const completionRate = Math.round(
    (answeredCount / totalQuestions) * 100
  );

  const weakAreas = [
    ...session.assessmentScores.deliveryFramework,
    ...session.assessmentScores.competencies,
    ...session.assessmentScores.technologySpecific,
  ]
    .filter((item) => item.score === "weak")
    .map((item) => item.criterion);

  const strongAreas = [
    ...session.assessmentScores.deliveryFramework,
    ...session.assessmentScores.competencies,
    ...session.assessmentScores.technologySpecific,
  ]
    .filter((item) => item.score === "strong")
    .map((item) => item.criterion);

  const wasUnderTime =
    session.timeTaken < session.timeAllocated * 60;
  const timePercentage = Math.round(
    (session.timeTaken / (session.timeAllocated * 60)) * 100
  );

  return (
    <div className={styles.resultsContainer}>
      <div className={styles.resultsHeader}>
        <div className={styles.resultsBanner}>
          <div className={styles.gradeCircle}>
            <span className={styles.gradeText}>{score.grade}</span>
            <span className={styles.percentageText}>{score.percentage}%</span>
          </div>
          <div className={styles.bannerText}>
            <h3>Quiz Complete!</h3>
            <p>
              You scored {score.totalPoints} out of {score.maxPoints} points
            </p>
          </div>
        </div>
      </div>

      <div className={styles.resultsGrid}>
        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>📊</div>
          <div className={styles.resultCardContent}>
            <div className={styles.resultCardValue}>{completionRate}%</div>
            <div className={styles.resultCardLabel}>
              Questions Answered ({answeredCount}/{totalQuestions})
            </div>
          </div>
        </div>

        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>⏱</div>
          <div className={styles.resultCardContent}>
            <div className={styles.resultCardValue}>
              {formatDuration(session.timeTaken)}
            </div>
            <div className={styles.resultCardLabel}>
              Time Taken ({timePercentage}% of allocated)
            </div>
          </div>
        </div>

        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>
            {wasUnderTime ? "✅" : "⚠️"}
          </div>
          <div className={styles.resultCardContent}>
            <div className={styles.resultCardValue}>
              {wasUnderTime ? "Under Time" : "Time Limit Reached"}
            </div>
            <div className={styles.resultCardLabel}>
              {wasUnderTime
                ? `${formatDuration(session.timeAllocated * 60 - session.timeTaken)} remaining`
                : "Used full time allocation"}
            </div>
          </div>
        </div>
      </div>

      {strongAreas.length > 0 && (
        <div className={styles.resultSection}>
          <h4 className={styles.strengthsHeader}>💪 Strengths</h4>
          <ul className={styles.criteriaList}>
            {strongAreas.map((criterion, idx) => (
              <li key={idx} className={styles.criteriaItemStrong}>
                {criterion}
              </li>
            ))}
          </ul>
        </div>
      )}

      {weakAreas.length > 0 && (
        <div className={styles.resultSection}>
          <h4 className={styles.improvementHeader}>📈 Areas for Improvement</h4>
          <ul className={styles.criteriaList}>
            {weakAreas.map((criterion, idx) => (
              <li key={idx} className={styles.criteriaItemWeak}>
                {criterion}
              </li>
            ))}
          </ul>
          <p className={styles.improvementTip}>
            Focus on these areas in your next practice session. Review the
            Reference Library for guidance.
          </p>
        </div>
      )}

      <div className={styles.resultSection}>
        <h4>Question-by-Question Breakdown</h4>
        <div className={styles.questionBreakdown}>
          {session.questions.map((question, idx) => {
            const answer = session.answers[question.id];
            const hasAnswer = !!answer;
            const hasNotes = !!(answer?.notes && answer.notes.trim());

            return (
              <div key={question.id} className={styles.breakdownItem}>
                <div className={styles.breakdownHeader}>
                  <span className={styles.breakdownNumber}>Q{idx + 1}</span>
                  <span className={styles.breakdownType}>
                    {question.type === "scenario" ? "📊" : "💡"}
                  </span>
                  <span className={styles.breakdownTitle}>
                    {question.type === "scenario"
                      ? question.scenario?.title || "Scenario"
                      : question.category || "Technology"}
                  </span>
                  <span
                    className={`${styles.breakdownStatus} ${
                      hasAnswer ? styles.statusAnswered : styles.statusSkipped
                    }`}
                  >
                    {hasAnswer ? "✓ Answered" : "○ Skipped"}
                  </span>
                </div>
                {hasNotes && (
                  <div className={styles.breakdownNotes}>
                    <strong>Your Notes:</strong>
                    <p>{answer.notes}</p>
                  </div>
                )}
                {question.type === "technology" &&
                  answer?.selectedAnswer &&
                  question.correct_answer && (
                    <div className={styles.breakdownAnswer}>
                      <div>
                        <strong>Your Answer:</strong> Option{" "}
                        {answer.selectedAnswer.toUpperCase()}
                      </div>
                      <div>
                        <strong>Correct Answer:</strong> Option{" "}
                        {question.correct_answer.toUpperCase()}
                      </div>
                      {question.explanation && (
                        <div className={styles.explanation}>
                          <strong>Explanation:</strong> {question.explanation}
                        </div>
                      )}
                    </div>
                  )}
              </div>
            );
          })}
        </div>
      </div>

      <div className={styles.resultsActions}>
        <button className={styles.secondaryButton} onClick={onViewHistory}>
          View Quiz History
        </button>
        <button className={styles.primaryButton} onClick={onStartNew}>
          Start New Quiz
        </button>
      </div>
    </div>
  );
}
