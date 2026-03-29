import os
import json
import httpx
from openai import OpenAI
from env.models import ReviewAction

def run_baseline(base_url: str) -> dict:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "dummy_key")
    OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    MODEL = os.environ.get("BASELINE_MODEL", "gpt-4o-mini")

    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    
    tasks = ["task_easy", "task_medium", "task_hard"]
    task_names = {
        "task_easy": "Task 1 - Flag Obvious Flaws (easy)",
        "task_medium": "Task 2 - Assess Mixed Quality (medium)",
        "task_hard": "Task 3 - Detect Subtle Manipulation (hard)"
    }
    
    results = {}
    total_score = 0.0
    schema = ReviewAction.model_json_schema()
    
    for task_id in tasks:
        try:
            # 1. Reset
            reset_resp = httpx.post(f"{base_url}/reset", json={"task_id": task_id}, timeout=30.0)
            reset_resp.raise_for_status()
            obs = reset_resp.json()
            
            # 2. Extract paper text
            paper_text = (
                f"Title: {obs['title']}\n"
                f"Abstract: {obs['abstract']}\n"
                f"Introduction: {obs['introduction']}\n"
                f"Methods: {obs['methods']}\n"
                f"Results: {obs['results']}\n"
                f"Conclusions: {obs['conclusions']}\n"
            )
            
            # 3. Call LLM
            prompt = (
                f"You are an expert scientific paper reviewer. Please evaluate the following paper based on the task description.\n"
                f"Task Description: {obs['task_description']}\n\n"
                f"Paper:\n{paper_text}\n\n"
                f"Respond ONLY with a JSON object matching this schema. No markdown code blocks, just raw JSON.\n"
                f"Ensure ALL justification fields are at least 20 words long.\n"
                f"Schema:\n{json.dumps(schema, indent=2)}"
            )
            
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            
            llm_text = response.choices[0].message.content.strip()
            
            # 4. Parse JSON
            if llm_text.startswith("```"):
                lines = llm_text.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                llm_text = "\n".join(lines).strip()
                
            action_dict = json.loads(llm_text)
            
            # Validate against model
            action = ReviewAction.model_validate(action_dict)
            
            # 5. Step
            step_resp = httpx.post(f"{base_url}/step", json=action.model_dump(), timeout=30.0)
            step_resp.raise_for_status()
            step_result = step_resp.json()
            
            score = step_result["reward"]["total"]
            results[task_id] = {
                "score": score,
                "raw_reward": step_result["reward"]
            }
            total_score += score
            
        except Exception as e:
            print(f"Error on {task_id}: {e}")
            results[task_id] = {
                "score": 0.0,
                "raw_reward": {"total": 0.0}
            }
            
    avg_score = total_score / len(tasks)
    results["average"] = avg_score
    
    print("========================================")
    print("PaperReviewEnv Baseline Results")
    print("========================================")
    for task_id in tasks:
        score = results[task_id]['score']
        # Left align name, pad appropriately
        # "Task 1 - Flag Obvious Flaws (easy):       0.XX"
        name_part = f"{task_names[task_id]}:"
        print(f"{name_part:<42}{score:.2f}")
    print("----------------------------------------")
    print(f"Average Score:                            {avg_score:.2f}")
    print("========================================")
    
    return results

if __name__ == "__main__":
    url = os.environ.get("ENV_BASE_URL", "http://localhost:7860")
    run_baseline(url)
