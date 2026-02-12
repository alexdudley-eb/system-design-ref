'use client'

import { useState, useEffect, useCallback } from 'react'
import { useSearch } from '@/hooks/useSearch'
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts'
import { Tool, addFavorite, removeFavorite } from '@/lib/api'
import styles from './ToolList.module.css'

interface ToolListProps {
  onSelectTool: (tool: Tool) => void
  selectedToolId?: number
}

export default function ToolList({ onSelectTool, selectedToolId }: ToolListProps) {
  const { tools, loading, error } = useSearch()
  const [focusedIndex, setFocusedIndex] = useState(0)

  useEffect(() => {
    if (tools.length > 0 && focusedIndex >= tools.length) {
      setFocusedIndex(tools.length - 1)
    }
  }, [tools.length, focusedIndex])

  const handleArrowUp = useCallback(() => {
    setFocusedIndex((prev) => Math.max(0, prev - 1))
  }, [])

  const handleArrowDown = useCallback(() => {
    setFocusedIndex((prev) => Math.min(tools.length - 1, prev + 1))
  }, [tools.length])

  const handleEnter = useCallback(() => {
    if (tools[focusedIndex]) {
      onSelectTool(tools[focusedIndex])
    }
  }, [tools, focusedIndex, onSelectTool])

  useKeyboardShortcuts({
    onArrowUp: handleArrowUp,
    onArrowDown: handleArrowDown,
    onEnter: handleEnter,
  })

  const handleFavoriteToggle = async (e: React.MouseEvent, tool: Tool) => {
    e.stopPropagation()
    
    try {
      if (tool.is_favorited) {
        await removeFavorite(tool.id)
      } else {
        await addFavorite(tool.id)
      }
      window.location.reload()
    } catch (error) {
      console.error('Failed to toggle favorite:', error)
    }
  }

  if (loading && tools.length === 0) {
    return (
      <div className={styles.emptyState}>
        <div className={styles.spinner}>Loading...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className={styles.emptyState}>
        <div className={styles.errorMessage}>{error}</div>
      </div>
    )
  }

  if (tools.length === 0) {
    return (
      <div className={styles.emptyState}>
        <p>No tools found</p>
        <p className={styles.emptyHint}>Try adjusting your filters</p>
      </div>
    )
  }

  return (
    <div className={styles.toolList}>
      {tools.map((tool, index) => (
        <div
          key={tool.id}
          className={`${styles.toolCard} ${
            selectedToolId === tool.id ? styles.toolCardSelected : ''
          } ${focusedIndex === index ? styles.toolCardFocused : ''}`}
          onClick={() => {
            setFocusedIndex(index)
            onSelectTool(tool)
          }}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault()
              onSelectTool(tool)
            }
          }}
        >
          <div className={styles.toolHeader}>
            <h3 className={styles.toolName}>{tool.name}</h3>
            <button
              className={styles.favoriteButton}
              onClick={(e) => handleFavoriteToggle(e, tool)}
              aria-label={tool.is_favorited ? 'Unfavorite' : 'Favorite'}
            >
              {tool.is_favorited ? '★' : '☆'}
            </button>
          </div>
          <div className={styles.toolMeta}>
            <span className={styles.categoryBadge}>{tool.category}</span>
            {tool.cap_leaning && (
              <span className={styles.capBadge}>{tool.cap_leaning}</span>
            )}
          </div>
          {tool.interview_oneliner && (
            <p className={styles.toolOneliner}>{tool.interview_oneliner}</p>
          )}
        </div>
      ))}
    </div>
  )
}
