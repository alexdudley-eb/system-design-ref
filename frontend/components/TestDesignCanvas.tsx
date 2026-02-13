"use client";

import { useState, useEffect } from "react";
import {
  TestSession,
  TestDesign,
  saveActiveTestSession,
} from "@/lib/quizStorage";
import QuizTimer from "./QuizTimer";
import styles from "./TestMode.module.css";

interface TestDesignCanvasProps {
  session: TestSession;
  onUpdateSession: (session: TestSession) => void;
  onFinish: (timeTaken: number) => void;
}

type DesignTab =
  | "requirements"
  | "entities-api"
  | "architecture"
  | "deep-dives"
  | "notes";

export default function TestDesignCanvas({
  session,
  onUpdateSession,
  onFinish,
}: TestDesignCanvasProps) {
  const [activeTab, setActiveTab] = useState<DesignTab>("requirements");
  const [design, setDesign] = useState<TestDesign>(session.design);
  const [timeTaken, setTimeTaken] = useState(0);

  useEffect(() => {
    const updatedSession = { ...session, design };
    onUpdateSession(updatedSession);
    saveActiveTestSession(updatedSession);
  }, [design]);

  const addRequirement = (
    type: "functional" | "nonFunctional" | "outOfScope",
  ) => {
    const key =
      type === "functional"
        ? "functionalRequirements"
        : type === "nonFunctional"
          ? "nonFunctionalRequirements"
          : "outOfScope";
    setDesign({ ...design, [key]: [...design[key], ""] });
  };

  const updateRequirement = (
    type: "functional" | "nonFunctional" | "outOfScope",
    index: number,
    value: string,
  ) => {
    const key =
      type === "functional"
        ? "functionalRequirements"
        : type === "nonFunctional"
          ? "nonFunctionalRequirements"
          : "outOfScope";
    const updated = [...design[key]];
    updated[index] = value;
    setDesign({ ...design, [key]: updated });
  };

  const removeRequirement = (
    type: "functional" | "nonFunctional" | "outOfScope",
    index: number,
  ) => {
    const key =
      type === "functional"
        ? "functionalRequirements"
        : type === "nonFunctional"
          ? "nonFunctionalRequirements"
          : "outOfScope";
    const updated = design[key].filter((_, i) => i !== index);
    setDesign({ ...design, [key]: updated });
  };

  const addEntity = () => {
    setDesign({
      ...design,
      entities: [...design.entities, { name: "", fields: [""] }],
    });
  };

  const addAPIEndpoint = () => {
    setDesign({
      ...design,
      apiEndpoints: [
        ...design.apiEndpoints,
        { method: "GET", path: "", description: "" },
      ],
    });
  };

  const addComponent = () => {
    setDesign({ ...design, components: [...design.components, ""] });
  };

  const addDeepDive = () => {
    setDesign({
      ...design,
      deepDives: [...design.deepDives, { topic: "", notes: "" }],
    });
  };

  const handleTick = (secondsElapsed: number) => {
    setTimeTaken(secondsElapsed);
  };

  const handleTimeUp = () => {
    onFinish(timeTaken);
  };

  const handleManualFinish = () => {
    onFinish(timeTaken);
  };

  return (
    <div className={styles.testContainer}>
      <div className={styles.testLayout}>
        <div className={styles.scenarioSidebar}>
          <h3>Scenario Info</h3>
          <div className={styles.scenarioInfo}>
            <h4>{session.scenario.title}</h4>
            <p>{session.scenario.description}</p>

            {Object.keys(session.scenario.scale).length > 0 && (
              <div className={styles.scaleInfo}>
                <h5>Scale</h5>
                <ul>
                  {Object.entries(session.scenario.scale).map(
                    ([key, value]) => (
                      <li key={key}>
                        <strong>{key.replace(/_/g, " ")}:</strong>{" "}
                        {value as string}
                      </li>
                    ),
                  )}
                </ul>
              </div>
            )}

            {session.scenario.hints && (
              <div className={styles.hints}>
                <h5>Hints</h5>
                {session.scenario.hints.out_of_scope.length > 0 && (
                  <>
                    <strong>Out of Scope:</strong>
                    <ul>
                      {session.scenario.hints.out_of_scope.map(
                        (item: string, idx: number) => (
                          <li key={idx}>{item}</li>
                        ),
                      )}
                    </ul>
                  </>
                )}
                {session.scenario.hints.key_constraints.length > 0 && (
                  <>
                    <strong>Key Constraints:</strong>
                    <ul>
                      {session.scenario.hints.key_constraints.map(
                        (item: string, idx: number) => (
                          <li key={idx}>{item}</li>
                        ),
                      )}
                    </ul>
                  </>
                )}
              </div>
            )}
          </div>

          <QuizTimer
            sessionId={session.id}
            totalSeconds={session.timeAllocated * 60}
            onTimeUp={handleTimeUp}
            onTick={handleTick}
          />
        </div>

        <div className={styles.designPanel}>
          <div className={styles.tabs}>
            <button
              className={activeTab === "requirements" ? styles.tabActive : ""}
              onClick={() => setActiveTab("requirements")}
            >
              Requirements
            </button>
            <button
              className={activeTab === "entities-api" ? styles.tabActive : ""}
              onClick={() => setActiveTab("entities-api")}
            >
              Entities & API
            </button>
            <button
              className={activeTab === "architecture" ? styles.tabActive : ""}
              onClick={() => setActiveTab("architecture")}
            >
              Architecture
            </button>
            <button
              className={activeTab === "deep-dives" ? styles.tabActive : ""}
              onClick={() => setActiveTab("deep-dives")}
            >
              Deep Dives
            </button>
            <button
              className={activeTab === "notes" ? styles.tabActive : ""}
              onClick={() => setActiveTab("notes")}
            >
              Notes
            </button>
          </div>

          <div className={styles.tabContent}>
            {activeTab === "requirements" && (
              <div className={styles.requirementsTab}>
                <section className={styles.designSection}>
                  <h4>Functional Requirements</h4>
                  {design.functionalRequirements.map(
                    (req: string, idx: number) => (
                      <div key={idx} className={styles.inputRow}>
                        <input
                          value={req}
                          onChange={(e) =>
                            updateRequirement("functional", idx, e.target.value)
                          }
                          placeholder="e.g., Users can post text and images"
                        />
                        <button
                          onClick={() => removeRequirement("functional", idx)}
                        >
                          Remove
                        </button>
                      </div>
                    ),
                  )}
                  <button onClick={() => addRequirement("functional")}>
                    + Add Functional Requirement
                  </button>
                </section>

                <section className={styles.designSection}>
                  <h4>Non-Functional Requirements</h4>
                  {design.nonFunctionalRequirements.map(
                    (req: string, idx: number) => (
                      <div key={idx} className={styles.inputRow}>
                        <input
                          value={req}
                          onChange={(e) =>
                            updateRequirement(
                              "nonFunctional",
                              idx,
                              e.target.value,
                            )
                          }
                          placeholder="e.g., 99.9% availability, <200ms latency"
                        />
                        <button
                          onClick={() =>
                            removeRequirement("nonFunctional", idx)
                          }
                        >
                          Remove
                        </button>
                      </div>
                    ),
                  )}
                  <button onClick={() => addRequirement("nonFunctional")}>
                    + Add Non-Functional Requirement
                  </button>
                </section>

                <section className={styles.designSection}>
                  <h4>Out of Scope</h4>
                  {design.outOfScope.map((req: string, idx: number) => (
                    <div key={idx} className={styles.inputRow}>
                      <input
                        value={req}
                        onChange={(e) =>
                          updateRequirement("outOfScope", idx, e.target.value)
                        }
                        placeholder="e.g., Analytics, Admin panel"
                      />
                      <button
                        onClick={() => removeRequirement("outOfScope", idx)}
                      >
                        Remove
                      </button>
                    </div>
                  ))}
                  <button onClick={() => addRequirement("outOfScope")}>
                    + Add Out of Scope
                  </button>
                </section>
              </div>
            )}

            {activeTab === "entities-api" && (
              <div>
                <section className={styles.designSection}>
                  <h4>Entities</h4>
                  {design.entities.map((entity, idx) => (
                    <div key={idx} className={styles.entity}>
                      <input
                        value={entity.name}
                        onChange={(e) => {
                          const updated = [...design.entities];
                          updated[idx].name = e.target.value;
                          setDesign({ ...design, entities: updated });
                        }}
                        placeholder="Entity name (e.g., User, Post)"
                      />
                      <textarea
                        value={entity.fields.join("\n")}
                        onChange={(e) => {
                          const updated = [...design.entities];
                          updated[idx].fields = e.target.value.split("\n");
                          setDesign({ ...design, entities: updated });
                        }}
                        placeholder="Fields (one per line)"
                        rows={4}
                      />
                    </div>
                  ))}
                  <button onClick={addEntity}>+ Add Entity</button>
                </section>

                <section className={styles.designSection}>
                  <h4>API Endpoints</h4>
                  {design.apiEndpoints.map((endpoint, idx) => (
                    <div key={idx} className={styles.apiEndpoint}>
                      <select
                        value={endpoint.method}
                        onChange={(e) => {
                          const updated = [...design.apiEndpoints];
                          updated[idx].method = e.target.value;
                          setDesign({ ...design, apiEndpoints: updated });
                        }}
                      >
                        <option>GET</option>
                        <option>POST</option>
                        <option>PUT</option>
                        <option>DELETE</option>
                      </select>
                      <input
                        value={endpoint.path}
                        onChange={(e) => {
                          const updated = [...design.apiEndpoints];
                          updated[idx].path = e.target.value;
                          setDesign({ ...design, apiEndpoints: updated });
                        }}
                        placeholder="/api/path"
                      />
                      <input
                        value={endpoint.description}
                        onChange={(e) => {
                          const updated = [...design.apiEndpoints];
                          updated[idx].description = e.target.value;
                          setDesign({ ...design, apiEndpoints: updated });
                        }}
                        placeholder="Description"
                      />
                    </div>
                  ))}
                  <button onClick={addAPIEndpoint}>+ Add API Endpoint</button>
                </section>
              </div>
            )}

            {activeTab === "architecture" && (
              <div>
                <section className={styles.designSection}>
                  <h4>High-Level Design Description</h4>
                  <textarea
                    value={design.highLevelDesign}
                    onChange={(e) =>
                      setDesign({ ...design, highLevelDesign: e.target.value })
                    }
                    placeholder="Describe your architecture..."
                    rows={6}
                  />
                </section>

                <section className={styles.designSection}>
                  <h4>Components</h4>
                  {design.components.map((component: string, idx: number) => (
                    <div key={idx} className={styles.inputRow}>
                      <input
                        value={component}
                        onChange={(e) => {
                          const updated = [...design.components];
                          updated[idx] = e.target.value;
                          setDesign({ ...design, components: updated });
                        }}
                        placeholder="e.g., Load Balancer, API Gateway, Database Cluster"
                      />
                    </div>
                  ))}
                  <button onClick={addComponent}>+ Add Component</button>
                </section>
              </div>
            )}

            {activeTab === "deep-dives" && (
              <div>
                {design.deepDives.map((dive, idx) => (
                  <section key={idx} className={styles.designSection}>
                    <input
                      value={dive.topic}
                      onChange={(e) => {
                        const updated = [...design.deepDives];
                        updated[idx].topic = e.target.value;
                        setDesign({ ...design, deepDives: updated });
                      }}
                      placeholder="Deep dive topic (e.g., Database Schema, Caching Strategy)"
                    />
                    <textarea
                      value={dive.notes}
                      onChange={(e) => {
                        const updated = [...design.deepDives];
                        updated[idx].notes = e.target.value;
                        setDesign({ ...design, deepDives: updated });
                      }}
                      placeholder="Detailed notes..."
                      rows={4}
                    />
                  </section>
                ))}
                <button onClick={addDeepDive}>+ Add Deep Dive</button>
              </div>
            )}

            {activeTab === "notes" && (
              <div>
                <section className={styles.designSection}>
                  <h4>Tradeoffs</h4>
                  <textarea
                    value={design.tradeoffs}
                    onChange={(e) =>
                      setDesign({ ...design, tradeoffs: e.target.value })
                    }
                    placeholder="Document key tradeoffs..."
                    rows={4}
                  />
                </section>

                <section className={styles.designSection}>
                  <h4>Scaling Considerations</h4>
                  <textarea
                    value={design.scalingConsiderations}
                    onChange={(e) =>
                      setDesign({
                        ...design,
                        scalingConsiderations: e.target.value,
                      })
                    }
                    placeholder="How would you scale this system?"
                    rows={4}
                  />
                </section>

                <section className={styles.designSection}>
                  <h4>Failure Modes</h4>
                  <textarea
                    value={design.failureModes}
                    onChange={(e) =>
                      setDesign({ ...design, failureModes: e.target.value })
                    }
                    placeholder="What can go wrong and how to handle it?"
                    rows={4}
                  />
                </section>
              </div>
            )}
          </div>

          <div className={styles.designActions}>
            <button
              className={styles.finishButton}
              onClick={handleManualFinish}
            >
              Finish Design → Assessment
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
