export interface QuestionPerformance {
  questionId: string
  easeFactor: number
  interval: number
  repetitions: number
  lastReviewDate: string
  nextReviewDate: string
  totalReviews: number
  correctReviews: number
}

const STORAGE_KEY = 'question_performance'
const MIN_EASE_FACTOR = 1.3
const MAX_EASE_FACTOR = 2.5
const INITIAL_EASE_FACTOR = 2.5
const INITIAL_INTERVAL = 1

function calculateNextReviewDate(intervalDays: number): string {
  const date = new Date()
  date.setDate(date.getDate() + intervalDays)
  return date.toISOString()
}

function getAllPerformanceData(): Record<string, QuestionPerformance> {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return {}
    return JSON.parse(stored) as Record<string, QuestionPerformance>
  } catch (error) {
    console.error('Failed to load question performance data:', error)
    return {}
  }
}

function savePerformanceData(data: Record<string, QuestionPerformance>): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch (error) {
    console.error('Failed to save question performance data:', error)
  }
}

export function getQuestionPerformance(questionId: string): QuestionPerformance | null {
  const allData = getAllPerformanceData()
  return allData[questionId] || null
}

export function initializeNewQuestion(questionId: string): QuestionPerformance {
  const now = new Date().toISOString()
  const performance: QuestionPerformance = {
    questionId,
    easeFactor: INITIAL_EASE_FACTOR,
    interval: INITIAL_INTERVAL,
    repetitions: 0,
    lastReviewDate: now,
    nextReviewDate: now,
    totalReviews: 0,
    correctReviews: 0,
  }

  const allData = getAllPerformanceData()
  allData[questionId] = performance
  savePerformanceData(allData)

  return performance
}

export function updateQuestionPerformance(
  questionId: string,
  wasCorrect: boolean
): QuestionPerformance {
  let performance = getQuestionPerformance(questionId)
  
  if (!performance) {
    performance = initializeNewQuestion(questionId)
  }

  const now = new Date().toISOString()
  performance.lastReviewDate = now
  performance.totalReviews += 1

  if (wasCorrect) {
    performance.correctReviews += 1
    performance.repetitions += 1

    if (performance.repetitions === 1) {
      performance.interval = 1
    } else if (performance.repetitions === 2) {
      performance.interval = 6
    } else {
      performance.interval = Math.round(performance.interval * performance.easeFactor)
    }

    performance.easeFactor = Math.min(
      MAX_EASE_FACTOR,
      performance.easeFactor + 0.1
    )
  } else {
    performance.repetitions = 0
    performance.interval = 1
    performance.easeFactor = Math.max(
      MIN_EASE_FACTOR,
      performance.easeFactor - 0.2
    )
  }

  performance.nextReviewDate = calculateNextReviewDate(performance.interval)

  const allData = getAllPerformanceData()
  allData[questionId] = performance
  savePerformanceData(allData)

  return performance
}

export function getQuestionsForReview(
  allQuestionIds: string[],
  maxCount?: number
): string[] {
  const now = new Date()
  const allData = getAllPerformanceData()

  const questionsWithPerformance = allQuestionIds.map(id => {
    const performance = allData[id]
    if (!performance) {
      return {
        id,
        isDue: true,
        dueDate: new Date(0),
        easeFactor: INITIAL_EASE_FACTOR,
        lastReviewDate: new Date(0),
        hasBeenReviewed: false,
      }
    }

    const nextReview = new Date(performance.nextReviewDate)
    return {
      id,
      isDue: nextReview <= now,
      dueDate: nextReview,
      easeFactor: performance.easeFactor,
      lastReviewDate: new Date(performance.lastReviewDate),
      hasBeenReviewed: true,
    }
  })

  const dueQuestions = questionsWithPerformance.filter(q => q.isDue)
  const notDueQuestions = questionsWithPerformance.filter(q => !q.isDue)

  dueQuestions.sort((a, b) => {
    if (a.hasBeenReviewed !== b.hasBeenReviewed) {
      return a.hasBeenReviewed ? 1 : -1
    }
    
    const dateDiff = a.dueDate.getTime() - b.dueDate.getTime()
    if (dateDiff !== 0) return dateDiff
    
    return a.easeFactor - b.easeFactor
  })

  notDueQuestions.sort((a, b) => {
    return a.lastReviewDate.getTime() - b.lastReviewDate.getTime()
  })

  const shuffleArray = <T,>(array: T[]): T[] => {
    const shuffled = [...array]
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    return shuffled
  }

  const dueCount = Math.ceil((maxCount || dueQuestions.length) * 0.7)
  const selectedDue = shuffleArray(dueQuestions.slice(0, dueCount))
  
  const remainingSlots = (maxCount || allQuestionIds.length) - selectedDue.length
  const selectedNotDue = remainingSlots > 0 
    ? shuffleArray(notDueQuestions.slice(0, remainingSlots))
    : []

  return [...selectedDue, ...selectedNotDue].map(q => q.id)
}

export function getPerformanceStats(): {
  totalQuestions: number
  reviewedQuestions: number
  dueToday: number
  averageEaseFactor: number
  averageInterval: number
} {
  const allData = getAllPerformanceData()
  const performances = Object.values(allData)
  const now = new Date()

  const reviewedQuestions = performances.filter(p => p.totalReviews > 0).length
  const dueToday = performances.filter(p => new Date(p.nextReviewDate) <= now).length
  
  const totalEase = performances.reduce((sum, p) => sum + p.easeFactor, 0)
  const totalInterval = performances.reduce((sum, p) => sum + p.interval, 0)

  return {
    totalQuestions: performances.length,
    reviewedQuestions,
    dueToday,
    averageEaseFactor: performances.length > 0 ? totalEase / performances.length : 0,
    averageInterval: performances.length > 0 ? totalInterval / performances.length : 0,
  }
}

export function resetQuestionPerformance(questionId: string): void {
  const allData = getAllPerformanceData()
  delete allData[questionId]
  savePerformanceData(allData)
}

export function resetAllPerformance(): void {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch (error) {
    console.error('Failed to reset performance data:', error)
  }
}
