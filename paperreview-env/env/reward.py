from env.models import ReviewAction, RewardBreakdown
from env.graders import (
    compute_score_alignment,
    compute_justification_quality,
    compute_penalties,
    compute_confidence_calibration
)

def compute_reward(action: ReviewAction, paper: dict) -> RewardBreakdown:
    gt = paper["ground_truth"]
    score_alignment = compute_score_alignment(action, gt)
    recommendation_correct = 1.0 if action.overall_recommendation == gt["recommendation"] else 0.0
    justification_quality = compute_justification_quality(action, gt["keyword_signals"])
    penalties, penalty_reasons = compute_penalties(action)
    
    raw_total = (
        0.30 * score_alignment +
        0.25 * recommendation_correct +
        0.25 * justification_quality +
        0.10 * 0.5 +  # placeholder until confidence calibration computed below
        0.10 * min(score_alignment, justification_quality)  # partial credit
    )
    
    confidence_calibration = compute_confidence_calibration(action, raw_total)
    
    total = max(0.0, min(1.0, (
        0.30 * score_alignment +
        0.25 * recommendation_correct +
        0.25 * justification_quality +
        0.10 * confidence_calibration +
        0.10 * min(score_alignment, justification_quality) +
        penalties
    )))
    
    return RewardBreakdown(
        total=total,
        score_alignment=score_alignment,
        recommendation_correct=recommendation_correct,
        justification_quality=justification_quality,
        confidence_calibration=confidence_calibration,
        partial_credit=min(score_alignment, justification_quality),
        penalties=penalties,
        penalty_reasons=penalty_reasons
    )
