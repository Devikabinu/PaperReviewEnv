from fastapi import APIRouter, Request, HTTPException
from typing import List
from pydantic import BaseModel

from env.models import (
    PaperObservation, 
    ReviewAction, 
    StepResult, 
    EnvironmentState,
    TaskInfo,
    RewardBreakdown
)
from env.tasks import TASKS
from baseline.inference import run_baseline

router = APIRouter()

class ResetRequest(BaseModel):
    task_id: str

class GraderRequest(BaseModel):
    episode_history: List[dict] = []

class GraderResponse(BaseModel):
    task_id: str
    final_score: float
    breakdown: RewardBreakdown
    grader_version: str

@router.post("/reset", response_model=PaperObservation)
def reset_env(request: Request, body: ResetRequest):
    env = request.app.state.env
    try:
        obs = env.reset(body.task_id)
        return obs
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/step", response_model=StepResult)
def step_env(request: Request, action: ReviewAction):
    env = request.app.state.env
    try:
        result = env.step(action)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/state", response_model=EnvironmentState)
def get_state(request: Request):
    env = request.app.state.env
    return env.state()

@router.get("/tasks", response_model=List[TaskInfo])
def get_tasks():
    return [TaskInfo(**task) for task in TASKS.values()]

@router.post("/grader", response_model=GraderResponse)
def run_grader(request: Request, body: GraderRequest):
    env = request.app.state.env
    
    history = body.episode_history
    if not history:
        history = env.get_episode_history()
        
    if not history:
        raise HTTPException(status_code=400, detail="No episode history found.")
        
    last_step = history[-1]
    obs = last_step.get("observation", {})
    reward_dict = last_step.get("reward", {})
    
    task_id = obs.get("task_id", "unknown")
    final_score = reward_dict.get("total", 0.0)
    
    return GraderResponse(
        task_id=task_id,
        final_score=final_score,
        breakdown=RewardBreakdown.model_validate(reward_dict),
        grader_version="1.0.0"
    )

@router.post("/baseline")
def execute_baseline(request: Request):
    base_url = f"http://127.0.0.1:7860" # Local container port inside standard OpenEnv config
    try:
        results = run_baseline(base_url)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
