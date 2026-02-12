'use client'

import { useSearch } from '@/hooks/useSearch'
import { useEffect, useState } from 'react'
import { getCategories } from '@/lib/api'
import styles from './FilterPanel.module.css'

export default function FilterPanel() {
  const { filters, updateFilters, clearFilters } = useSearch()
  const [categories, setCategories] = useState<string[]>([])
  const [showFavorites, setShowFavorites] = useState(false)

  useEffect(() => {
    getCategories().then(setCategories).catch(console.error)
  }, [])

  const capOptions = ['CP', 'AP', 'Tunable']
  const consistencyOptions = ['Strong', 'Eventual', 'Causal', 'Session']

  return (
    <div className={styles.filterPanel}>
      <div className={styles.filterSection}>
        <label className={styles.filterLabel}>Category</label>
        <div className={styles.filterChips}>
          {categories.map((cat) => (
            <button
              key={cat}
              className={`${styles.chip} ${
                filters.category === cat ? styles.chipActive : ''
              }`}
              onClick={() =>
                updateFilters({
                  category: filters.category === cat ? undefined : cat,
                })
              }
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.filterSection}>
        <label className={styles.filterLabel}>CAP Leaning</label>
        <div className={styles.filterButtons}>
          {capOptions.map((cap) => (
            <button
              key={cap}
              className={`${styles.filterButton} ${
                filters.cap_leaning === cap ? styles.filterButtonActive : ''
              }`}
              onClick={() =>
                updateFilters({
                  cap_leaning: filters.cap_leaning === cap ? undefined : cap,
                })
              }
            >
              {cap}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.filterSection}>
        <label className={styles.filterLabel}>Consistency</label>
        <select
          className={styles.filterSelect}
          value={filters.consistency_model || ''}
          onChange={(e) =>
            updateFilters({
              consistency_model: e.target.value || undefined,
            })
          }
        >
          <option value="">All</option>
          {consistencyOptions.map((opt) => (
            <option key={opt} value={opt}>
              {opt}
            </option>
          ))}
        </select>
      </div>

      <div className={styles.filterSection}>
        <label className={styles.filterCheckbox}>
          <input
            type="checkbox"
            checked={filters.aws_only !== false}
            onChange={(e) =>
              updateFilters({ aws_only: e.target.checked ? undefined : false })
            }
          />
          <span>AWS only</span>
        </label>
      </div>

      <button className={styles.clearButton} onClick={clearFilters}>
        Clear all filters
      </button>
    </div>
  )
}
