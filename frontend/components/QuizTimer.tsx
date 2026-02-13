"use client";

import { useState, useEffect, useRef } from "react";
import {
  formatTime,
  saveTimerState,
  getTimerState,
  calculateRemainingTime,
} from "@/lib/quizStorage";
import styles from "./PracticeMode.module.css";

interface QuizTimerProps {
  sessionId: string;
  totalSeconds: number;
  onTimeUp: () => void;
  onTick: (secondsElapsed: number) => void;
}

export default function QuizTimer({
  sessionId,
  totalSeconds,
  onTimeUp,
  onTick,
}: QuizTimerProps) {
  const [secondsRemaining, setSecondsRemaining] = useState(totalSeconds);
  const [isPaused, setIsPaused] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const secondsElapsedRef = useRef(0);
  const timerInitialized = useRef(false);

  useEffect(() => {
    if (timerInitialized.current) return;

    const savedStartTime = getTimerState(sessionId);
    if (savedStartTime) {
      const remaining = calculateRemainingTime(savedStartTime, totalSeconds);
      setSecondsRemaining(remaining);
      secondsElapsedRef.current = totalSeconds - remaining;
    } else {
      const startTime = Date.now();
      saveTimerState(sessionId, startTime);
    }

    timerInitialized.current = true;
  }, [sessionId, totalSeconds]);

  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        setIsPaused(true);
      } else {
        setIsPaused(false);
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, []);

  useEffect(() => {
    if (isPaused) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      return;
    }

    intervalRef.current = setInterval(() => {
      setSecondsRemaining((prev) => {
        const newValue = prev - 1;

        if (newValue <= 0) {
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
          }
          onTimeUp();
          return 0;
        }

        return newValue;
      });
    }, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isPaused, totalSeconds, onTimeUp]);

  useEffect(() => {
    const elapsed = totalSeconds - secondsRemaining;
    if (elapsed > 0) {
      onTick(elapsed);
    }
  }, [secondsRemaining, totalSeconds, onTick]);

  const minutes = Math.floor(secondsRemaining / 60);
  const seconds = secondsRemaining % 60;
  const isWarning = secondsRemaining <= 300;
  const isCritical = secondsRemaining <= 60;

  return (
    <div className={styles.timerContainer}>
      {isPaused && (
        <div className={styles.timerPausedBadge}>Paused (tab inactive)</div>
      )}
      <div
        className={`${styles.timer} ${isWarning ? styles.timerWarning : ""} ${
          isCritical ? styles.timerCritical : ""
        }`}
      >
        <span className={styles.timerIcon}>⏱</span>
        <span className={styles.timerText}>{formatTime(secondsRemaining)}</span>
      </div>
      {isWarning && !isCritical && (
        <span className={styles.timerWarningText}>5 minutes remaining</span>
      )}
      {isCritical && (
        <span className={styles.timerCriticalText}>Final minute!</span>
      )}
    </div>
  );
}
