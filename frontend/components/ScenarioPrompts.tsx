'use client'

import { useState } from 'react'
import { getScenarioSuggestions } from '@/lib/api'
import styles from './ScenarioPrompts.module.css'

const SCENARIOS = [
  { id: 'payments', label: 'Payments', icon: '💳' },
  { id: 'chat', label: 'Chat', icon: '💬' },
  { id: 'feed', label: 'Feed', icon: '📰' },
  { id: 'analytics', label: 'Analytics', icon: '📊' },
  { id: 'search', label: 'Search', icon: '🔍' },
  { id: 'auth', label: 'Auth', icon: '🔐' },
]

export default function ScenarioPrompts() {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null)
  const [scenarioData, setScenarioData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleScenarioSelect = async (scenarioId: string) => {
    setLoading(true)
    setSelectedScenario(scenarioId)
    
    try {
      const data = await getScenarioSuggestions(scenarioId)
      setScenarioData(data)
    } catch (error) {
      console.error('Failed to load scenario:', error)
    } finally {
      setLoading(false)
    }
  }

  const closeModal = () => {
    setIsOpen(false)
    setSelectedScenario(null)
    setScenarioData(null)
  }

  return (
    <>
      <button className={styles.triggerButton} onClick={() => setIsOpen(true)}>
        💡 Scenarios
      </button>

      {isOpen && (
        <div className={styles.modal} onClick={closeModal}>
          <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
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
                    selectedScenario === scenario.id ? styles.scenarioCardActive : ''
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
              <div className={styles.scenarioResult}>
                <h3>Recommended Stack</h3>
                <p className={styles.reasoning}>{scenarioData.reasoning}</p>
                
                <div className={styles.toolsList}>
                  {scenarioData.tools.map((tool: any) => (
                    <div key={tool.id} className={styles.toolChip}>
                      {tool.name}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  )
}
