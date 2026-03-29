from typing import Optional, List, Dict, Any
from env.models import (
    PaperObservation, 
    ReviewAction, 
    StepResult, 
    EnvironmentState
)
from env.tasks import TASKS
from env.papers import get_paper_by_task
from env.reward import compute_reward

class PaperReviewEnv:
    def __init__(self):
        self.current_task_id: Optional[str] = None
        self.current_paper: Optional[dict] = None
        self.step_number: int = 0
        self.episode_active: bool = False
        self.last_reward: Optional[float] = None
        self._episode_history: List[dict] = []
        self._global_step_counter: int = 0

    def reset(self, task_id: str) -> PaperObservation:
        if task_id not in TASKS:
            raise ValueError(f"Invalid task_id: {task_id}")
        
        self.current_task_id = task_id
        self.current_paper = get_paper_by_task(task_id, self._global_step_counter)
        self.step_number = 0
        self.episode_active = True
        self.last_reward = None
        self._episode_history = []
        self._global_step_counter += 1
        
        task_info = TASKS[task_id]
        
        obs = PaperObservation(
            paper_id=self.current_paper["paper_id"],
            title=self.current_paper["title"],
            abstract=self.current_paper["abstract"],
            introduction=self.current_paper["introduction"],
            methods=self.current_paper["methods"],
            results=self.current_paper["results"],
            conclusions=self.current_paper["conclusions"],
            task_id=task_id,
            task_description=task_info["description"],
            step_number=self.step_number,
            max_steps=1
        )
        return obs

    def step(self, action: ReviewAction) -> StepResult:
        if not self.episode_active or self.current_paper is None:
            raise RuntimeError("Episode not active.")
            
        reward_breakdown = compute_reward(action, self.current_paper)
        self.last_reward = reward_breakdown.total
        
        done = True
        self.episode_active = False
        
        obs = PaperObservation(
            paper_id=self.current_paper["paper_id"],
            title=self.current_paper["title"],
            abstract=self.current_paper["abstract"],
            introduction=self.current_paper["introduction"],
            methods=self.current_paper["methods"],
            results=self.current_paper["results"],
            conclusions=self.current_paper["conclusions"],
            task_id=self.current_task_id,
            task_description=TASKS[self.current_task_id]["description"],
            step_number=self.step_number + 1,
            max_steps=1
        )
        
        result = StepResult(
            observation=obs,
            reward=reward_breakdown,
            done=done,
            info={"paper_flaws": self.current_paper["ground_truth"]["known_flaws"]}
        )
        
        self._episode_history.append({
            "observation": obs.model_dump(),
            "action": action.model_dump(),
            "reward": reward_breakdown.model_dump(),
            "done": done,
            "info": result.info
        })
        
        self.step_number += 1
        return result

    def state(self) -> EnvironmentState:
        return EnvironmentState(
            current_task_id=self.current_task_id,
            current_paper_id=self.current_paper["paper_id"] if self.current_paper else None,
            step_number=self.step_number,
            episode_active=self.episode_active,
            last_reward=self.last_reward
        )

    def get_episode_history(self) -> List[dict]:
        return self._episode_history
