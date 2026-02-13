"use client";

import { useState, useEffect } from "react";
import { QuizSession, QuizAnswer, saveActiveSession } from "@/lib/quizStorage";
import QuizTimer from "./QuizTimer";
import ScenarioDetail from "./ScenarioDetail";
import styles from "./PracticeMode.module.css";

interface QuizQuestionProps {
  session: QuizSession;
  currentIndex: number;
  onIndexChange: (index: number) => void;
  onUpdateSession: (session: QuizSession) => void;
  onFinish: (timeTaken: number) => void;
}

export default function QuizQuestion({
  session,
  currentIndex,
  onIndexChange,
  onUpdateSession,
  onFinish,
}: QuizQuestionProps) {
  const [selectedAnswer, setSelectedAnswer] = useState<string>("");
  const [notes, setNotes] = useState<string>("");
  const [timeTaken, setTimeTaken] = useState(0);

  const currentQuestion = session.questions[currentIndex];
  const totalQuestions = session.questions.length;

  useEffect(() => {
    const existingAnswer = session.answers[currentQuestion.id];
    if (existingAnswer) {
      setSelectedAnswer(existingAnswer.selectedAnswer || "");
      setNotes(existingAnswer.notes || "");
    } else {
      setSelectedAnswer("");
      setNotes("");
    }
  }, [currentIndex, currentQuestion.id, session.answers]);

  const saveCurrentAnswer = () => {
    const answer: QuizAnswer = {
      questionId: currentQuestion.id,
      selectedAnswer: selectedAnswer || undefined,
      notes: notes || undefined,
    };

    const updatedSession = {
      ...session,
      answers: {
        ...session.answers,
        [currentQuestion.id]: answer,
      },
    };

    onUpdateSession(updatedSession);
    saveActiveSession(updatedSession);
  };

  const handleNext = () => {
    saveCurrentAnswer();
    if (currentIndex < totalQuestions - 1) {
      onIndexChange(currentIndex + 1);
    }
  };

  const handlePrevious = () => {
    saveCurrentAnswer();
    if (currentIndex > 0) {
      onIndexChange(currentIndex - 1);
    }
  };

  const handleFinish = () => {
    saveCurrentAnswer();

    const allAnswered = session.questions.every(
      (q) => session.answers[q.id] || currentQuestion.id === q.id,
    );

    if (!allAnswered) {
      const confirmFinish = window.confirm(
        "You haven't answered all questions. Do you want to finish the quiz anyway?",
      );
      if (!confirmFinish) return;
    }

    onFinish(timeTaken);
  };

  const handleTimeUp = () => {
    saveCurrentAnswer();
    alert("Time's up! Moving to self-assessment.");
    onFinish(session.timeAllocated * 60);
  };

  return (
    <div className={styles.quizContainer}>
      <div className={styles.quizHeader}>
        <div className={styles.quizProgress}>
          <span className={styles.questionNumber}>
            Question {currentIndex + 1} of {totalQuestions}
          </span>
          <span className={styles.questionType}>
            {currentQuestion.type === "scenario"
              ? "📊 Scenario"
              : "💡 Technology Selection"}
          </span>
        </div>

        <QuizTimer
          sessionId={session.id}
          totalSeconds={session.timeAllocated * 60}
          onTimeUp={handleTimeUp}
          onTick={setTimeTaken}
        />
      </div>

      <div className={styles.questionContent}>
        {currentQuestion.type === "technology" && (
          <div className={styles.techQuestion}>
            <div className={styles.questionCategory}>
              {currentQuestion.category}
            </div>
            <h3 className={styles.questionText}>{currentQuestion.question}</h3>

            <div className={styles.optionsContainer}>
              {currentQuestion.options?.map((option) => (
                <label
                  key={option.id}
                  className={`${styles.optionLabel} ${
                    selectedAnswer === option.id ? styles.optionSelected : ""
                  }`}
                >
                  <input
                    type="radio"
                    name="answer"
                    value={option.id}
                    checked={selectedAnswer === option.id}
                    onChange={(e) => setSelectedAnswer(e.target.value)}
                  />
                  <span className={styles.optionText}>{option.text}</span>
                </label>
              ))}
            </div>

            <div className={styles.notesSection}>
              <label htmlFor="notes">Your Notes & Reasoning:</label>
              <textarea
                id="notes"
                className={styles.notesTextarea}
                placeholder="Explain your choice, discuss trade-offs, mention alternatives..."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={4}
              />
            </div>
          </div>
        )}

        {currentQuestion.type === "scenario" && currentQuestion.scenario && (
          <div className={styles.scenarioQuestion}>
            <h3 className={styles.questionText}>{currentQuestion.question}</h3>
            <p className={styles.scenarioInstructions}>
              Design the system architecture below. Think through the
              requirements, draw diagrams (on paper/whiteboard), and document
              your approach in the notes section.
            </p>

            <div className={styles.scenarioDetailWrapper}>
              <ScenarioDetail data={currentQuestion.scenario} />
            </div>

            <div className={styles.notesSection}>
              <label htmlFor="notes">Your Design Notes:</label>
              <textarea
                id="notes"
                className={styles.notesTextarea}
                placeholder="Document your approach: requirements, entities, high-level design, deep dives, trade-offs..."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={8}
              />
              <p className={styles.notesHint}>
                Tip: Follow the Delivery Framework - Requirements → High-Level
                Design → Deep Dives → Trade-offs
              </p>
            </div>
          </div>
        )}
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
            {session.questions.map((q, idx) => (
              <button
                key={q.id}
                className={`${styles.progressDot} ${
                  idx === currentIndex ? styles.dotActive : ""
                } ${session.answers[q.id] ? styles.dotAnswered : ""}`}
                onClick={() => {
                  saveCurrentAnswer();
                  onIndexChange(idx);
                }}
                title={`Question ${idx + 1}`}
              />
            ))}
          </div>
        </div>

        <div className={styles.navRight}>
          {currentIndex < totalQuestions - 1 ? (
            <button className={styles.navButton} onClick={handleNext}>
              Next →
            </button>
          ) : (
            <button className={styles.finishButton} onClick={handleFinish}>
              Finish Quiz
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
