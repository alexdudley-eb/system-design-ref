'use client'

import { useEffect, useState } from 'react'
import { Tool, ToolDetail as ToolDetailType, getToolDetail } from '@/lib/api'
import styles from './ToolDetail.module.css'

interface ToolDetailProps {
  tool: Tool
  interviewMode: boolean
}

export default function ToolDetail({ tool, interviewMode }: ToolDetailProps) {
  const [detailData, setDetailData] = useState<ToolDetailType | null>(null)
  const [loading, setLoading] = useState(false)
  const [copiedSkeleton, setCopiedSkeleton] = useState(false)

  useEffect(() => {
    async function fetchDetail() {
      setLoading(true)
      try {
        const data = await getToolDetail(tool.id)
        setDetailData(data)
      } catch (error) {
        console.error('Failed to fetch tool detail:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDetail()
  }, [tool.id])

  const copyAnswerSkeleton = () => {
    const skeleton = `
${tool.name}

${tool.interview_oneliner || ''}

Best used for:
${tool.best_for || 'N/A'}

Key tradeoffs:
${tool.tradeoffs || 'N/A'}

Avoid when:
${tool.avoid_when || 'N/A'}
    `.trim()

    navigator.clipboard.writeText(skeleton).then(() => {
      setCopiedSkeleton(true)
      setTimeout(() => setCopiedSkeleton(false), 2000)
    })
  }

  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}>Loading details...</div>
      </div>
    )
  }

  return (
    <div className={styles.toolDetail}>
      <div className={styles.header}>
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
        <button className={styles.copyButton} onClick={copyAnswerSkeleton}>
          {copiedSkeleton ? '✓ Copied!' : '📋 Copy Answer'}
        </button>
      </div>

      {tool.interview_oneliner && (
        <div className={styles.oneliner}>
          <h2>Interview One-liner</h2>
          <p className={styles.onelineText}>{tool.interview_oneliner}</p>
        </div>
      )}

      <div className={styles.section}>
        <h3>✓ Best Used For</h3>
        <div className={styles.content}>
          {tool.best_for?.split('\n').map((line, i) => (
            <p key={i}>{line}</p>
          )) || <p className={styles.emptyContent}>Not specified</p>}
        </div>
      </div>

      <div className={styles.section}>
        <h3>✗ Avoid When</h3>
        <div className={styles.content}>
          {tool.avoid_when?.split('\n').map((line, i) => (
            <p key={i}>{line}</p>
          )) || <p className={styles.emptyContent}>Not specified</p>}
        </div>
      </div>

      <div className={styles.section}>
        <h3>⚖ Key Tradeoffs</h3>
        <div className={styles.content}>
          {tool.tradeoffs?.split('\n').map((line, i) => (
            <p key={i}>{line}</p>
          )) || <p className={styles.emptyContent}>Not specified</p>}
        </div>
      </div>

      {tool.scaling_pattern && (
        <div className={styles.section}>
          <h3>📈 Scaling Pattern</h3>
          <div className={styles.content}>
            <p>{tool.scaling_pattern}</p>
          </div>
        </div>
      )}

      {!interviewMode && detailData?.deep_study && (
        <>
          <div className={styles.divider}></div>
          <h2 className={styles.deepStudyTitle}>Deep Study Mode</h2>

          {detailData.deep_study.failure_modes && (
            <div className={styles.section}>
              <h3>💥 Failure Modes</h3>
              <div className={styles.content}>
                {detailData.deep_study.failure_modes.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          )}

          {detailData.deep_study.multi_region_notes && (
            <div className={styles.section}>
              <h3>🌍 Multi-Region / DR</h3>
              <div className={styles.content}>
                {detailData.deep_study.multi_region_notes.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          )}

          {detailData.deep_study.tuning_gotchas && (
            <div className={styles.section}>
              <h3>⚠️ Tuning Gotchas</h3>
              <div className={styles.content}>
                {detailData.deep_study.tuning_gotchas.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          )}

          {detailData.deep_study.observability_signals && (
            <div className={styles.section}>
              <h3>📊 Observability Signals</h3>
              <div className={styles.content}>
                {detailData.deep_study.observability_signals.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          )}

          {detailData.deep_study.alternatives && (
            <div className={styles.section}>
              <h3>🔄 Alternatives</h3>
              <div className={styles.content}>
                {detailData.deep_study.alternatives.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          )}

          {detailData.deep_study.interview_prompts && (
            <div className={styles.section}>
              <h3>💬 Interview Prompts</h3>
              <div className={styles.content}>
                {detailData.deep_study.interview_prompts.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      <div className={styles.links}>
        <h3>🔗 Resources</h3>
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
    </div>
  )
}
