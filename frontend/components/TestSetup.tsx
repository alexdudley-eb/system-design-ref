"use client";

import React, { useState } from "react";
import styles from "./TestMode.module.css";

interface TestSetupProps {
  onStart: (scenarioType: string | null, timeAllocated: number) => void;
  loading?: boolean;
}

export default function TestSetup({ onStart, loading }: TestSetupProps) {
  const [scenarioType, setScenarioType] = useState<string | null>(null);
  const [timeAllocated, setTimeAllocated] = useState(45);

  const handleStart = () => {
    onStart(scenarioType, timeAllocated);
  };

  return (
    <div className={styles.setupContainer}>
      <div className={styles.setupSection}>
        <h3>System Design Interview Simulation</h3>
        <p className={styles.setupDescription}>
          Test yourself under real interview conditions. You'll receive only the
          scenario title, description, scale requirements, and hints. Fill in
          all design aspects yourself: requirements, entities, API, and
          architecture.
        </p>
      </div>

      <div className={styles.setupSection}>
        <label className={styles.setupLabel}>Choose Scenario</label>
        <div className={styles.radioGroup}>
          <label className={styles.radioOption}>
            <input
              type="radio"
              name="scenarioType"
              checked={scenarioType === null}
              onChange={() => setScenarioType(null)}
            />
            <span>Random Scenario</span>
            <span className={styles.radioDescription}>
              Surprise me with any system
            </span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="scenarioType"
              checked={scenarioType === "uber"}
              onChange={() => setScenarioType("uber")}
            />
            <span>Ride Sharing (Uber/Lyft)</span>
            <span className={styles.radioDescription}>
              High-scale, real-time matching
            </span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="scenarioType"
              checked={scenarioType === "whatsapp"}
              onChange={() => setScenarioType("whatsapp")}
            />
            <span>Chat Messenger (WhatsApp)</span>
            <span className={styles.radioDescription}>
              Messaging, presence, delivery
            </span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="scenarioType"
              checked={scenarioType === "instagram"}
              onChange={() => setScenarioType("instagram")}
            />
            <span>Social Media Feed (Instagram)</span>
            <span className={styles.radioDescription}>
              Media upload, feed generation
            </span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="scenarioType"
              checked={scenarioType === "url_shortener"}
              onChange={() => setScenarioType("url_shortener")}
            />
            <span>URL Shortener</span>
            <span className={styles.radioDescription}>
              High-throughput key generation
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
              checked={timeAllocated === 30}
              onChange={() => setTimeAllocated(30)}
            />
            <span>30 minutes</span>
            <span className={styles.radioDescription}>
              Quick iteration practice
            </span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="timeAllocated"
              checked={timeAllocated === 45}
              onChange={() => setTimeAllocated(45)}
            />
            <span>45 minutes</span>
            <span className={styles.radioDescription}>
              Standard interview length
            </span>
          </label>

          <label className={styles.radioOption}>
            <input
              type="radio"
              name="timeAllocated"
              checked={timeAllocated === 60}
              onChange={() => setTimeAllocated(60)}
            />
            <span>60 minutes</span>
            <span className={styles.radioDescription}>Extended deep dive</span>
          </label>
        </div>
      </div>

      <div className={styles.setupActions}>
        <button
          className={styles.startButton}
          onClick={handleStart}
          disabled={loading}
        >
          {loading ? "Loading..." : "Start Test"}
        </button>
      </div>

      <div className={styles.setupInfo}>
        <h4>Test Structure</h4>
        <ul>
          <li>
            <strong>Phase 1 (5-10 min):</strong> Clarify requirements
          </li>
          <li>
            <strong>Phase 2 (10-15 min):</strong> Define entities and API
          </li>
          <li>
            <strong>Phase 3 (15-20 min):</strong> Design high-level architecture
          </li>
          <li>
            <strong>Phase 4 (10-15 min):</strong> Deep dives and tradeoffs
          </li>
        </ul>
      </div>
    </div>
  );
}
