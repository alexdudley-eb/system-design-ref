"use client";

import { useState, useEffect, useCallback } from "react";
import {
  FlashcardSession,
  FlashcardAnswer,
  saveActiveFlashcardSession,
} from "@/lib/quizStorage";
import QuizTimer from "./QuizTimer";
import styles from "./QuizMeMode.module.css";

interface FlashcardQuestionProps {
  session: FlashcardSession;
  currentIndex: number;
  onIndexChange: (index: number) => void;
  onUpdateSession: (session: FlashcardSession) => void;
  onFinish: (timeTaken: number) => void;
}

export default function FlashcardQuestion({
  session,
  currentIndex,
  onIndexChange,
  onUpdateSession,
  onFinish,
}: FlashcardQuestionProps) {
  const [userAnswer, setUserAnswer] = useState("");
  const [isRevealed, setIsRevealed] = useState(false);
  const [isAnswered, setIsAnswered] = useState(false);
  const [timeTaken, setTimeTaken] = useState(0);

  const hasValidSession =
    session?.flashcards &&
    Array.isArray(session.flashcards) &&
    session.flashcards.length > 0;
  const hasValidIndex =
    hasValidSession &&
    currentIndex >= 0 &&
    currentIndex < session.flashcards.length;
  const currentCard = hasValidIndex ? session.flashcards[currentIndex] : null;

  useEffect(() => {
    if (!currentCard) return;

    const answer = session.answers[currentCard.id];
    if (answer) {
      setUserAnswer(answer.userAnswer);
      setIsRevealed(true);
      setIsAnswered(true);
    } else {
      setUserAnswer("");
      setIsRevealed(false);
      setIsAnswered(false);
    }
  }, [currentIndex, currentCard?.id, session.answers]);

  if (!hasValidSession) {
    return (
      <div className={styles.quizContainer}>
        <div className={styles.errorMessage}>
          <p>No flashcards available. Please start a new quiz.</p>
        </div>
      </div>
    );
  }

  if (!hasValidIndex || !currentCard) {
    return (
      <div className={styles.quizContainer}>
        <div className={styles.errorMessage}>
          <p>Invalid question index. Please restart the quiz.</p>
        </div>
      </div>
    );
  }

  const handleReveal = () => {
    setIsRevealed(true);

    const hasOptions = currentCard.options && currentCard.options.length > 0;

    if (
      session.answerMode === "multiple-choice" &&
      hasOptions &&
      currentCard.correct_answer
    ) {
      const isCorrect = userAnswer === currentCard.correct_answer;
      const answer: FlashcardAnswer = {
        questionId: currentCard.id,
        userAnswer,
        isCorrect,
        selfAssessed: false,
      };

      const updatedSession = {
        ...session,
        answers: {
          ...session.answers,
          [currentCard.id]: answer,
        },
      };

      setIsAnswered(true);
      onUpdateSession(updatedSession);
      saveActiveFlashcardSession(updatedSession);
    }
  };

  const handleMarkCorrect = (isCorrect: boolean) => {
    const hasOptions = currentCard.options && currentCard.options.length > 0;
    const effectiveAnswerMode =
      session.answerMode === "multiple-choice" && hasOptions
        ? "multiple-choice"
        : "write-in";

    const answer: FlashcardAnswer = {
      questionId: currentCard.id,
      userAnswer,
      isCorrect,
      selfAssessed: effectiveAnswerMode === "write-in",
    };

    const updatedSession = {
      ...session,
      answers: {
        ...session.answers,
        [currentCard.id]: answer,
      },
    };

    setIsAnswered(true);
    onUpdateSession(updatedSession);
    saveActiveFlashcardSession(updatedSession);
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      onIndexChange(currentIndex - 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < session.flashcards.length - 1) {
      onIndexChange(currentIndex + 1);
    }
  };

  const handleTick = (secondsElapsed: number) => {
    setTimeTaken(secondsElapsed);
  };

  const handleTimeUp = () => {
    onFinish(timeTaken);
  };

  const handleManualFinish = () => {
    onFinish(timeTaken);
  };

  const isLastCard = currentIndex === session.flashcards.length - 1;
  const allAnswered =
    Object.keys(session.answers).length === session.flashcards.length;

  const hasOptions = currentCard.options && currentCard.options.length > 0;
  const effectiveAnswerMode =
    session.answerMode === "multiple-choice" && hasOptions
      ? "multiple-choice"
      : "write-in";

  return (
    <div className={styles.quizContainer}>
      <div className={styles.quizHeader}>
        <div className={styles.quizProgress}>
          <span className={styles.questionNumber}>
            Question {currentIndex + 1} of {session.flashcards.length}
          </span>
          <span className={styles.questionType}>{currentCard.category}</span>
        </div>
        <QuizTimer
          sessionId={session.id}
          totalSeconds={session.timeAllocated * 60}
          onTimeUp={handleTimeUp}
          onTick={handleTick}
        />
      </div>

      <div className={styles.questionContent}>
        <div className={styles.flashcardContainer}>
          <div className={styles.questionCategory}>{currentCard.category}</div>
          <h3 className={styles.questionText}>{currentCard.question}</h3>

          {effectiveAnswerMode === "write-in" ? (
            <>
              <div className={styles.answerSection}>
                <label className={styles.answerLabel}>Your Answer:</label>
                <textarea
                  className={styles.answerTextarea}
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Type your answer here..."
                  rows={3}
                  disabled={isAnswered}
                />
                <p className={styles.answerHint}>
                  Write what you know, then reveal to check
                </p>
              </div>

              {!isRevealed && !isAnswered && (
                <button
                  className={styles.revealButton}
                  onClick={handleReveal}
                  disabled={!userAnswer.trim()}
                >
                  Reveal Answer
                </button>
              )}
            </>
          ) : (
            <>
              <div className={styles.multipleChoiceSection}>
                <label className={styles.answerLabel}>
                  Select Your Answer:
                </label>
                <div className={styles.optionsContainer}>
                  {currentCard.options?.map((option: any) => (
                    <label
                      key={option.id}
                      className={`${styles.optionLabel} ${
                        userAnswer === option.id ? styles.optionSelected : ""
                      }`}
                    >
                      <input
                        type="radio"
                        name="answer"
                        value={option.id}
                        checked={userAnswer === option.id}
                        onChange={(e) => setUserAnswer(e.target.value)}
                        disabled={isAnswered}
                      />
                      <span className={styles.optionText}>{option.text}</span>
                    </label>
                  ))}
                </div>
              </div>

              {!isRevealed && !isAnswered && (
                <button
                  className={styles.revealButton}
                  onClick={handleReveal}
                  disabled={!userAnswer}
                >
                  Submit Answer
                </button>
              )}
            </>
          )}

          {isRevealed && (
            <div className={styles.answerReveal}>
              <div className={styles.correctAnswer}>
                <h4>Correct Answer:</h4>
                <p>{currentCard.answer}</p>
              </div>

              {currentCard.key_points && currentCard.key_points.length > 0 && (
                <div className={styles.keyPoints}>
                  <h4>Key Points:</h4>
                  <ul>
                    {currentCard.key_points.map(
                      (point: string, idx: number) => (
                        <li key={idx}>{point}</li>
                      ),
                    )}
                  </ul>
                </div>
              )}

              {currentCard.explanation && (
                <div className={styles.explanation}>
                  <h4>Explanation:</h4>
                  <p>{currentCard.explanation}</p>
                </div>
              )}

              {currentCard.context && (
                <div className={styles.context}>
                  <h4>Context:</h4>
                  <p>{currentCard.context}</p>
                </div>
              )}

              {currentCard.comparison && (
                <div className={styles.comparison}>
                  <h4>Comparison:</h4>
                  <ul>
                    {Object.entries(currentCard.comparison).map(
                      ([key, value]) => (
                        <li key={key}>
                          <strong>{key}:</strong> {value as string}
                        </li>
                      ),
                    )}
                  </ul>
                </div>
              )}

              {!isAnswered && (
                <div className={styles.selfAssessment}>
                  <p className={styles.assessmentPrompt}>
                    Did you get it right?
                  </p>
                  <div className={styles.assessmentButtons}>
                    <button
                      className={styles.incorrectButton}
                      onClick={() => handleMarkCorrect(false)}
                    >
                      ✗ Incorrect
                    </button>
                    <button
                      className={styles.correctButton}
                      onClick={() => handleMarkCorrect(true)}
                    >
                      ✓ Correct
                    </button>
                  </div>
                </div>
              )}

              {isAnswered && (
                <div className={styles.answeredBadge}>
                  {session.answers[currentCard.id]?.isCorrect ? (
                    <span className={styles.correctBadge}>
                      ✓ Marked Correct
                    </span>
                  ) : (
                    <span className={styles.incorrectBadge}>
                      ✗ Marked Incorrect
                    </span>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <div className={styles.quizNavigation}>
        <div className={styles.navLeft}>
          <button
            className={styles.navButton}
            onClick={handlePrevious}
            disabled={currentIndex === 0}
          >
            ← Previous
          </button>
        </div>

        <div className={styles.navCenter}>
          <div className={styles.progressDots}>
            {session.flashcards.map((_, idx) => (
              <button
                key={idx}
                className={`${styles.progressDot} ${
                  idx === currentIndex ? styles.dotActive : ""
                } ${session.answers[session.flashcards[idx].id] ? styles.dotAnswered : ""}`}
                onClick={() => onIndexChange(idx)}
                aria-label={`Go to question ${idx + 1}`}
              />
            ))}
          </div>
        </div>

        <div className={styles.navRight}>
          {!isLastCard && (
            <button className={styles.navButton} onClick={handleNext}>
              Next →
            </button>
          )}
          {isLastCard && allAnswered && (
            <button
              className={styles.finishButton}
              onClick={handleManualFinish}
            >
              Finish Quiz
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
