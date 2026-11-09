"""Threshold calibration utilities (Section 7)."""

from typing import List, Tuple
import numpy as np


class ThresholdCalibrator:
    @staticmethod
    def calibrate_from_quantile(values: List[float], quantile: float = 0.25) -> float:
        return float(np.quantile(values, quantile))

    @staticmethod
    def calibrate_balanced_accuracy(
        positive_values: List[float], negative_values: List[float],
    ) -> Tuple[float, float]:
        candidates = sorted(set(positive_values) | set(negative_values))
        best_thr, best_score = candidates[0], 0.0
        for thr in candidates:
            tpr = sum(1 for v in positive_values if v >= thr) / max(len(positive_values), 1)
            tnr = sum(1 for v in negative_values if v < thr) / max(len(negative_values), 1)
            score = (tpr + tnr) / 2
            if score > best_score:
                best_thr, best_score = thr, score
        return float(best_thr), float(best_score)
