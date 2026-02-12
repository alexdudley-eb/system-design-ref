'use client'

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react'
import { Tool, searchTools, getTools, FilterParams } from '@/lib/api'

interface SearchContextValue {
  tools: Tool[]
  loading: boolean
  error: string | null
  searchQuery: string
  setSearchQuery: (query: string) => void
  filters: FilterParams
  updateFilters: (filters: Partial<FilterParams>) => void
  clearFilters: () => void
  refetch: () => void
}

const SearchContext = createContext<SearchContextValue | undefined>(undefined)

export function SearchProvider({ children }: { children: ReactNode }) {
  const [tools, setTools] = useState<Tool[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState<FilterParams>({})

  const fetchTools = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      let results: Tool[]
      
      if (searchQuery.trim()) {
        results = await searchTools(searchQuery)
      } else {
        results = await getTools(filters)
      }
      
      setTools(results)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tools')
      setTools([])
    } finally {
      setLoading(false)
    }
  }, [searchQuery, filters])

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchTools()
    }, 300)

    return () => clearTimeout(timeoutId)
  }, [fetchTools])

  const updateFilters = useCallback((newFilters: Partial<FilterParams>) => {
    setFilters(prev => ({ ...prev, ...newFilters }))
  }, [])

  const clearFilters = useCallback(() => {
    setFilters({})
    setSearchQuery('')
  }, [])

  const value: SearchContextValue = {
    tools,
    loading,
    error,
    searchQuery,
    setSearchQuery,
    filters,
    updateFilters,
    clearFilters,
    refetch: fetchTools,
  }

  return (
    <SearchContext.Provider value={value}>
      {children}
    </SearchContext.Provider>
  )
}

export function useSearchContext() {
  const context = useContext(SearchContext)
  if (context === undefined) {
    throw new Error('useSearchContext must be used within a SearchProvider')
  }
  return context
}
