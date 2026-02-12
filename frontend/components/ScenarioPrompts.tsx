"use client";

import { useState } from "react";
import { ScenarioResponse } from "@/lib/api";
import { getScenarioSuggestions } from "@/lib/api";
import ScenarioDetail from "./ScenarioDetail";
import styles from "./ScenarioPrompts.module.css";

const SCENARIOS = [
  { id: "payments", label: "Payments", icon: "💳" },
  { id: "chat", label: "Chat", icon: "💬" },
  { id: "feed", label: "Feed", icon: "📰" },
  { id: "analytics", label: "Analytics", icon: "📊" },
  { id: "search", label: "Search", icon: "🔍" },
  { id: "auth", label: "Auth", icon: "🔐" },
  { id: "uber", label: "Uber", icon: "🚗" },
  { id: "bitly", label: "URL Shortener", icon: "🔗" },
  { id: "dropbox", label: "Dropbox", icon: "📦" },
  { id: "ratelimiter", label: "Rate Limiter", icon: "🚦" },
  { id: "whatsapp", label: "WhatsApp", icon: "📱" },
  { id: "youtube", label: "YouTube", icon: "▶️" },
  { id: "ticketmaster", label: "TicketMaster", icon: "🎟️" },
];

export default function ScenarioPrompts() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
  const [scenarioData, setScenarioData] = useState<ScenarioResponse | null>(
    null,
  );
  const [loading, setLoading] = useState(false);

  const handleScenarioSelect = async (scenarioId: string) => {
    if (selectedScenario === scenarioId) return;

    setLoading(true);
    setSelectedScenario(scenarioId);

    try {
      const data = await getScenarioSuggestions(scenarioId);
      setScenarioData(data);
    } catch (error) {
      console.error("Failed to load scenario:", error);
    } finally {
      setLoading(false);
    }
  };

  const closeModal = () => {
    setIsOpen(false);
    setSelectedScenario(null);
    setScenarioData(null);
  };

  return (
    <>
      <button className={styles.triggerButton} onClick={() => setIsOpen(true)}>
        💡 Scenarios
      </button>

      {isOpen && (
        <div className={styles.modal} onClick={closeModal}>
          <div
            className={styles.modalContent}
            onClick={(e) => e.stopPropagation()}
          >
            <div className={styles.modalHeader}>
              <h2>System Design Scenarios</h2>
              <button className={styles.closeButton} onClick={closeModal}>
                ✕
              </button>
            </div>

            <div className={styles.scenarioGrid}>
              {SCENARIOS.map((scenario) => (
                <button
                  key={scenario.id}
                  className={`${styles.scenarioCard} ${
                    selectedScenario === scenario.id
                      ? styles.scenarioCardActive
                      : ""
                  }`}
                  onClick={() => handleScenarioSelect(scenario.id)}
                >
                  <span className={styles.scenarioIcon}>{scenario.icon}</span>
                  <span className={styles.scenarioLabel}>{scenario.label}</span>
                </button>
              ))}
            </div>

            {loading && (
              <div className={styles.loadingState}>Loading scenario...</div>
            )}

            {scenarioData && !loading && (
              <div className={styles.detailContainer}>
                <ScenarioDetail data={scenarioData} />
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}
