"use client";

import { useState, useEffect } from "react";
import styles from "./ReferencePanel.module.css";

type ReferenceType = "numbers" | "framework" | "rubric" | "patterns";

interface NumbersData {
  latency: Array<{ operation: string; value: string; context: string; usage: string }>;
  throughput: Array<{ metric: string; value: string; context: string; usage: string }>;
  capacity: Array<{ item: string; value: string; context: string; usage: string }>;
  storage: Array<{ item: string; value: string; context: string; usage: string }>;
  availability: Array<{ tier: string; downtime_per_year: string; context: string; usage: string }>;
}

interface FrameworkPhase {
  phase: string;
  time: string;
  goal: string;
  activities: string[];
  common_mistakes?: string[];
  tips?: string[];
  example_questions?: string[];
  areas?: Array<{ topic: string; questions: string[] }>;
  reflection_questions?: string[];
}

interface FrameworkData {
  overview: string;
  time_allocation: {
    total_time: string;
    requirements: string;
    high_level_design: string;
    deep_dives: string;
    wrap_up: string;
  };
  phases: FrameworkPhase[];
  best_practices: string[];
}

interface RubricCompetency {
  name: string;
  weight: string;
  description: string;
  levels: {
    strong: string[];
    adequate: string[];
    weak: string[];
  };
  how_to_improve: string[];
}

interface RubricData {
  overview: string;
  competencies: RubricCompetency[];
  level_expectations: {
    mid_level: { expectations: string[] };
    senior: { expectations: string[] };
    staff_plus: { expectations: string[] };
  };
  red_flags: string[];
  green_flags: string[];
}

interface PatternApproach {
  name: string;
  description: string;
  pros: string[];
  cons: string[];
  when_to_use: string;
  technologies?: string[];
  implementation?: string;
  example_sql?: string;
  types?: Array<{ variant: string; description: string; pros: string[]; cons: string[] }>;
}

interface Pattern {
  title: string;
  problem: string;
  use_cases: string[];
  approaches: PatternApproach[];
  scaling_considerations?: string[];
  ticketmaster_example?: string;
  example_flow?: { scenario: string; steps: string[] };
  strategies?: Array<{
    name: string;
    description: string;
    latency_improvement?: string;
    throughput_improvement?: string;
    when_to_use: string;
    considerations?: string[];
    cache_patterns?: string[];
    cache_keys?: string[];
    tradeoffs?: string[];
    sharding_keys?: string[];
    challenges?: string[];
    technologies?: string[];
    methods?: Array<{ approach: string; description: string; pros: string[]; cons: string[] }>;
  }>;
  layered_approach?: {
    description: string;
    layers: string[];
    result: string;
  };
  example_architecture?: {
    scenario: string;
    design: string[];
    result: string;
  };
  example_design?: {
    scenario: string;
    flow: string[];
    latency?: string;
  };
}

interface PatternsData {
  [key: string]: Pattern;
}

