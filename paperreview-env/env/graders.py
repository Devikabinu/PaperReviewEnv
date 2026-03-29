from env.models import ReviewAction

def compute_score_alignment(action: ReviewAction, ground_truth: dict, tolerance: float = 0.2) -> float:
    dimensions = ["novelty_score", "methodology_score", "statistical_validity_score", 
                  "reproducibility_score", "clarity_score"]
    scores = []
    for dim in dimensions:
        if dim in ground_truth:
            diff = abs(getattr(action, dim) - ground_truth[dim])
            dim_score = max(0.0, 1.0 - (diff / tolerance))
            scores.append(dim_score)
    return sum(scores) / len(scores) if scores else 0.0

def compute_justification_quality(action: ReviewAction, keyword_signals: dict) -> float:
    fields = {
        "novelty": (action.novelty_justification, keyword_signals.get("novelty", [])),
        "methodology": (action.methodology_justification, keyword_signals.get("methodology", [])),
        "statistical": (action.statistical_justification, keyword_signals.get("statistical", [])),
        "reproducibility": (action.reproducibility_justification, keyword_signals.get("reproducibility", [])),
        "clarity": (action.clarity_justification, keyword_signals.get("clarity", []))
    }
    dimension_scores = []
    for dim, (justification, keywords) in fields.items():
        length_score = min(1.0, len(justification.split()) / 15)  # full credit at 15+ words
        if keywords:
            keyword_hits = sum(1 for kw in keywords if kw.lower() in justification.lower())
            keyword_score = min(1.0, keyword_hits / max(1, len(keywords) * 0.3))  # need 30% of keywords
        else:
            keyword_score = 0.5
        dimension_scores.append(0.5 * length_score + 0.5 * keyword_score)
    return sum(dimension_scores) / len(dimension_scores)

def compute_penalties(action: ReviewAction) -> tuple[float, list[str]]:
    penalties = 0.0
    reasons = []
    
    all_scores = [action.novelty_score, action.methodology_score, 
                  action.statistical_validity_score, action.reproducibility_score, 
                  action.clarity_score]
    if len(set(round(s, 2) for s in all_scores)) == 1:
        penalties -= 0.2
        reasons.append("all_scores_identical")
    
    short_justifications = sum(1 for j in [
        action.novelty_justification, action.methodology_justification,
        action.statistical_justification, action.reproducibility_justification,
        action.clarity_justification
    ] if len(j.split()) < 10)
    if short_justifications >= 3:
        penalties -= 0.1
        reasons.append("too_many_short_justifications")
    
    avg_score = sum(all_scores) / len(all_scores)
    if avg_score > 0.75 and action.overall_recommendation == "reject":
        penalties -= 0.3
        reasons.append("recommendation_contradicts_scores_reject_with_high_scores")
    if avg_score < 0.35 and action.overall_recommendation == "accept":
        penalties -= 0.3
        reasons.append("recommendation_contradicts_scores_accept_with_low_scores")
    
    return penalties, reasons

def compute_confidence_calibration(action: ReviewAction, actual_performance: float) -> float:
    diff = abs(action.confidence - actual_performance)
    return max(0.0, 1.0 - diff * 2)
