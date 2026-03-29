---
title: PaperReviewEnv
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---

# PaperReviewEnv

## Environment Description and Motivation
PaperReviewEnv is a peer review simulation environment where AI agents act as academic reviewers. They evaluate scientific papers across five critical dimensions: novelty, methodology, statistical validity, reproducibility, and clarity. The motivation is to train and evaluate AI systems on their ability to detect subtle flaws in research methodology and statistical reporting, a crucial skill for automated scientific evaluation and AI safety.

## Action Space
The `ReviewAction` model requires agents to provide scores (0.0 to 1.0) and textual justifications (minimum 20 characters) for five dimensions:
- Novelty
- Methodology
- Statistical Validity
- Reproducibility
- Clarity
It also requires an `overall_recommendation` ("accept", "minor_revision", "major_revision", or "reject") and a `confidence` score.

## Observation Space
The `PaperObservation` provides the agent with:
- The `paper_id` and the text of the paper broken down into: `title`, `abstract`, `introduction`, `methods`, `results`, and `conclusions`.
- Metadata including `task_id`, `task_description`, `step_number`, and `max_steps`.

## Task Descriptions

### Task 1: Flag Obvious Flaws (Easy)
- **Difficulty:** easy
- **Description:** Paper has 4 planted, obvious flaws (e.g., n=3 patients, p<0.05 without specific values, missing methods). Agent must identify them and recommend rejection.
- **Expected Difficulty & Target Score:** 0.80 - 0.95

### Task 2: Assess Mixed Quality Paper (Medium)
- **Difficulty:** medium
- **Description:** Paper has genuine strengths but real weaknesses (e.g., small dataset, no ablation study, overclaimed conclusions). Agent must score each dimension correctly and recommend major revision.
- **Expected Difficulty & Target Score:** 0.55 - 0.75

### Task 3: Detect Subtle Statistical Manipulation (Hard)
- **Difficulty:** hard
- **Description:** Paper appears polished but contains subtle statistical issues (p-hacking, cherry-picked baselines, HARKing). Agent must detect these and recommend major revision.
- **Expected Difficulty & Target Score:** 0.35 - 0.55

## Setup and Usage Instructions
1. Install requirements: `pip install -r requirements.txt`
2. Run API: `uvicorn api.main:app --host 0.0.0.0 --port 7860`
3. Test with the baseline script: `python -c "from baseline.inference import run_baseline; run_baseline('http://localhost:7860')"`

## Docker Instructions
1. Build the container: `docker build -t paperreview-env .`
2. Run the container: `docker run -p 7860:7860 paperreview-env`

## Baseline Score Table
Baseline models typically score as follows:
- Easy: ~0.85
- Medium: ~0.65
- Hard: ~0.45

## How Graders Work
Graders consist of fully deterministic, stateless Python functions. They compute rewards based on:
1. **Score Alignment:** Proximity of predicted scores to ground truth scores.
2. **Justification Quality:** Based on keyword signal hits in justifications and length of text.
3. **Recommendation Correctness:** Strict matching of the final editorial recommendation.
4. **Confidence Calibration:** Proximity of agent confidence to actual performance in the step.
5. **Penalties:** Applied for identical scores across dimensions, overly short justifications, or contradictory recommendations (e.g., high scores but a reject recommendation).
