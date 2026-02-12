'use client'

import { useEffect } from 'react'
import { Tool } from '@/lib/api'
import styles from './ToolModal.module.css'

interface ToolModalProps {
  tool: Tool
  onClose: () => void
}

export default function ToolModal({ tool, onClose }: ToolModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    document.addEventListener('keydown', handleEscape)
    document.body.style.overflow = 'hidden'

    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [onClose])

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <div>
            <h1 className={styles.toolName}>{tool.name}</h1>
            <div className={styles.badges}>
              <span className={styles.categoryBadge}>{tool.category}</span>
              {tool.cap_leaning && (
                <span className={styles.badge}>{tool.cap_leaning}</span>
              )}
              {tool.consistency_model && (
                <span className={styles.badge}>{tool.consistency_model}</span>
              )}
            </div>
          </div>
          <button className={styles.closeButton} onClick={onClose} aria-label="Close modal">
            ✕
          </button>
        </div>

        <div className={styles.modalBody}>
          {tool.interview_oneliner && (
            <div className={styles.section}>
              <div className={styles.oneliner}>
                <p>{tool.interview_oneliner}</p>
              </div>
            </div>
          )}

          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>✓ Best Used For</h3>
            <div className={styles.sectionContent}>
              {tool.best_for?.split('\n').map((line, i) => (
                <p key={i} className={styles.contentLine}>{line}</p>
              )) || <p className={styles.emptyContent}>Not specified</p>}
            </div>
          </div>

          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>✗ Avoid When</h3>
            <div className={styles.sectionContent}>
              {tool.avoid_when?.split('\n').map((line, i) => (
                <p key={i} className={styles.contentLine}>{line}</p>
              )) || <p className={styles.emptyContent}>Not specified</p>}
            </div>
          </div>

          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>⚖️ Key Tradeoffs</h3>
            <div className={styles.sectionContent}>
              {tool.tradeoffs?.split('\n').map((line, i) => (
                <p key={i} className={styles.contentLine}>{line}</p>
              )) || <p className={styles.emptyContent}>Not specified</p>}
            </div>
          </div>

          {tool.scaling_pattern && (
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>📈 Scaling Pattern</h3>
              <div className={styles.sectionContent}>
                <p className={styles.contentLine}>{tool.scaling_pattern}</p>
              </div>
            </div>
          )}

          {(tool.official_docs_url || tool.deep_dive_url_1 || tool.deep_dive_url_2) && (
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>🔗 Resources</h3>
              <div className={styles.linkList}>
                {tool.official_docs_url && (
                  <a
                    href={tool.official_docs_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={styles.link}
                  >
                    Official Documentation →
                  </a>
                )}
                {tool.deep_dive_url_1 && (
                  <a
                    href={tool.deep_dive_url_1}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={styles.link}
                  >
                    Deep Dive 1 →
                  </a>
                )}
                {tool.deep_dive_url_2 && (
                  <a
                    href={tool.deep_dive_url_2}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={styles.link}
                  >
                    Deep Dive 2 →
                  </a>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
