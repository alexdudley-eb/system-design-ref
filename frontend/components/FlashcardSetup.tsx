"use client";

import { useState } from "react";
import styles from "./QuizMeMode.module.css";

type AnswerMode = 'multiple-choice' | 'write-in';

interface FlashcardSetupProps {
  onStart: (
    questionCount: number,
    timeAllocated: number,
    category: 'all' | 'technology' | 'concept' | 'pattern' | 'numbers',
    answerMode: AnswerMode
  ) => void;
  loading?: boolean;
}

export default function FlashcardSetup({ onStart, loading }: FlashcardSetupProps) {
  const [questionCount, setQuestionCount] = useState(10);
  const [timeAllocated, setTimeAllocated] = useState(10);
  const [category, setCategory] = useState<'all' | 'technology' | 'concept' | 'pattern' | 'numbers'>('all');
  const [answerMode, setAnswerMode] = useState<AnswerMode>('multiple-choice');

  const handleStart = () => {
    onStart(questionCount, timeAllocated, category, answerMode);
  };

  return (
    <div className={styles.setupContainer}>
      <div className={styles.setupSection}>
        <h3>Quick Knowledge Testing</h3>
        <p className={styles.setupDescription}>
          Test your system design knowledge with rapid-fire flashcard questions
          covering technology selection, core concepts, design patterns, and
          numbers to know.
        </p>
      </div>

      <div className={styles.setupSection}>
        <label className={styles.setupLabel}>Number of Questions</label>
        <div className={styles.radioGroup}>
          <label className={styles.radioOption}>
            <input
              type="radio"
              name="questionCount"
              checked={questionCount === 5}
              onChange={() => setQuestionCount(5)}
            />
            <span>5 questions</span>
            <span className={styles.radioDescription}>Quick review (~5 min)</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="questionCount"
              checked={questionCount === 10}
              onChange={() => setQuestionCount(10)}
            />
            <span>10 questions</span>
            <span className={styles.radioDescription}>Standard set (~10 min)</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="questionCount"
              checked={questionCount === 15}
              onChange={() => setQuestionCount(15)}
            />
            <span>15 questions</span>
            <span className={styles.radioDescription}>Comprehensive (~15 min)</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="questionCount"
              checked={questionCount === 20}
              onChange={() => setQuestionCount(20)}
            />
            <span>20 questions</span>
            <span className={styles.radioDescription}>Deep dive (~20 min)</span>
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
              checked={timeAllocated === 5}
              onChange={() => setTimeAllocated(5)}
            />
            <span>5 minutes</span>
            <span className={styles.radioDescription}>Fast pace, 30s per question</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="timeAllocated"
              checked={timeAllocated === 10}
              onChange={() => setTimeAllocated(10)}
            />
            <span>10 minutes</span>
            <span className={styles.radioDescription}>Standard pace, 1 min per question</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="timeAllocated"
              checked={timeAllocated === 15}
              onChange={() => setTimeAllocated(15)}
            />
            <span>15 minutes</span>
            <span className={styles.radioDescription}>Relaxed pace, 90s per question</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="timeAllocated"
              checked={timeAllocated === 20}
              onChange={() => setTimeAllocated(20)}
            />
            <span>20 minutes</span>
            <span className={styles.radioDescription}>Thoughtful pace, 2 min per question</span>
          </label>
        </div>
      </div>

      <div className={styles.setupSection}>
        <label className={styles.setupLabel}>Answer Mode</label>
        <div className={styles.radioGroup}>
          <label className={styles.radioOption}>
            <input
              type="radio"
              name="answerMode"
              checked={answerMode === 'multiple-choice'}
              onChange={() => setAnswerMode('multiple-choice')}
            />
            <span>Multiple Choice</span>
            <span className={styles.radioDescription}>Select from answer options</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="answerMode"
              checked={answerMode === 'write-in'}
              onChange={() => setAnswerMode('write-in')}
            />
            <span>Write-in</span>
            <span className={styles.radioDescription}>Type your answer and self-assess</span>
          </label>
        </div>
      </div>

      <div className={styles.setupSection}>
        <label className={styles.setupLabel}>Question Category</label>
        <div className={styles.radioGroup}>
          <label className={styles.radioOption}>
            <input
              type="radio"
              name="category"
              checked={category === 'all'}
              onChange={() => setCategory('all')}
            />
            <span>All Categories</span>
            <span className={styles.radioDescription}>Mixed questions from all areas</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="category"
              checked={category === 'technology'}
              onChange={() => setCategory('technology')}
            />
            <span>Technology Selection</span>
            <span className={styles.radioDescription}>Database, cache, queue, storage choices</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="category"
              checked={category === 'concept'}
              onChange={() => setCategory('concept')}
            />
            <span>Core Concepts</span>
            <span className={styles.radioDescription}>CAP, ACID, consistency, sharding, replication</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="category"
              checked={category === 'pattern'}
              onChange={() => setCategory('pattern')}
            />
            <span>Design Patterns</span>
            <span className={styles.radioDescription}>Circuit breaker, Saga, CQRS, Event Sourcing</span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="category"
              checked={category === 'numbers'}
              onChange={() => setCategory('numbers')}
            />
            <span>Numbers to Know</span>
            <span className={styles.radioDescription}>Latencies, throughput, scale estimates</span>
          </label>
        </div>
      </div>

      <div className={styles.setupActions}>
        <button
          className={styles.startButton}
          onClick={handleStart}
          disabled={loading}
        >
          {loading ? "Loading..." : "Start Quiz"}
        </button>
      </div>

      <div className={styles.setupInfo}>
        <h4>How It Works</h4>
        <ul>
          <li>
            <strong>Answer:</strong> Type your answer in the text field
          </li>
          <li>
            <strong>Reveal:</strong> Click to see the correct answer
          </li>
          <li>
            <strong>Self-Assess:</strong> Mark yourself correct or incorrect
          </li>
          <li>
            <strong>Learn:</strong> Review key points and explanations
          </li>
        </ul>
      </div>
    </div>
  );
}
