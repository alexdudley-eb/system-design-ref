"use client";

import { useState } from "react";
import styles from "./PracticeMode.module.css";

interface QuizSetupProps {
  onStart: (questionCount: number, timeAllocated: number) => void;
  loading?: boolean;
}

export default function QuizSetup({ onStart, loading }: QuizSetupProps) {
  const [questionCount, setQuestionCount] = useState(5);
  const [timeAllocated, setTimeAllocated] = useState(45);

  const handleStart = () => {
    onStart(questionCount, timeAllocated);
  };

  return (
    <div className={styles.setupContainer}>
      <div className={styles.setupSection}>
        <h3>Configure Your Quiz</h3>
        <p className={styles.setupDescription}>
          Test your system design knowledge with a mix of scenario-based and
          technology selection questions. Track your progress and identify
          areas for improvement.
        </p>
      </div>

      <div className={styles.setupSection}>
        <label className={styles.setupLabel}>Number of Questions</label>
        <div className={styles.radioGroup}>
          <label className={styles.radioOption}>
            <input
              type="radio"
              name="questionCount"
              value="1"
              checked={questionCount === 1}
              onChange={() => setQuestionCount(1)}
            />
            <span>1 question</span>
            <span className={styles.radioDescription}>Quick practice</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="questionCount"
              value="3"
              checked={questionCount === 3}
              onChange={() => setQuestionCount(3)}
            />
            <span>3 questions</span>
            <span className={styles.radioDescription}>Short session</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="questionCount"
              value="5"
              checked={questionCount === 5}
              onChange={() => setQuestionCount(5)}
            />
            <span>5 questions</span>
            <span className={styles.radioDescription}>
              Full practice (recommended)
            </span>
          </label>
        </div>
      </div>

      <div className={styles.setupSection}>
        <label className={styles.setupLabel}>Time Limit</label>
        <div className={styles.radioGroup}>
          <label className={styles.radioOption}>
            <input
              type="radio"
              name="timeAllocated"
              value="15"
              checked={timeAllocated === 15}
              onChange={() => setTimeAllocated(15)}
            />
            <span>15 minutes</span>
            <span className={styles.radioDescription}>Quick sprint</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="timeAllocated"
              value="30"
              checked={timeAllocated === 30}
              onChange={() => setTimeAllocated(30)}
            />
            <span>30 minutes</span>
            <span className={styles.radioDescription}>Moderate pace</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="timeAllocated"
              value="45"
              checked={timeAllocated === 45}
              onChange={() => setTimeAllocated(45)}
            />
            <span>45 minutes</span>
            <span className={styles.radioDescription}>
              Standard interview time
            </span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="timeAllocated"
              value="60"
              checked={timeAllocated === 60}
              onChange={() => setTimeAllocated(60)}
            />
            <span>60 minutes</span>
            <span className={styles.radioDescription}>Extended practice</span>
          </label>
        </div>
      </div>

      <div className={styles.setupActions}>
        <button
          className={styles.startButton}
          onClick={handleStart}
          disabled={loading}
        >
          {loading ? "Loading Questions..." : "Start Quiz"}
        </button>
      </div>

      <div className={styles.setupInfo}>
        <h4>What to Expect:</h4>
        <ul>
          <li>
            <strong>Scenario Questions (70%):</strong> Full system design
            problems like Uber, WhatsApp, etc.
          </li>
          <li>
            <strong>Technology Questions (30%):</strong> Multiple choice
            questions testing your knowledge of when and why to use specific
            technologies
          </li>
          <li>
            <strong>Self-Assessment:</strong> After completing the quiz,
            evaluate yourself against the Delivery Framework and Assessment
            Rubric
          </li>
          <li>
            <strong>Progress Tracking:</strong> All quiz sessions are saved
            locally so you can track improvement over time
          </li>
        </ul>
      </div>
    </div>
  );
}
