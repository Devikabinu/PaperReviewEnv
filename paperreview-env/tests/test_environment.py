import pytest
from env.environment import PaperReviewEnv
from env.models import ReviewAction

def test_reset_valid_tasks():
    env = PaperReviewEnv()
    for task_id in ["task_easy", "task_medium", "task_hard"]:
        obs = env.reset(task_id)
        assert obs.task_id == task_id
        assert obs.paper_id is not None
        assert env.episode_active is True

def test_reset_invalid_task():
    env = PaperReviewEnv()
    with pytest.raises(ValueError):
        env.reset("task_invalid")

def test_step_before_reset():
    env = PaperReviewEnv()
    action = ReviewAction(
        novelty_score=0.5, novelty_justification="a "*20,
        methodology_score=0.5, methodology_justification="a "*20,
        statistical_validity_score=0.5, statistical_justification="a "*20,
        reproducibility_score=0.5, reproducibility_justification="a "*20,
        clarity_score=0.5, clarity_justification="a "*20,
        overall_recommendation="accept", confidence=0.5
    )
    with pytest.raises(RuntimeError):
        env.step(action)

def test_step_done_true():
    env = PaperReviewEnv()
    env.reset("task_easy")
    action = ReviewAction(
        novelty_score=0.5, novelty_justification="a "*20,
        methodology_score=0.5, methodology_justification="b "*20,
        statistical_validity_score=0.5, statistical_justification="c "*20,
        reproducibility_score=0.5, reproducibility_justification="d "*20,
        clarity_score=0.5, clarity_justification="e "*20,
        overall_recommendation="accept", confidence=0.5
    )
    res = env.step(action)
    assert res.done is True
    assert env.episode_active is False

def test_state_before_and_after_reset():
    env = PaperReviewEnv()
    state = env.state()
    assert state.current_task_id is None
    assert state.episode_active is False
    
    env.reset("task_easy")
    state2 = env.state()
    assert state2.current_task_id == "task_easy"
    assert state2.episode_active is True

def test_no_state_leakage():
    env = PaperReviewEnv()
    env.reset("task_easy")
    action = ReviewAction(
        novelty_score=0.1, novelty_justification="a "*20,
        methodology_score=0.2, methodology_justification="b "*20,
        statistical_validity_score=0.3, statistical_justification="c "*20,
        reproducibility_score=0.4, reproducibility_justification="d "*20,
        clarity_score=0.5, clarity_justification="e "*20,
        overall_recommendation="reject", confidence=0.5
    )
    env.step(action)
    assert len(env.get_episode_history()) == 1
    
    env.reset("task_medium")
    assert len(env.get_episode_history()) == 0
    assert env.current_task_id == "task_medium"
    assert env.step_number == 0
