import yaml
import os
from env.models import ReviewAction

def load_tasks():
    # Attempt to load tasks from openenv.yaml
    yaml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "openenv.yaml")
    
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    tasks_dict = {}
    for task in config.get("tasks", []):
        task_copy = dict(task)
        task_copy["action_schema"] = ReviewAction.model_json_schema()
        tasks_dict[task["id"]] = task_copy
        
    return tasks_dict

TASKS = load_tasks()
