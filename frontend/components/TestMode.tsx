"use client";

import { useState, useEffect } from "react";
import { getTestScenario } from "@/lib/api";
import type { TestScenario } from "@/lib/api";
import {
  TestSession,
  TestDesign,
  generateSessionId,
  saveActiveTestSession,
  getActiveTestSession,
  clearActiveTestSession,
  saveTestSession,
  AssessmentScores,
} from "@/lib/quizStorage";
import TestSetup from "./TestSetup";
import TestDesignCanvas from "./TestDesignCanvas";
import TestAssessment from "./TestAssessment";
import TestResults from "./TestResults";
import TestHistory from "./TestHistory";
import styles from "./TestMode.module.css";

type TestScreen = "setup" | "design" | "assessment" | "results" | "history";

export default function TestMode() {
  const [isOpen, setIsOpen] = useState(false);
  const [screen, setScreen] = useState<TestScreen>("setup");
  const [session, setSession] = useState<TestSession | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      const activeSession = getActiveTestSession();
      if (activeSession && !activeSession.completed) {
        setSession(activeSession);
        setScreen("design");
      }
    }
  }, [isOpen]);

  const handleStartTest = async (
    scenarioType: string | null,
    timeAllocated: number
  ) => {
    setLoading(true);
    try {
      const scenario = await getTestScenario(scenarioType || undefined);
      const emptyDesign: TestDesign = {
        functionalRequirements: [],
        nonFunctionalRequirements: [],
        outOfScope: [],
        entities: [],
        apiEndpoints: [],
        highLevelDesign: "",
        components: [],
        deepDives: [],
        tradeoffs: "",
        scalingConsiderations: "",
        failureModes: "",
      };

      const newSession: TestSession = {
        id: generateSessionId(),
        date: new Date().toISOString(),
        mode: 'test',
        scenario,
        design: emptyDesign,
        timeAllocated,
        timeTaken: 0,
        completed: false,
      };

      setSession(newSession);
      saveActiveTestSession(newSession);
      setScreen("design");
    } catch (error) {
      console.error("Failed to load test scenario:", error);
      alert("Failed to load test scenario. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleFinishDesign = (timeTaken: number) => {
    if (!session) return;

    const updatedSession = { ...session, timeTaken };
    setSession(updatedSession);
    saveActiveTestSession(updatedSession);
    setScreen("assessment");
  };

  const handleAssessmentComplete = (scores: AssessmentScores) => {
    if (!session) return;

    const completedSession: TestSession = {
      ...session,
      assessmentScores: scores,
      completed: true,
    };

    setSession(completedSession);
    saveTestSession(completedSession);
    clearActiveTestSession();
    setScreen("results");
  };

  const handleViewHistory = () => {
    setScreen("history");
  };

  const handleReviewSession = (reviewSession: TestSession) => {
    setSession(reviewSession);
    setScreen("results");
  };

  const handleStartNewTest = () => {
    setSession(null);
    clearActiveTestSession();
    setScreen("setup");
  };

  const closeModal = () => {
    if (screen === "design" && session && !session.completed) {
      const confirmClose = window.confirm(
        "You have an active test in progress. Your progress will be saved. Do you want to close?"
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
        📝 Test Mode
      </button>

      {isOpen && (
        <div className={styles.modal} onClick={closeModal}>
          <div
            className={styles.modalContent}
            onClick={(e) => e.stopPropagation()}
          >
            <div className={styles.modalHeader}>
              <h2>
                {screen === "setup" && "Test Mode Setup"}
                {screen === "design" && "System Design Test"}
                {screen === "assessment" && "Self-Assessment"}
                {screen === "results" && "Test Results"}
                {screen === "history" && "Test History"}
              </h2>
              <button className={styles.closeButton} onClick={closeModal}>
                ✕
              </button>
            </div>

            <div className={styles.modalBody}>
              {screen === "setup" && (
                <TestSetup onStart={handleStartTest} loading={loading} />
              )}

              {screen === "design" && session && (
                <TestDesignCanvas
                  session={session}
                  onUpdateSession={setSession}
                  onFinish={handleFinishDesign}
                />
              )}

              {screen === "assessment" && session && (
                <TestAssessment
                  session={session}
                  onComplete={handleAssessmentComplete}
                />
              )}

              {screen === "results" && session && (
                <TestResults
                  session={session}
                  onStartNew={handleStartNewTest}
                  onViewHistory={handleViewHistory}
                />
              )}

              {screen === "history" && (
                <TestHistory
                  onReview={handleReviewSession}
                  onStartNew={handleStartNewTest}
                />
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
