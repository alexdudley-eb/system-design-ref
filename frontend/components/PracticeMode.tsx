"use client";

import { useState, useEffect } from "react";
import { getQuizQuestions } from "@/lib/api";
import type { QuizQuestion } from "@/lib/api";
import {
  QuizSession,
  generateSessionId,
  saveActiveSession,
  getActiveSession,
  clearActiveSession,
  saveQuizSession,
  AssessmentScores,
} from "@/lib/quizStorage";
import QuizSetup from "./QuizSetup";
import QuizQuestionView from "./QuizQuestion";
import QuizAssessment from "./QuizAssessment";
import QuizResults from "./QuizResults";
import QuizHistory from "./QuizHistory";
import styles from "./PracticeMode.module.css";

type QuizScreen = "setup" | "quiz" | "assessment" | "results" | "history";

export default function PracticeMode() {
  const [isOpen, setIsOpen] = useState(false);
  const [screen, setScreen] = useState<QuizScreen>("setup");
  const [session, setSession] = useState<QuizSession | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      const activeSession = getActiveSession();
      if (activeSession && !activeSession.completed) {
        setSession(activeSession);
        setScreen("quiz");
        setCurrentQuestionIndex(
          Object.keys(activeSession.answers || {}).length
        );
      }
    }
  }, [isOpen]);

  const handleStartQuiz = async (
    questionCount: number,
    timeAllocated: number
  ) => {
    setLoading(true);
    try {
      const response = await getQuizQuestions(questionCount);
      const newSession: QuizSession = {
        id: generateSessionId(),
        date: new Date().toISOString(),
        mode: 'practice',
        questions: response.questions,
        answers: {},
        timeAllocated,
        timeTaken: 0,
        completed: false,
      };

      setSession(newSession);
      saveActiveSession(newSession);
      setScreen("quiz");
      setCurrentQuestionIndex(0);
    } catch (error) {
      console.error("Failed to load quiz questions:", error);
      alert("Failed to load quiz questions. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleFinishQuiz = (timeTaken: number) => {
    if (!session) return;

    const updatedSession = { ...session, timeTaken };
    setSession(updatedSession);
    saveActiveSession(updatedSession);
    setScreen("assessment");
  };

  const handleAssessmentComplete = (scores: AssessmentScores) => {
    if (!session) return;

    const completedSession: QuizSession = {
      ...session,
      assessmentScores: scores,
      completed: true,
    };

    setSession(completedSession);
    saveQuizSession(completedSession);
    clearActiveSession();
    setScreen("results");
  };

  const handleViewHistory = () => {
    setScreen("history");
  };

  const handleReviewSession = (reviewSession: QuizSession) => {
    setSession(reviewSession);
    setScreen("results");
  };

  const handleStartNewQuiz = () => {
    setSession(null);
    setCurrentQuestionIndex(0);
    clearActiveSession();
    setScreen("setup");
  };

  const closeModal = () => {
    if (
      screen === "quiz" &&
      session &&
      !session.completed &&
      Object.keys(session.answers).length > 0
    ) {
      const confirmClose = window.confirm(
        "You have an active practice session in progress. Your progress will be saved. Do you want to close?"
      );
      if (!confirmClose) return;
    }

    setIsOpen(false);
    setTimeout(() => {
      if (screen === "results" || screen === "history") {
        setScreen("setup");
        setSession(null);
      }
    }, 300);
  };

  return (
    <>
      <button className={styles.triggerButton} onClick={() => setIsOpen(true)}>
        🔄 Practice Mode
      </button>

      {isOpen && (
        <div className={styles.modal} onClick={closeModal}>
          <div
            className={styles.modalContent}
            onClick={(e) => e.stopPropagation()}
          >
            <div className={styles.modalHeader}>
              <h2>
                {screen === "setup" && "Practice Mode Setup"}
                {screen === "quiz" && "Practice in Progress"}
                {screen === "assessment" && "Self-Assessment"}
                {screen === "results" && "Practice Results"}
                {screen === "history" && "Practice History"}
              </h2>
              <button className={styles.closeButton} onClick={closeModal}>
                ✕
              </button>
            </div>

            <div className={styles.modalBody}>
              {screen === "setup" && (
                <QuizSetup onStart={handleStartQuiz} loading={loading} />
              )}

              {screen === "quiz" && session && (
                <QuizQuestionView
                  session={session}
                  currentIndex={currentQuestionIndex}
                  onIndexChange={setCurrentQuestionIndex}
                  onUpdateSession={setSession}
                  onFinish={handleFinishQuiz}
                />
              )}

              {screen === "assessment" && session && (
                <QuizAssessment
                  session={session}
                  onComplete={handleAssessmentComplete}
                />
              )}

              {screen === "results" && session && (
                <QuizResults
                  session={session}
                  onStartNew={handleStartNewQuiz}
                  onViewHistory={handleViewHistory}
                />
              )}

              {screen === "history" && (
                <QuizHistory
                  onReview={handleReviewSession}
                  onStartNew={handleStartNewQuiz}
                />
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
