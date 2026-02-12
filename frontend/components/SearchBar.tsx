'use client'

import { useRef, useEffect } from 'react'
import { useSearch } from '@/hooks/useSearch'
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts'
import styles from './SearchBar.module.css'

export default function SearchBar() {
  const { searchQuery, setSearchQuery, loading } = useSearch()
  const inputRef = useRef<HTMLInputElement>(null)

  useKeyboardShortcuts({
    onSearch: () => {
      inputRef.current?.focus()
    },
  })

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  return (
    <div className={styles.searchBar}>
      <div className={styles.searchIcon}>
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path
            d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM18 18l-4.35-4.35"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
      <input
        ref={inputRef}
        type="text"
        placeholder="Search tools... (Cmd+K)"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className={styles.searchInput}
      />
      {loading && <div className={styles.loadingSpinner}>●</div>}
      {searchQuery && (
        <button
          onClick={() => setSearchQuery('')}
          className={styles.clearButton}
          aria-label="Clear search"
        >
          ✕
        </button>
      )}
    </div>
  )
}