export default function ReferencePanel() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedType, setSelectedType] = useState<ReferenceType>("numbers");
  const [data, setData] = useState<NumbersData | FrameworkData | RubricData | PatternsData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && !data) {
      loadData(selectedType);
    }
  }, [isOpen, selectedType]);

  const loadData = async (type: ReferenceType) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/reference/${type}`);
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("Failed to load reference data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleTypeChange = (type: ReferenceType) => {
    setSelectedType(type);
    setData(null);
    loadData(type);
  };

  const renderNumbers = (data: NumbersData) => (
    <div className={styles.numbersGrid}>
      <div className={styles.numberSection}>
        <h3>⚡ Latency</h3>
        {data.latency.map((item, idx) => (
          <div key={idx} className={styles.numberCard}>
            <div className={styles.numberValue}>{item.value}</div>
            <div className={styles.numberOp}>{item.operation}</div>
            <div className={styles.numberUsage}>{item.usage}</div>
          </div>
        ))}
      </div>

      <div className={styles.numberSection}>
        <h3>📈 Throughput</h3>
        {data.throughput.map((item, idx) => (
          <div key={idx} className={styles.numberCard}>
            <div className={styles.numberValue}>{item.value}</div>
            <div className={styles.numberOp}>{item.metric}</div>
            <div className={styles.numberUsage}>{item.usage}</div>
          </div>
        ))}
      </div>

      <div className={styles.numberSection}>
        <h3>🎯 Capacity</h3>
        {data.capacity.map((item, idx) => (
          <div key={idx} className={styles.numberCard}>
            <div className={styles.numberValue}>{item.value}</div>
            <div className={styles.numberOp}>{item.item}</div>
            <div className={styles.numberUsage}>{item.usage}</div>
          </div>
        ))}
      </div>

      <div className={styles.numberSection}>
        <h3>💾 Storage</h3>
        {data.storage.map((item, idx) => (
          <div key={idx} className={styles.numberCard}>
            <div className={styles.numberValue}>{item.value}</div>
            <div className={styles.numberOp}>{item.item}</div>
            <div className={styles.numberUsage}>{item.usage}</div>
          </div>
        ))}
      </div>

      <div className={styles.numberSection}>
        <h3>✅ Availability</h3>
        {data.availability.map((item, idx) => (
          <div key={idx} className={styles.numberCard}>
            <div className={styles.numberValue}>{item.tier}</div>
            <div className={styles.numberOp}>{item.downtime_per_year} downtime/year</div>
            <div className={styles.numberUsage}>{item.usage}</div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderFramework = (data: FrameworkData) => (
    <div className={styles.frameworkContent}>
      <div className={styles.frameworkOverview}>
        <p>{data.overview}</p>
        <div className={styles.timeAllocation}>
          <h4>⏱️ Time Allocation ({data.time_allocation.total_time})</h4>
          <ul>
            <li><strong>Requirements:</strong> {data.time_allocation.requirements}</li>
            <li><strong>High-Level Design:</strong> {data.time_allocation.high_level_design}</li>
            <li><strong>Deep Dives:</strong> {data.time_allocation.deep_dives}</li>
            <li><strong>Wrap-Up:</strong> {data.time_allocation.wrap_up}</li>
          </ul>
        </div>
      </div>

      {data.phases.map((phase, idx) => (
        <div key={idx} className={styles.phase}>
          <h3>{phase.phase}</h3>
          <div className={styles.phaseDetails}>
            <div className={styles.phaseTime}>⏱️ {phase.time}</div>
            <div className={styles.phaseGoal}>🎯 {phase.goal}</div>
          </div>

          {phase.activities && (
            <div className={styles.phaseSection}>
              <h4>Activities:</h4>
              <ul>
                {phase.activities.map((activity, i) => (
                  <li key={i}>{activity}</li>
                ))}
              </ul>
            </div>
          )}

          {phase.common_mistakes && (
            <div className={styles.phaseSection}>
              <h4>❌ Common Mistakes:</h4>
              <ul>
                {phase.common_mistakes.map((mistake, i) => (
                  <li key={i}>{mistake}</li>
                ))}
              </ul>
            </div>
          )}

          {phase.example_questions && (
            <div className={styles.phaseSection}>
              <h4>💡 Example Questions:</h4>
              <ul>
                {phase.example_questions.map((q, i) => (
                  <li key={i}>{q}</li>
                ))}
              </ul>
            </div>
          )}

          {phase.tips && (
            <div className={styles.phaseSection}>
              <h4>💡 Tips:</h4>
              <ul>
                {phase.tips.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>
            </div>
          )}

          {phase.areas && (
            <div className={styles.phaseSection}>
              <h4>Deep Dive Areas:</h4>
              {phase.areas.map((area, i) => (
                <div key={i} className={styles.deepDiveArea}>
                  <strong>{area.topic}</strong>
                  <ul>
                    {area.questions.map((q, j) => (
                      <li key={j}>{q}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}

          {phase.reflection_questions && (
            <div className={styles.phaseSection}>
              <h4>🤔 Reflection Questions:</h4>
              <ul>
                {phase.reflection_questions.map((q, i) => (
                  <li key={i}>{q}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}

      <div className={styles.bestPractices}>
        <h3>✨ Best Practices</h3>
        <ul>
          {data.best_practices.map((practice, idx) => (
            <li key={idx}>{practice}</li>
          ))}
        </ul>
      </div>
    </div>
  );

  const renderRubric = (data: RubricData) => (
    <div className={styles.rubricContent}>
      <div className={styles.rubricOverview}>
        <p>{data.overview}</p>
      </div>

      {data.competencies.map((comp, idx) => (
        <div key={idx} className={styles.competency}>
          <h3>
            {comp.name} <span className={styles.weight}>({comp.weight})</span>
          </h3>
          <p className={styles.compDescription}>{comp.description}</p>

          <div className={styles.levels}>
            <div className={styles.levelStrong}>
              <h4>✅ Strong</h4>
              <ul>
                {comp.levels.strong.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>

            <div className={styles.levelAdequate}>
              <h4>➖ Adequate</h4>
              <ul>
                {comp.levels.adequate.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>

            <div className={styles.levelWeak}>
              <h4>❌ Weak</h4>
              <ul>
                {comp.levels.weak.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className={styles.improvement}>
            <h4>📈 How to Improve:</h4>
            <ul>
              {comp.how_to_improve.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      ))}

      <div className={styles.expectations}>
        <h3>🎯 Level Expectations</h3>
        <div className={styles.expectationsGrid}>
          <div className={styles.levelExpectation}>
            <h4>Mid-Level</h4>
            <ul>
              {data.level_expectations.mid_level.expectations.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
          <div className={styles.levelExpectation}>
            <h4>Senior</h4>
            <ul>
              {data.level_expectations.senior.expectations.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
          <div className={styles.levelExpectation}>
            <h4>Staff+</h4>
            <ul>
              {data.level_expectations.staff_plus.expectations.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className={styles.flags}>
        <div className={styles.redFlags}>
          <h4>🚩 Red Flags</h4>
          <ul>
            {data.red_flags.map((flag, i) => (
              <li key={i}>{flag}</li>
            ))}
          </ul>
        </div>
        <div className={styles.greenFlags}>
          <h4>🟢 Green Flags</h4>
          <ul>
            {data.green_flags.map((flag, i) => (
              <li key={i}>{flag}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );

  const renderPatterns = (data: PatternsData) => (
    <div className={styles.patternsContent}>
      {Object.entries(data).map(([key, pattern]) => (
        <div key={key} className={styles.pattern}>
          <h3>{pattern.title}</h3>
          <p className={styles.patternProblem}><strong>Problem:</strong> {pattern.problem}</p>

          <div className={styles.useCases}>
            <h4>Use Cases:</h4>
            <ul>
              {pattern.use_cases.map((useCase, i) => (
                <li key={i}>{useCase}</li>
              ))}
            </ul>
          </div>

          {pattern.approaches && (
            <div className={styles.approaches}>
              <h4>Approaches:</h4>
              {pattern.approaches.map((approach, i) => (
                <div key={i} className={styles.approach}>
                  <h5>{approach.name}</h5>
                  <p>{approach.description}</p>
                  <div className={styles.proscons}>
                    <div className={styles.pros}>
                      <strong>✅ Pros:</strong>
                      <ul>
                        {approach.pros.map((pro, j) => (
                          <li key={j}>{pro}</li>
                        ))}
                      </ul>
                    </div>
                    <div className={styles.cons}>
                      <strong>❌ Cons:</strong>
                      <ul>
                        {approach.cons.map((con, j) => (
                          <li key={j}>{con}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                  <p className={styles.whenToUse}><strong>When to use:</strong> {approach.when_to_use}</p>
                </div>
              ))}
            </div>
          )}

          {pattern.strategies && (
            <div className={styles.strategies}>
              <h4>Strategies:</h4>
              {pattern.strategies.map((strategy, i) => (
                <div key={i} className={styles.strategy}>
                  <h5>{strategy.name}</h5>
                  <p>{strategy.description}</p>
                  {strategy.latency_improvement && (
                    <p className={styles.improvement}>
                      <strong>Improvement:</strong> {strategy.latency_improvement}
                    </p>
                  )}
                  {strategy.throughput_improvement && (
                    <p className={styles.improvement}>
                      <strong>Improvement:</strong> {strategy.throughput_improvement}
                    </p>
                  )}
                  <p className={styles.whenToUse}><strong>When to use:</strong> {strategy.when_to_use}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );

  const renderContent = () => {
    if (loading) return <div className={styles.loading}>Loading...</div>;
    if (!data) return null;

    switch (selectedType) {
      case "numbers":
        return renderNumbers(data as NumbersData);
      case "framework":
        return renderFramework(data as FrameworkData);
      case "rubric":
        return renderRubric(data as RubricData);
      case "patterns":
        return renderPatterns(data as PatternsData);
      default:
        return null;
    }
  };

  return (
    <>
      <button className={styles.triggerButton} onClick={() => setIsOpen(true)}>
        📚 Reference
      </button>

      {isOpen && (
        <div className={styles.modal} onClick={() => setIsOpen(false)}>
          <div
            className={styles.modalContent}
            onClick={(e) => e.stopPropagation()}
          >
            <div className={styles.modalHeader}>
              <h2>System Design Reference</h2>
              <button className={styles.closeButton} onClick={() => setIsOpen(false)}>
                ✕
              </button>
            </div>

            <div className={styles.tabs}>
              <button
                className={selectedType === "numbers" ? styles.tabActive : styles.tab}
                onClick={() => handleTypeChange("numbers")}
              >
                📊 Numbers to Know
              </button>
              <button
                className={selectedType === "framework" ? styles.tabActive : styles.tab}
                onClick={() => handleTypeChange("framework")}
              >
                🎯 Framework
              </button>
              <button
                className={selectedType === "rubric" ? styles.tabActive : styles.tab}
                onClick={() => handleTypeChange("rubric")}
              >
                📋 Rubric
              </button>
              <button
                className={selectedType === "patterns" ? styles.tabActive : styles.tab}
                onClick={() => handleTypeChange("patterns")}
              >
                🔧 Patterns
              </button>
            </div>

            <div className={styles.content}>{renderContent()}</div>
          </div>
        </div>
      )}
    </>
  );
}
