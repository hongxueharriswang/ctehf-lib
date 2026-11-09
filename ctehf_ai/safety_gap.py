"""Educational safety gap (Section 6.1)."""

from enum import Enum


def safety_gap(perf_ai: float, perf_indep: float) -> float:
    return float(perf_ai - perf_indep)


class SafetyGapInterpretation(Enum):
    BALANCED = "balanced"
    AI_DEPENDENCE = "ai_dependence"
    MEASUREMENT_ANOMALY = "measurement_anomaly"
    LARGE_DIVERGENCE = "large_divergence"


def interpret_safety_gap(
    gap: float, small_threshold: float = 0.05, large_threshold: float = 0.25
) -> SafetyGapInterpretation:
    if abs(gap) <= small_threshold:
        return SafetyGapInterpretation.BALANCED
    if abs(gap) >= large_threshold:
        return SafetyGapInterpretation.LARGE_DIVERGENCE
    return (SafetyGapInterpretation.AI_DEPENDENCE if gap > 0
            else SafetyGapInterpretation.MEASUREMENT_ANOMALY)


def recommended_response(interp: SafetyGapInterpretation) -> str:
    return {
        SafetyGapInterpretation.BALANCED:
            "Sustain current dual-preparation design; monitor for drift.",
        SafetyGapInterpretation.AI_DEPENDENCE:
            "Increase AI-free practice; introduce productive struggle; "
            "redesign assessment to require independent demonstration.",
        SafetyGapInterpretation.MEASUREMENT_ANOMALY:
            "Investigate measurement or pedagogical anomaly.",
        SafetyGapInterpretation.LARGE_DIVERGENCE:
            "Flag for individual pedagogical review; consider SCAM-informed intervention.",
    }[interp]
