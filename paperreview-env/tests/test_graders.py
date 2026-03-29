import pytest
from env.models import ReviewAction
from env.reward import compute_reward
from env.papers import PAPERS

def create_action(overrides=None):
    base = {
        "novelty_score": 0.5, "novelty_justification": "This is a dummy justification that needs to be at least twenty words long so I am going to keep writing until it is definitely more than twenty words.",
        "methodology_score": 0.5, "methodology_justification": "This is a dummy justification that needs to be at least twenty words long so I am going to keep writing until it is definitely more than twenty words.",
        "statistical_validity_score": 0.5, "statistical_justification": "This is a dummy justification that needs to be at least twenty words long so I am going to keep writing until it is definitely more than twenty words.",
        "reproducibility_score": 0.5, "reproducibility_justification": "This is a dummy justification that needs to be at least twenty words long so I am going to keep writing until it is definitely more than twenty words.",
        "clarity_score": 0.5, "clarity_justification": "This is a dummy justification that needs to be at least twenty words long so I am going to keep writing until it is definitely more than twenty words.",
        "overall_recommendation": "major_revision",
        "confidence": 0.5
    }
    if overrides:
        base.update(overrides)
    return ReviewAction(**base)

def test_perfect_action_reward():
    paper = PAPERS[0]
    gt = paper["ground_truth"]
    
    action = create_action({
        "novelty_score": gt["novelty_score"],
        "methodology_score": gt["methodology_score"],
        "statistical_validity_score": gt["statistical_validity_score"],
        "reproducibility_score": gt["reproducibility_score"],
        "clarity_score": gt["clarity_score"],
        "overall_recommendation": gt["recommendation"],
    })
    
    # Inject keywords to get high justification score
    kw = gt["keyword_signals"]
    if kw.get("novelty"): action.novelty_justification += " " + " ".join(kw["novelty"])
    if kw.get("methodology"): action.methodology_justification += " " + " ".join(kw["methodology"])
    if kw.get("statistical"): action.statistical_justification += " " + " ".join(kw["statistical"])
    if kw.get("reproducibility"): action.reproducibility_justification += " " + " ".join(kw["reproducibility"])
    if kw.get("clarity"): action.clarity_justification += " " + " ".join(kw["clarity"])
    
    action.confidence = 1.0 # High confidence for high score
    
    reward = compute_reward(action, paper)
    assert reward.total > 0.8

def test_terrible_action_reward():
    paper = PAPERS[0]
    # Wrong recommendation, wrong scores, short justifications
    action = ReviewAction(
        novelty_score=0.9, novelty_justification="this justification is suitably terrible but over 20 chars",
        methodology_score=0.9, methodology_justification="this justification is suitably terrible but over 20 chars",
        statistical_validity_score=0.9, statistical_justification="this justification is suitably terrible but over 20 chars",
        reproducibility_score=0.9, reproducibility_justification="this justification is suitably terrible but over 20 chars",
        clarity_score=0.9, clarity_justification="this justification is suitably terrible but over 20 chars",
        overall_recommendation="accept" if paper["ground_truth"]["recommendation"] != "accept" else "reject",
        confidence=1.0 # Miss-calibrated
    )
    reward = compute_reward(action, paper)
    assert reward.total < 0.4

def test_graders_return_different_scores():
    paper = PAPERS[0]
    actions = [
        create_action({"novelty_score": 0.8, "methodology_score": 0.4, "statistical_validity_score": 0.1, "reproducibility_score": 0.3, "clarity_score": 0.9}),
        create_action({"novelty_score": 0.2, "methodology_score": 0.7, "statistical_validity_score": 0.5, "reproducibility_score": 0.2, "clarity_score": 0.4}),
        create_action({"novelty_score": 0.5, "methodology_score": 0.5, "statistical_validity_score": 0.5, "reproducibility_score": 0.5, "clarity_score": 0.5})
    ]
    
    scores = set()
    for act in actions:
        reward = compute_reward(act, paper)
        # Round slightly to handle floating point noise
        scores.add(round(reward.total, 4))
        
    assert len(scores) >= 3, "Graders did not return 3 different scores for 3 distinct actions"

def test_identical_scores_penalty():
    paper = PAPERS[0]
    action = create_action({"novelty_score": 0.7, "methodology_score": 0.7, "statistical_validity_score": 0.7, "reproducibility_score": 0.7, "clarity_score": 0.7})
    reward = compute_reward(action, paper)
    assert "all_scores_identical" in reward.penalty_reasons

def test_contradictory_recommendation_penalty():
    paper = PAPERS[0]
    action = create_action({
        "novelty_score": 0.9, 
        "methodology_score": 0.9, 
        "statistical_validity_score": 0.9, 
        "reproducibility_score": 0.9, 
        "clarity_score": 0.85, # Average is approx 0.89
        "overall_recommendation": "reject"
    })
    reward = compute_reward(action, paper)
    assert "recommendation_contradicts_scores_reject_with_high_scores" in reward.penalty_reasons

def test_rewards_in_range():
    paper = PAPERS[0]
    action = create_action({"confidence": 1.0})
    reward = compute_reward(action, paper)
    assert 0.0 <= reward.total <= 1.0
