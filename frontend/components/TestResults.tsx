"use client";

import { TestSession, formatDuration, formatTime, calculateScore } from "@/lib/quizStorage";
import styles from "./TestMode.module.css";

interface TestResultsProps {
  session: TestSession;
  onStartNew: () => void;
  onViewHistory: () => void;
}

export default function TestResults({
  session,
  onStartNew,
  onViewHistory,
}: TestResultsProps) {
  const { totalPoints, maxPoints, percentage, grade } = calculateScore(session.assessmentScores!);

  return (
    <div className={styles.resultsContainer}>
      <div className={styles.resultsHeader}>
        <div className={styles.resultsBanner}>
          <div className={styles.gradeCircle}>
            <span className={styles.gradeText}>{grade}</span>
            <span className={styles.percentageText}>{percentage}%</span>
          </div>
          <div className={styles.bannerText}>
            <h3>Test Complete!</h3>
            <p>{session.scenario.title}</p>
          </div>
        </div>
      </div>

      <div className={styles.resultsGrid}>
        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>⏱</div>
          <div>
            <div className={styles.resultCardValue}>
              {formatDuration(session.timeTaken)}
            </div>
            <div className={styles.resultCardLabel}>Time Taken</div>
          </div>
        </div>

        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>📊</div>
          <div>
            <div className={styles.resultCardValue}>{totalPoints}/{maxPoints}</div>
            <div className={styles.resultCardLabel}>Overall Score</div>
          </div>
        </div>

        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>✓</div>
          <div>
            <div className={styles.resultCardValue}>
              {session.design.functionalRequirements.filter(r => r.trim()).length}
            </div>
            <div className={styles.resultCardLabel}>Requirements Identified</div>
          </div>
        </div>

        <div className={styles.resultCard}>
          <div className={styles.resultCardIcon}>🔧</div>
          <div>
            <div className={styles.resultCardValue}>
              {session.design.entities.filter(e => e.name.trim()).length}
            </div>
            <div className={styles.resultCardLabel}>Entities Defined</div>
          </div>
        </div>
      </div>

      <div className={styles.resultSection}>
        <h4>Your Design</h4>
        <div className={styles.designSummary}>
          <div className={styles.summaryItem}>
            <h5>Functional Requirements ({session.design.functionalRequirements.filter(r => r.trim()).length})</h5>
            <ul>
              {session.design.functionalRequirements.filter(r => r.trim()).map((req, idx) => (
                <li key={idx}>{req}</li>
              ))}
            </ul>
          </div>

          <div className={styles.summaryItem}>
            <h5>Non-Functional Requirements ({session.design.nonFunctionalRequirements.filter(r => r.trim()).length})</h5>
            <ul>
              {session.design.nonFunctionalRequirements.filter(r => r.trim()).map((req, idx) => (
                <li key={idx}>{req}</li>
              ))}
            </ul>
          </div>

          <div className={styles.summaryItem}>
            <h5>Entities ({session.design.entities.filter(e => e.name.trim()).length})</h5>
            {session.design.entities.filter(e => e.name.trim()).map((entity, idx) => (
              <div key={idx} className={styles.entityDisplay}>
                <strong>{entity.name}:</strong> {entity.fields.filter(f => f.trim()).join(', ')}
              </div>
            ))}
          </div>

          <div className={styles.summaryItem}>
            <h5>API Endpoints ({session.design.apiEndpoints.filter(e => e.path.trim()).length})</h5>
            {session.design.apiEndpoints.filter(e => e.path.trim()).map((endpoint, idx) => (
              <div key={idx} className={styles.apiDisplay}>
                <code>{endpoint.method} {endpoint.path}</code> - {endpoint.description}
              </div>
            ))}
          </div>

          {session.design.highLevelDesign && (
            <div className={styles.summaryItem}>
              <h5>High-Level Design</h5>
              <p>{session.design.highLevelDesign}</p>
            </div>
          )}

          {session.design.components.filter(c => c.trim()).length > 0 && (
            <div className={styles.summaryItem}>
              <h5>Components</h5>
              <ul>
                {session.design.components.filter(c => c.trim()).map((comp, idx) => (
                  <li key={idx}>{comp}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      <div className={styles.resultsActions}>
        <button className={styles.secondaryButton} onClick={onViewHistory}>
          View History
        </button>
        <button className={styles.primaryButton} onClick={onStartNew}>
          Start New Test
        </button>
      </div>
    </div>
  );
}
