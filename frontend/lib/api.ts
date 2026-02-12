const API_BASE_URL = 'http://localhost:8000/api'

export interface Tool {
  id: number
  name: string
  category: string
  cap_leaning?: string
  consistency_model?: string
  interview_oneliner?: string
  best_for?: string
  avoid_when?: string
  tradeoffs?: string
  scaling_pattern?: string
  official_docs_url?: string
  deep_dive_url_1?: string
  deep_dive_url_2?: string
  aws_only?: number
  is_favorited?: boolean
}

export interface ToolDeep {
  failure_modes?: string
  multi_region_notes?: string
  tuning_gotchas?: string
  observability_signals?: string
  alternatives?: string
  interview_prompts?: string
}

export interface ToolDetail extends Tool {
  deep_study?: ToolDeep
}

export interface ScenarioResponse {
  scenario: string
  reasoning: string
  tools: Tool[]
}

export interface FilterParams {
  category?: string
  cap_leaning?: string
  consistency_model?: string
  aws_only?: boolean
}

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('API fetch error:', error)
    throw error
  }
}

export async function getTools(filters?: FilterParams): Promise<Tool[]> {
  const params = new URLSearchParams()
  
  if (filters?.category) params.append('category', filters.category)
  if (filters?.cap_leaning) params.append('cap_leaning', filters.cap_leaning)
  if (filters?.consistency_model) params.append('consistency_model', filters.consistency_model)
  if (filters?.aws_only !== undefined) params.append('aws_only', String(filters.aws_only))
  
  const query = params.toString() ? `?${params.toString()}` : ''
  return fetchAPI<Tool[]>(`/tools${query}`)
}

export async function searchTools(query: string): Promise<Tool[]> {
  if (!query.trim()) {
    return getTools()
  }
  return fetchAPI<Tool[]>(`/tools/search?q=${encodeURIComponent(query)}`)
}

export async function getToolDetail(toolId: number): Promise<ToolDetail> {
  return fetchAPI<ToolDetail>(`/tools/${toolId}`)
}

export async function getScenarioSuggestions(scenarioType: string): Promise<ScenarioResponse> {
  return fetchAPI<ScenarioResponse>(`/scenarios/${scenarioType}`)
}

export async function getFavorites(): Promise<Tool[]> {
  const response = await fetchAPI<{ tool: Tool }[]>('/favorites')
  return response.map(fav => fav.tool)
}

export async function addFavorite(toolId: number): Promise<void> {
  await fetchAPI(`/favorites/${toolId}`, {
    method: 'POST',
  })
}

export async function removeFavorite(toolId: number): Promise<void> {
  await fetchAPI(`/favorites/${toolId}`, {
    method: 'DELETE',
  })
}

export async function getCategories(): Promise<string[]> {
  return fetchAPI<string[]>('/categories')
}
