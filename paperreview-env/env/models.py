from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class PaperObservation(BaseModel):
    paper_id: str = Field(description="Unique identifier for the paper")
    title: str = Field(description="Title of the paper")
    abstract: str = Field(description="Abstract of the paper")
    introduction: str = Field(description="Introduction section")
    methods: str = Field(description="Methods section")
    results: str = Field(description="Results section")
    conclusions: str = Field(description="Conclusions section")
    task_id: str = Field(description="Current task identifier")
    task_description: str = Field(description="Human-readable task objective")
    step_number: int = Field(description="Current step in the episode")
    max_steps: int = Field(description="Maximum steps allowed per episode")

class ReviewAction(BaseModel):
    novelty_score: float = Field(ge=0.0, le=1.0, description="Score for novelty of contribution (0=not novel, 1=highly novel)")
    novelty_justification: str = Field(min_length=20, description="Justification for novelty score, minimum 20 characters")
    methodology_score: float = Field(ge=0.0, le=1.0, description="Score for soundness of methodology (0=flawed, 1=rigorous)")
    methodology_justification: str = Field(min_length=20, description="Justification for methodology score")
    statistical_validity_score: float = Field(ge=0.0, le=1.0, description="Score for statistical validity (0=invalid, 1=valid)")
    statistical_justification: str = Field(min_length=20, description="Justification for statistical validity score")
    reproducibility_score: float = Field(ge=0.0, le=1.0, description="Score for reproducibility (0=not reproducible, 1=fully reproducible)")
    reproducibility_justification: str = Field(min_length=20, description="Justification for reproducibility score")
    clarity_score: float = Field(ge=0.0, le=1.0, description="Score for writing clarity (0=unclear, 1=exemplary)")
    clarity_justification: str = Field(min_length=20, description="Justification for clarity score")
    overall_recommendation: Literal["accept", "minor_revision", "major_revision", "reject"] = Field(description="Final editorial recommendation")
    confidence: float = Field(ge=0.0, le=1.0, description="Agent confidence in its review (0=uncertain, 1=certain)")

class RewardBreakdown(BaseModel):
    total: float = Field(ge=0.0, le=1.0, description="Overall reward for this step")
    score_alignment: float = Field(ge=0.0, le=1.0, description="How well numeric scores match ground truth within tolerance")
    recommendation_correct: float = Field(ge=0.0, le=1.0, description="1.0 if recommendation matches ground truth, 0.0 otherwise")
    justification_quality: float = Field(ge=0.0, le=1.0, description="Quality of justifications based on keyword coverage and length")
    confidence_calibration: float = Field(ge=0.0, le=1.0, description="Whether confidence matches actual performance")
    partial_credit: float = Field(ge=0.0, le=1.0, description="Partial progress signal even in failed episodes")
    penalties: float = Field(ge=-1.0, le=0.0, description="Deductions for bad behavior")
    penalty_reasons: List[str] = Field(default_factory=list, description="List of reasons for penalties applied")

class StepResult(BaseModel):
    observation: PaperObservation = Field(description="Next observation after the action")
    reward: RewardBreakdown = Field(description="Reward breakdown for this step")
    done: bool = Field(description="Whether the episode is complete")
    info: dict = Field(default_factory=dict, description="Additional diagnostic information")

class EnvironmentState(BaseModel):
    current_task_id: Optional[str] = Field(description="Active task ID or null if not started")
    current_paper_id: Optional[str] = Field(description="Active paper ID or null if not started")
    step_number: int = Field(description="Current step count")
    episode_active: bool = Field(description="Whether an episode is currently running")
    last_reward: Optional[float] = Field(description="Reward from last step or null")

class TaskInfo(BaseModel):
    id: str = Field(description="Task identifier")
    name: str = Field(description="Human-readable task name")
    difficulty: str = Field(description="easy | medium | hard")
    description: str = Field(description="What the agent must accomplish")
    target_score_range: List[float] = Field(description="Expected score range for frontier models")
    action_schema: dict = Field(description="JSON schema of the ReviewAction model")
