'use client'

import styles from './ModeToggle.module.css'

interface ModeToggleProps {
  interviewMode: boolean
  onToggle: () => void
}

export default function ModeToggle({ interviewMode, onToggle }: ModeToggleProps) {
  return (
    <div className={styles.modeToggle}>
      <span className={styles.label}>Mode:</span>
      <button
        className={`${styles.toggleButton} ${
          interviewMode ? styles.toggleButtonActive : ''
        }`}
        onClick={onToggle}
        aria-label={`Switch to ${interviewMode ? 'study' : 'interview'} mode`}
      >
        <span className={styles.toggleOption}>
          {interviewMode ? '🎯 Interview' : '📚 Study Mode'}
        </span>
      </button>
      <span className={styles.hint}>(Cmd+I)</span>
    </div>
  )
}
