"use client";

import QuizAssessment from "./QuizAssessment";
import { TestSession } from "@/lib/quizStorage";
import type { AssessmentScores } from "@/lib/quizStorage";

interface TestAssessmentProps {
  session: TestSession;
  onComplete: (scores: AssessmentScores) => void;
}

export default function TestAssessment({ session, onComplete }: TestAssessmentProps) {
  const testSessionAsQuizSession = {
    ...session,
    mode: 'practice' as const,
    questions: [],
    answers: {},
  };

  return (
    <QuizAssessment
      session={testSessionAsQuizSession}
      onComplete={onComplete}
    />
  );
}
