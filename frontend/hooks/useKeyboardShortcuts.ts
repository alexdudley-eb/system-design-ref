import { useEffect } from 'react'

interface ShortcutHandlers {
  onSearch?: () => void
  onToggleFavorites?: () => void
  onToggleMode?: () => void
  onEscape?: () => void
  onArrowUp?: () => void
  onArrowDown?: () => void
  onEnter?: () => void
  onNumberKey?: (num: number) => void
}

export function useKeyboardShortcuts(handlers: ShortcutHandlers) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const isCmdOrCtrl = e.metaKey || e.ctrlKey
      const target = e.target as HTMLElement
      const isTyping = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable

      if (isCmdOrCtrl && e.key === 'k') {
        e.preventDefault()
        handlers.onSearch?.()
        return
      }

      if (isCmdOrCtrl && e.key === 'f') {
        e.preventDefault()
        handlers.onToggleFavorites?.()
        return
      }

      if (isCmdOrCtrl && e.key === 'i') {
        e.preventDefault()
        handlers.onToggleMode?.()
        return
      }

      if (!isTyping) {
        if (e.key === 'Escape') {
          e.preventDefault()
          handlers.onEscape?.()
          return
        }

        if (e.key === 'ArrowUp') {
          e.preventDefault()
          handlers.onArrowUp?.()
          return
        }

        if (e.key === 'ArrowDown') {
          e.preventDefault()
          handlers.onArrowDown?.()
          return
        }

        if (e.key === 'Enter') {
          e.preventDefault()
          handlers.onEnter?.()
          return
        }

        if (e.key >= '1' && e.key <= '9') {
          const num = parseInt(e.key, 10)
          handlers.onNumberKey?.(num)
          return
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [handlers])
}
