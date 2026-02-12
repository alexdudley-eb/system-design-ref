'use client'

import { useState } from 'react'
import { ScenarioResponse, Tool } from '@/lib/api'
import ToolModal from './ToolModal'
import styles from './ScenarioDetail.module.css'

const TABS = [
  { id: 'requirements', label: 'Requirements' },
  { id: 'entities', label: 'Core Entities' },
  { id: 'api', label: 'API' },
  { id: 'high_level', label: 'High Level' },
  { id: 'deep_dive', label: 'Deep Dive' },
] as const

type TabId = (typeof TABS)[number]['id']

const METHOD_COLORS: Record<string, string> = {
  GET: styles.methodGet,
  POST: styles.methodPost,
  PUT: styles.methodPut,
  DELETE: styles.methodDelete,
  PATCH: styles.methodPatch,
  WS: styles.methodWs,
}

interface ScenarioDetailProps {
  data: ScenarioResponse
}

export default function ScenarioDetail({ data }: ScenarioDetailProps) {
  const [activeTab, setActiveTab] = useState<TabId>('requirements')
  const [selectedTool, setSelectedTool] = useState<Tool | null>(null)
  const [isToolModalOpen, setIsToolModalOpen] = useState(false)

  const handleToolClick = (tool: Tool) => {
    setSelectedTool(tool)
    setIsToolModalOpen(true)
  }

  const handleCloseToolModal = () => {
    setIsToolModalOpen(false)
    setSelectedTool(null)
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>{data.title}</h2>
        <p className={styles.description}>{data.description}</p>
      </div>

      <div className={styles.tabBar}>
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={`${styles.tab} ${activeTab === tab.id ? styles.tabActive : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className={styles.tabContent}>
        {activeTab === 'requirements' && (
          <RequirementsTab data={data} />
        )}
        {activeTab === 'entities' && (
          <EntitiesTab data={data} />
        )}
        {activeTab === 'api' && (
          <ApiTab data={data} />
        )}
        {activeTab === 'high_level' && (
          <HighLevelTab data={data} />
        )}
        {activeTab === 'deep_dive' && (
          <DeepDiveTab data={data} />
        )}
      </div>

      <div className={styles.toolsFooter}>
        <h4 className={styles.toolsLabel}>Recommended Stack</h4>
        <p className={styles.toolsReasoning}>{data.reasoning}</p>
        <div className={styles.toolChips}>
          {data.tools.map((tool) => (
            <button
              key={tool.id}
              className={styles.toolChip}
              onClick={() => handleToolClick(tool)}
            >
              {tool.name}
            </button>
          ))}
        </div>
      </div>

      {isToolModalOpen && selectedTool && (
        <ToolModal tool={selectedTool} onClose={handleCloseToolModal} />
      )}
    </div>
  )
}

function RequirementsTab({ data }: { data: ScenarioResponse }) {
  return (
    <div className={styles.requirementsGrid}>
      <div className={styles.reqSection}>
        <h3 className={styles.reqTitle}>Functional Requirements</h3>
        <ul className={styles.reqList}>
          {data.requirements.functional.map((req, i) => (
            <li key={i} className={styles.reqItem}>
              <span className={styles.reqBullet}>-</span>
              {req}
            </li>
          ))}
        </ul>
      </div>

      <div className={styles.reqSection}>
        <h3 className={styles.reqTitle}>Non-Functional Requirements</h3>
        <ul className={styles.reqList}>
          {data.requirements.non_functional.map((req, i) => (
            <li key={i} className={styles.reqItem}>
              <span className={styles.reqBullet}>-</span>
              {req}
            </li>
          ))}
        </ul>
      </div>

      <div className={styles.reqSection}>
        <h3 className={styles.reqTitle}>Out of Scope</h3>
        <ul className={styles.reqList}>
          {data.requirements.out_of_scope.map((req, i) => (
            <li key={i} className={`${styles.reqItem} ${styles.reqItemMuted}`}>
              <span className={styles.reqBullet}>-</span>
              {req}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

function EntitiesTab({ data }: { data: ScenarioResponse }) {
  return (
    <div className={styles.entitiesGrid}>
      {data.core_entities.map((entity) => (
        <div key={entity.name} className={styles.entityCard}>
          <div className={styles.entityHeader}>{entity.name}</div>
          <ul className={styles.fieldList}>
            {entity.fields.map((field, i) => (
              <li key={i} className={styles.fieldItem}>{field}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}

function ApiTab({ data }: { data: ScenarioResponse }) {
  return (
    <div className={styles.apiList}>
      {data.api.map((endpoint, i) => (
        <div key={i} className={styles.apiCard}>
          <div className={styles.apiRoute}>
            <span className={`${styles.methodBadge} ${METHOD_COLORS[endpoint.method] || ''}`}>
              {endpoint.method}
            </span>
            <code className={styles.apiPath}>{endpoint.path}</code>
          </div>
          <p className={styles.apiDescription}>{endpoint.description}</p>
          {endpoint.auth && (
            <div className={styles.apiMeta}>
              <span className={styles.apiMetaLabel}>Auth:</span> {endpoint.auth}
            </div>
          )}
          {endpoint.request_body && (
            <div className={styles.apiBody}>
              <span className={styles.apiMetaLabel}>Body:</span>
              <code>{endpoint.request_body}</code>
            </div>
          )}
          {endpoint.response && (
            <div className={styles.apiBody}>
              <span className={styles.apiMetaLabel}>Response:</span>
              <code>{endpoint.response}</code>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

function HighLevelTab({ data }: { data: ScenarioResponse }) {
  return (
    <div className={styles.highLevel}>
      <div className={styles.archDescription}>
        <p>{data.high_level.description}</p>
      </div>

      <div className={styles.componentsSection}>
        <h3 className={styles.sectionTitle}>Components</h3>
        <ul className={styles.componentList}>
          {data.high_level.components.map((comp, i) => (
            <li key={i} className={styles.componentItem}>{comp}</li>
          ))}
        </ul>
      </div>

      {data.high_level.notes.length > 0 && (
        <div className={styles.notesSection}>
          <h3 className={styles.sectionTitle}>Key Notes</h3>
          <ul className={styles.notesList}>
            {data.high_level.notes.map((note, i) => (
              <li key={i} className={styles.noteItem}>{note}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

function DeepDiveTab({ data }: { data: ScenarioResponse }) {
  return (
    <div className={styles.deepDive}>
      {data.deep_dive.flows.map((flow, i) => (
        <div key={i} className={styles.flowSection}>
          <h3 className={styles.flowTitle}>{flow.name}</h3>
          <ol className={styles.flowSteps}>
            {flow.steps.map((step, j) => (
              <li key={j} className={styles.flowStep}>{step}</li>
            ))}
          </ol>
        </div>
      ))}

      {data.deep_dive.caching && (
        <div className={styles.ddSection}>
          <h3 className={styles.sectionTitle}>Caching Strategy</h3>
          <p className={styles.ddText}>{data.deep_dive.caching}</p>
        </div>
      )}

      {data.deep_dive.scaling && (
        <div className={styles.ddSection}>
          <h3 className={styles.sectionTitle}>Scaling</h3>
          <p className={styles.ddText}>{data.deep_dive.scaling}</p>
        </div>
      )}

      {data.deep_dive.notes.length > 0 && (
        <div className={styles.ddSection}>
          <h3 className={styles.sectionTitle}>Additional Notes</h3>
          <ul className={styles.notesList}>
            {data.deep_dive.notes.map((note, i) => (
              <li key={i} className={styles.noteItem}>{note}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
