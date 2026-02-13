"use client";

import { useState } from "react";
import {
  QuizSession,
  AssessmentScores,
  AssessmentScore,
} from "@/lib/quizStorage";
import styles from "./PracticeMode.module.css";

interface QuizAssessmentProps {
  session: QuizSession;
  onComplete: (scores: AssessmentScores) => void;
}

const DELIVERY_FRAMEWORK_CRITERIA = [
  "Clarified requirements (functional + non-functional)",
  "Identified core entities and relationships",
  "Drew high-level system diagram",
  "Explained component interactions",
  "Deep dived into 2-3 critical areas",
  "Discussed trade-offs and alternatives",
];

const COMPETENCY_CRITERIA = [
  "Problem Navigation: Asked clarifying questions, prioritized correctly",
  "Solution Design: Well-structured, scalable architecture",
  "Technical Excellence: Chose appropriate technologies, explained trade-offs",
  "Communication: Clear explanations, showed reasoning",
];

const TECHNOLOGY_CRITERIA = [
  "Identified correct technology for requirements",
  "Explained WHY this technology fits",
  "Discussed key pros and cons",
  "Mentioned limitations and edge cases",
  "Compared with alternatives",
  "Considered scale, latency, consistency implications",
];

export default function QuizAssessment({
  session,
  onComplete,
}: QuizAssessmentProps) {
  const [deliveryFramework, setDeliveryFramework] = useState<
    AssessmentScore[]
  >(
    DELIVERY_FRAMEWORK_CRITERIA.map((criterion) => ({
      criterion,
      score: "adequate" as const,
    }))
  );

  const [competencies, setCompetencies] = useState<AssessmentScore[]>(
    COMPETENCY_CRITERIA.map((criterion) => ({
      criterion,
      score: "adequate" as const,
    }))
  );

  const [technologySpecific, setTechnologySpecific] = useState<
    AssessmentScore[]
  >(
    TECHNOLOGY_CRITERIA.map((criterion) => ({
      criterion,
      score: "adequate" as const,
    }))
  );

  const updateScore = (
    category: "delivery" | "competency" | "technology",
    index: number,
    score: "strong" | "adequate" | "weak"
  ) => {
    if (category === "delivery") {
      const updated = [...deliveryFramework];
      updated[index] = { ...updated[index], score };
      setDeliveryFramework(updated);
    } else if (category === "competency") {
      const updated = [...competencies];
      updated[index] = { ...updated[index], score };
      setCompetencies(updated);
    } else {
      const updated = [...technologySpecific];
      updated[index] = { ...updated[index], score };
      setTechnologySpecific(updated);
    }
  };

  const handleSubmit = () => {
    const scores: AssessmentScores = {
      deliveryFramework,
      competencies,
      technologySpecific,
    };

    onComplete(scores);
  };

  const hasScenarioQuestions = session.questions.some(
    (q) => q.type === "scenario"
  );
  const hasTechQuestions = session.questions.some(
    (q) => q.type === "technology"
  );

  return (
    <div className={styles.assessmentContainer}>
      <div className={styles.assessmentIntro}>
        <h3>Self-Assessment Checklist</h3>
        <p>
          Evaluate your performance across key competencies. Be honest with
          yourself - this helps identify areas for improvement.
        </p>
        <div className={styles.scoreGuide}>
          <div className={styles.scoreItem}>
            <strong>Strong:</strong> Consistently demonstrated excellence
          </div>
          <div className={styles.scoreItem}>
            <strong>Adequate:</strong> Met expectations, room for improvement
          </div>
          <div className={styles.scoreItem}>
            <strong>Weak:</strong> Needs significant work
          </div>
        </div>
      </div>

      {hasScenarioQuestions && (
        <div className={styles.assessmentSection}>
          <h4>A. Delivery Framework Alignment</h4>
          <p className={styles.sectionDescription}>
            For scenario questions, evaluate how well you followed the
            structured interview approach.
          </p>

          {deliveryFramework.map((item, index) => (
            <div key={index} className={styles.assessmentItem}>
              <div className={styles.criterionText}>{item.criterion}</div>
              <div className={styles.scoreOptions}>
                <label className={styles.scoreOption}>
                  <input
                    type="radio"
                    name={`delivery-${index}`}
                    value="strong"
                    checked={item.score === "strong"}
                    onChange={() => updateScore("delivery", index, "strong")}
                  />
                  <span>Strong</span>
                </label>
                <label className={styles.scoreOption}>
                  <input
                    type="radio"
                    name={`delivery-${index}`}
                    value="adequate"
                    checked={item.score === "adequate"}
                    onChange={() => updateScore("delivery", index, "adequate")}
                  />
                  <span>Adequate</span>
                </label>
                <label className={styles.scoreOption}>
                  <input
                    type="radio"
                    name={`delivery-${index}`}
                    value="weak"
                    checked={item.score === "weak"}
                    onChange={() => updateScore("delivery", index, "weak")}
                  />
                  <span>Weak</span>
                </label>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className={styles.assessmentSection}>
        <h4>B. Assessment Rubric Competencies</h4>
        <p className={styles.sectionDescription}>
          Core competencies that interviewers evaluate across all questions.
        </p>

        {competencies.map((item, index) => (
          <div key={index} className={styles.assessmentItem}>
            <div className={styles.criterionText}>{item.criterion}</div>
            <div className={styles.scoreOptions}>
              <label className={styles.scoreOption}>
                <input
                  type="radio"
                  name={`competency-${index}`}
                  value="strong"
                  checked={item.score === "strong"}
                  onChange={() => updateScore("competency", index, "strong")}
                />
                <span>Strong</span>
              </label>
              <label className={styles.scoreOption}>
                <input
                  type="radio"
                  name={`competency-${index}`}
                  value="adequate"
                  checked={item.score === "adequate"}
                  onChange={() => updateScore("competency", index, "adequate")}
                />
                <span>Adequate</span>
              </label>
              <label className={styles.scoreOption}>
                <input
                  type="radio"
                  name={`competency-${index}`}
                  value="weak"
                  checked={item.score === "weak"}
                  onChange={() => updateScore("competency", index, "weak")}
                />
                <span>Weak</span>
              </label>
            </div>
          </div>
        ))}
      </div>

      {hasTechQuestions && (
        <div className={styles.assessmentSection}>
          <h4>C. Technology-Specific Criteria</h4>
          <p className={styles.sectionDescription}>
            For technology selection questions, evaluate your depth of
            understanding.
          </p>

          {technologySpecific.map((item, index) => (
            <div key={index} className={styles.assessmentItem}>
              <div className={styles.criterionText}>{item.criterion}</div>
              <div className={styles.scoreOptions}>
                <label className={styles.scoreOption}>
                  <input
                    type="radio"
                    name={`technology-${index}`}
                    value="strong"
                    checked={item.score === "strong"}
                    onChange={() => updateScore("technology", index, "strong")}
                  />
                  <span>Strong</span>
                </label>
                <label className={styles.scoreOption}>
                  <input
                    type="radio"
                    name={`technology-${index}`}
                    value="adequate"
                    checked={item.score === "adequate"}
                    onChange={() =>
                      updateScore("technology", index, "adequate")
                    }
                  />
                  <span>Adequate</span>
                </label>
                <label className={styles.scoreOption}>
                  <input
                    type="radio"
                    name={`technology-${index}`}
                    value="weak"
                    checked={item.score === "weak"}
                    onChange={() => updateScore("technology", index, "weak")}
                  />
                  <span>Weak</span>
                </label>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className={styles.assessmentActions}>
        <button className={styles.submitButton} onClick={handleSubmit}>
          Complete Assessment
        </button>
      </div>
    </div>
  );
}
