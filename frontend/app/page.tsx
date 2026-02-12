'use client'

import { useState, useEffect } from 'react'
import SearchBar from '@/components/SearchBar'
import FilterPanel from '@/components/FilterPanel'
import ToolList from '@/components/ToolList'
import ToolDetail from '@/components/ToolDetail'
import ScenarioPrompts from '@/components/ScenarioPrompts'
import ReferencePanel from '@/components/ReferencePanel'
import ModeToggle from '@/components/ModeToggle'
import { SearchProvider } from '@/contexts/SearchContext'
import { Tool } from '@/lib/api'

export default function Home() {
  const [selectedTool, setSelectedTool] = useState<Tool | null>(null)
  const [interviewMode, setInterviewMode] = useState<boolean>(true)

  useEffect(() => {
    const stored = localStorage.getItem('interviewMode')
    if (stored !== null) {
      setInterviewMode(stored === 'true')
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('interviewMode', String(interviewMode))
  }, [interviewMode])

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>System Design Reference</h1>
        <div className="header-controls">
          <ReferencePanel />
          <ScenarioPrompts />
          <ModeToggle 
            interviewMode={interviewMode} 
            onToggle={() => setInterviewMode(!interviewMode)} 
          />
        </div>
      </header>

      <SearchProvider>
        <div className="search-section">
          <SearchBar />
        </div>

        <FilterPanel />

        <div className="main-content">
          <div className="tool-list-panel">
            <ToolList onSelectTool={setSelectedTool} selectedToolId={selectedTool?.id} />
          </div>
          <div className="tool-detail-panel">
            {selectedTool ? (
              <ToolDetail tool={selectedTool} interviewMode={interviewMode} />
            ) : (
              <div className="empty-state">
                <h2>Select a tool to view details</h2>
                <p>Use Cmd+K to search or browse the list</p>
              </div>
            )}
          </div>
        </div>
      </SearchProvider>
    </div>
  )
}
