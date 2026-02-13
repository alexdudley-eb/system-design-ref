"use client";

import { useState, useEffect } from "react";
import { getFlashcardSet } from "@/lib/api";
import type { FlashcardQuestion } from "@/lib/api";
import {
  FlashcardSession,
  generateSessionId,
  saveActiveFlashcardSession,
  getActiveFlashcardSession,
  clearActiveFlashcardSession,
  saveFlashcardSession,
} from "@/lib/quizStorage";
import {
  getQuestionsForReview,
  updateQuestionPerformance,
} from "@/lib/spacedRepetition";
import FlashcardSetup from "./FlashcardSetup";
import FlashcardQuestionView from "./FlashcardQuestion";
import FlashcardResults from "./FlashcardResults";
import FlashcardHistory from "./FlashcardHistory";
import styles from "./QuizMeMode.module.css";

type FlashcardScreen = "setup" | "flashcards" | "results" | "history";

export default function QuizMeMode() {
  const [isOpen, setIsOpen] = useState(false);
  const [screen, setScreen] = useState<FlashcardScreen>("setup");
  const [session, setSession] = useState<FlashcardSession | null>(null);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      const activeSession = getActiveFlashcardSession();
      if (activeSession && !activeSession.completed) {
        setSession(activeSession);
        setScreen("flashcards");
        setCurrentCardIndex(Object.keys(activeSession.answers || {}).length);
      }
    }
  }, [isOpen]);

  const handleStartQuiz = async (
    questionCount: number,
    timeAllocated: number,
    category: "all" | "technology" | "concept" | "pattern" | "numbers",
    answerMode: "multiple-choice" | "write-in",
  ) => {
    setLoading(true);
    try {
      const response = await getFlashcardSet(questionCount * 2, category);

      const allQuestionIds = response.questions.map((q) => q.id);
      const prioritizedIds = getQuestionsForReview(
        allQuestionIds,
        questionCount,
      );

      const selectedQuestions = prioritizedIds
        .map((id) => response.questions.find((q) => q.id === id))
        .filter((q): q is FlashcardQuestion => q !== undefined)
        .slice(0, questionCount);

      if (selectedQuestions.length < questionCount) {
        const remainingCount = questionCount - selectedQuestions.length;
        const usedIds = new Set(selectedQuestions.map((q) => q.id));
        const additionalQuestions = response.questions
          .filter((q) => !usedIds.has(q.id))
          .slice(0, remainingCount);
        selectedQuestions.push(...additionalQuestions);
      }

      const newSession: FlashcardSession = {
        version: 1,
        id: generateSessionId(),
        date: new Date().toISOString(),
        mode: "quiz",
        flashcards: selectedQuestions,
        answers: {},
        correctCount: 0,
        incorrectCount: 0,
        timeAllocated,
        timeTaken: 0,
        completed: false,
        answerMode,
      };

      setSession(newSession);
      saveActiveFlashcardSession(newSession);
      setScreen("flashcards");
      setCurrentCardIndex(0);
    } catch (error) {
      console.error("Failed to load flashcards:", error);
      alert("Failed to load flashcards. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleFinishQuiz = (timeTaken: number) => {
    if (!session) return;

    const correctCount = Object.values(session.answers).filter(
      (a) => a.isCorrect,
    ).length;
    const incorrectCount = Object.values(session.answers).filter(
      (a) => !a.isCorrect,
    ).length;

    Object.entries(session.answers).forEach(([questionId, answer]) => {
      updateQuestionPerformance(questionId, answer.isCorrect);
    });

    const completedSession: FlashcardSession = {
      ...session,
      timeTaken,
      correctCount,
      incorrectCount,
      completed: true,
    };

    setSession(completedSession);
    saveFlashcardSession(completedSession);
    clearActiveFlashcardSession();
    setScreen("results");
  };

  const handleViewHistory = () => {
    setScreen("history");
  };

  const handleReviewSession = (reviewSession: FlashcardSession) => {
    setSession(reviewSession);
    setScreen("results");
  };

  const handleStartNewQuiz = () => {
    setSession(null);
    setCurrentCardIndex(0);
    clearActiveFlashcardSession();
    setScreen("setup");
  };

  const closeModal = () => {
    if (
      screen === "flashcards" &&
      session &&
      !session.completed &&
      Object.keys(session.answers).length > 0
    ) {
      const confirmClose = window.confirm(
        "You have an active quiz session in progress. Your progress will be saved. Do you want to close?",
      );
      if (!confirmClose) return;
    }

    setIsOpen(false);
    setTimeout(() => {
      if (
        screen === "results" ||
        screen === "history" ||
        screen === "flashcards"
      ) {
        setScreen("setup");
        setSession(null);
      }
    }, 300);
  };

  return (
    <>
      <button className={styles.triggerButton} onClick={() => setIsOpen(true)}>
        🎯 Quiz Me
      </button>

      {isOpen && (
        <div className={styles.modal} onClick={closeModal}>
          <div
            className={styles.modalContent}
            onClick={(e) => e.stopPropagation()}
          >
            <div className={styles.modalHeader}>
              <h2>
                {screen === "setup" && "Quiz Me Setup"}
                {screen === "flashcards" && "Flashcard Quiz"}
                {screen === "results" && "Quiz Results"}
                {screen === "history" && "Quiz History"}
              </h2>
              <button className={styles.closeButton} onClick={closeModal}>
                ✕
              </button>
            </div>

            <div className={styles.modalBody}>
              {screen === "setup" && (
                <FlashcardSetup onStart={handleStartQuiz} loading={loading} />
              )}

              {screen === "flashcards" && session && (
                <FlashcardQuestionView
                  session={session}
                  currentIndex={currentCardIndex}
                  onIndexChange={setCurrentCardIndex}
                  onUpdateSession={setSession}
                  onFinish={handleFinishQuiz}
                />
              )}

              {screen === "results" && session && (
                <FlashcardResults
                  session={session}
                  onStartNew={handleStartNewQuiz}
                  onViewHistory={handleViewHistory}
                />
              )}

              {screen === "history" && (
                <FlashcardHistory
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
