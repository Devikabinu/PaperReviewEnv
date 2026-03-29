import os
import yaml
from fastapi.testclient import TestClient
from api.main import app

def test_openenv_yaml_valid():
    yaml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "openenv.yaml")
    assert os.path.exists(yaml_path)
    
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    required_keys = ["name", "version", "description", "tasks", "observation_space", "action_space", "reward_range", "endpoints"]
    for key in required_keys:
        assert key in config
        
    assert len(config["tasks"]) == 3
    
    difficulties = set()
    for task in config["tasks"]:
        assert "id" in task
        assert "name" in task
        assert "difficulty" in task
        assert "description" in task
        assert "target_score_range" in task
        difficulties.add(task["difficulty"])
        
    assert difficulties == {"easy", "medium", "hard"}

def test_api_endpoints():
    client = TestClient(app)
    
    res = client.get("/health")
    assert res.status_code == 200
    
    res = client.get("/tasks")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) == 3
    
    res = client.post("/reset", json={"task_id": "task_easy"})
    assert res.status_code == 200
    assert res.json()["task_id"] == "task_easy"
