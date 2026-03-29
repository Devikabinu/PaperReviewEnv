from typing import List, Dict, Any

PAPERS: List[Dict[str, Any]] = [
    {
        "paper_id": "paper_1",
        "title": "Neural Networks Improve Patient Outcomes: A Comprehensive Study",
        "abstract": "We used advanced neural networks to predict patient outcomes and achieved state-of-the-art accuracy.",
        "introduction": "Machine learning is increasingly applied in healthcare. We hypothesized that neural networks could predict outcomes better than existing methods.",
        "methods": "We applied a neural network to the data.",
        "results": "Our model achieved a 99% accuracy on the test set. We tested across 47 hypotheses and found significance at p<0.05. Sample size was n=3 patients total, lacking any control group.",
        "conclusions": "Neural networks represent a massive leap forward in medicine.",
        "ground_truth": {
            "novelty_score": 0.3,
            "methodology_score": 0.1,
            "statistical_validity_score": 0.1,
            "reproducibility_score": 0.1,
            "clarity_score": 0.4,
            "recommendation": "reject",
            "known_flaws": ["no_control_group", "tiny_sample", "p_hacking", "missing_methods"],
            "keyword_signals": {
                "novelty": ["application", "standard"],
                "methodology": ["control", "sample", "methods", "n=3", "group"],
                "statistical": ["p-value", "hypotheses", "multiple", "correction", "47"],
                "reproducibility": ["code", "data", "missing"],
                "clarity": ["brevity", "unclear"]
            }
        }
    },
    {
        "paper_id": "paper_2",
        "title": "Transformer Architectures for Climate Prediction: Promise and Limitations",
        "abstract": "We apply transformers to climate data to predict extreme weather events. The approach shows promise.",
        "introduction": "Predicting climate is hard. We introduce a novel application of transformer models, widely used in NLP, to climate data.",
        "methods": "We trained a transformer on historical temperature data using standard deep learning frameworks. We used a dataset comprising 2 years of data.",
        "results": "The model outperforms traditional statistical methods on our 2-year dataset. We did not perform an ablation study.",
        "conclusions": "This work revolutionizes climate science and solves long-term forecasting.",
        "ground_truth": {
            "novelty_score": 0.8,
            "methodology_score": 0.5,
            "statistical_validity_score": 0.6,
            "reproducibility_score": 0.7,
            "clarity_score": 0.9,
            "recommendation": "major_revision",
            "known_flaws": ["small_dataset", "no_ablation", "overclaimed_conclusions"],
            "keyword_signals": {
                "novelty": ["novel", "application", "transformer"],
                "methodology": ["ablation", "years", "small", "dataset"],
                "statistical": ["variance", "baseline"],
                "reproducibility": ["hyperparameters", "details"],
                "clarity": ["well-written", "clear", "overclaimed", "revolutionizes"]
            }
        }
    },
    {
        "paper_id": "paper_3",
        "title": "Mindfulness Intervention Reduces Corporate Burnout: A Randomized Controlled Trial",
        "abstract": "We conducted a rigorous RCT on mindfulness training in corporate settings, finding significant reductions in burnout.",
        "introduction": "Burnout is prevalent. Our study tests a new mindfulness intervention.",
        "methods": "Participants were randomized into intervention and control groups. Pre-registration is available, though the primary outcome was updated post-data collection.",
        "results": "The primary endpoint showed a significant reduction in burnout (p=0.049). Confidence intervals are [0.01, 2.3]. Baselines used for comparison were from 1995.",
        "conclusions": "Mindfulness definitively cures corporate burnout.",
        "ground_truth": {
            "novelty_score": 0.6,
            "methodology_score": 0.7,
            "statistical_validity_score": 0.2,
            "reproducibility_score": 0.8,
            "clarity_score": 0.8,
            "recommendation": "major_revision",
            "known_flaws": ["p_value_borderline", "cherry_picked_baselines", "harking", "ci_barely_excludes_null"],
            "keyword_signals": {
                "novelty": ["intervention", "setting"],
                "methodology": ["randomized", "control"],
                "statistical": ["p=0.049", "harking", "post-hoc", "cherry-picked", "baselines", "interval", "null"],
                "reproducibility": ["pre-registration", "data"],
                "clarity": ["clear", "polished"]
            }
        }
    },
    # 4 to 12
    {
        "paper_id": "paper_4",
        "title": "Quantum Computing the Economy: A Fast Algorithm",
        "abstract": "We simulate the entire stock market using a quantum computer with 10 qubits.",
        "introduction": "Economics needs quantum advantage.",
        "methods": "We used a 10 qubit simulator.",
        "results": "Simulated 1 stock. p<0.05 on 80 tests. n=1 stock. Methods section is short.",
        "conclusions": "We solved economics.",
        "ground_truth": {
            "novelty_score": 0.2,
            "methodology_score": 0.15,
            "statistical_validity_score": 0.12,
            "reproducibility_score": 0.1,
            "clarity_score": 0.3,
            "recommendation": "reject",
            "known_flaws": ["tiny_sample", "p_hacking", "missing_methods", "no_control_group"],
            "keyword_signals": {
                "novelty": ["quantum", "economics"],
                "methodology": ["sample", "methods", "control"],
                "statistical": ["p-value", "multiple", "tests"],
                "reproducibility": ["simulator"],
                "clarity": ["short"]
            }
        }
    },
    {
        "paper_id": "paper_5",
        "title": "Gene Editing in Agriculture: The Tomato Case",
        "abstract": "CRISPR used on tomatoes to increase yield.",
        "introduction": "Gene editing can solve hunger.",
        "methods": "CRISPR-Cas9 applied to exactly 10 plants.",
        "results": "Yield up by 5% but p=0.08. We did no ablation. Dataset was 1 month. Revolutionizes farming.",
        "conclusions": "This revolutionizes agriculture.",
        "ground_truth": {
            "novelty_score": 0.75,
            "methodology_score": 0.45,
            "statistical_validity_score": 0.55,
            "reproducibility_score": 0.65,
            "clarity_score": 0.85,
            "recommendation": "major_revision",
            "known_flaws": ["small_dataset", "no_ablation", "overclaimed_conclusions"],
            "keyword_signals": {
                "novelty": ["crispr", "tomato"],
                "methodology": ["ablation", "dataset", "small"],
                "statistical": ["p=0.08", "significant"],
                "reproducibility": ["protocol"],
                "clarity": ["overclaimed"]
            }
        }
    },
    {
        "paper_id": "paper_6",
        "title": "Universal Basic Income: A 10-Year Study",
        "abstract": "A robust 10-year study on UBI.",
        "introduction": "UBI is a hot topic.",
        "methods": "RCT across 5 cities.",
        "results": "Effect is p=0.048. Baselines were from older non-UBI studies. CI is [0.005, 1.5]. Outcome metric was changed in year 9.",
        "conclusions": "UBI works perfectly.",
        "ground_truth": {
            "novelty_score": 0.65,
            "methodology_score": 0.75,
            "statistical_validity_score": 0.25,
            "reproducibility_score": 0.75,
            "clarity_score": 0.75,
            "recommendation": "major_revision",
            "known_flaws": ["p_value_borderline", "cherry_picked_baselines", "harking", "ci_barely_excludes_null"],
            "keyword_signals": {
                "novelty": ["long-term", "ubi"],
                "methodology": ["rct", "cities"],
                "statistical": ["harking", "post-hoc", "cherry", "baselines", "p=0.048"],
                "reproducibility": ["data"],
                "clarity": ["polished"]
            }
        }
    },
    {
        "paper_id": "paper_7",
        "title": "Deep Learning for Deep Space",
        "abstract": "Finding aliens with ML.",
        "introduction": "Aliens might exist.",
        "methods": "We used an autoencoder.",
        "results": "n=2 galaxies. No control. p<0.05 on 100 metrics.",
        "conclusions": "We found aliens.",
        "ground_truth": {
            "novelty_score": 0.25,
            "methodology_score": 0.12,
            "statistical_validity_score": 0.15,
            "reproducibility_score": 0.15,
            "clarity_score": 0.35,
            "recommendation": "reject",
            "known_flaws": ["tiny_sample", "missing_methods", "no_control_group", "p_hacking"],
            "keyword_signals": {
                "novelty": ["space", "ml"],
                "methodology": ["galaxies", "control", "sample", "methods"],
                "statistical": ["p-value", "metrics"],
                "reproducibility": ["dataset"],
                "clarity": ["brief"]
            }
        }
    },
    {
        "paper_id": "paper_8",
        "title": "Microplastics in the Ocean: A New Filter",
        "abstract": "We made a filter for plastic.",
        "introduction": "Plastic is bad.",
        "methods": "We built a filter and tested it in a small tank for 1 week.",
        "results": "Filtered 90%. No ablation on filter layers. Small dataset. Revolutionizes ocean cleaning.",
        "conclusions": "Oceans are saved.",
        "ground_truth": {
            "novelty_score": 0.85,
            "methodology_score": 0.55,
            "statistical_validity_score": 0.65,
            "reproducibility_score": 0.75,
            "clarity_score": 0.88,
            "recommendation": "major_revision",
            "known_flaws": ["small_dataset", "no_ablation", "overclaimed_conclusions"],
            "keyword_signals": {
                "novelty": ["filter", "plastic"],
                "methodology": ["ablation", "dataset", "tank", "small"],
                "statistical": ["variance"],
                "reproducibility": ["design"],
                "clarity": ["overclaimed", "saved"]
            }
        }
    },
    {
        "paper_id": "paper_9",
        "title": "Social Media and Teen Anxiety",
        "abstract": "Link between apps and stress.",
        "introduction": "Phones cause stress.",
        "methods": "Survey of 1000 teens.",
        "results": "p=0.047. Used arbitrary old baseline. Survey metric changed halfway. CI [0.02, 3.1].",
        "conclusions": "Phones are universally bad.",
        "ground_truth": {
            "novelty_score": 0.55,
            "methodology_score": 0.65,
            "statistical_validity_score": 0.22,
            "reproducibility_score": 0.72,
            "clarity_score": 0.78,
            "recommendation": "major_revision",
            "known_flaws": ["p_value_borderline", "cherry_picked_baselines", "harking", "ci_barely_excludes_null"],
            "keyword_signals": {
                "novelty": ["survey", "teens"],
                "methodology": ["sample", "large"],
                "statistical": ["p=0.047", "harking", "changed", "cherry", "baseline"],
                "reproducibility": ["questions"],
                "clarity": ["clear"]
            }
        }
    },
    {
        "paper_id": "paper_10",
        "title": "Curing the Common Cold with Water",
        "abstract": "Drinking water cures colds.",
        "introduction": "Water is good.",
        "methods": "Drink water.",
        "results": "n=4 people. No control group. Tested 60 metrics, p<0.05 on one. Methods are 1 line.",
        "conclusions": "Water cures everything.",
        "ground_truth": {
            "novelty_score": 0.15,
            "methodology_score": 0.08,
            "statistical_validity_score": 0.09,
            "reproducibility_score": 0.2,
            "clarity_score": 0.25,
            "recommendation": "reject",
            "known_flaws": ["tiny_sample", "no_control_group", "missing_methods", "p_hacking"],
            "keyword_signals": {
                "novelty": ["water", "cold"],
                "methodology": ["control", "sample", "group", "methods", "n=4"],
                "statistical": ["p-value", "metrics", "multiple"],
                "reproducibility": ["setup"],
                "clarity": ["short"]
            }
        }
    },
    {
        "paper_id": "paper_11",
        "title": "LLMs for Legal Advice",
        "abstract": "Using LLMs for law.",
        "introduction": "Lawyers are expensive.",
        "methods": "Prompted an LLM.",
        "results": "Did ok. Small dataset of 5 cases. No ablation on prompt. Revolutionizes law.",
        "conclusions": "Lawyers are obsolete.",
        "ground_truth": {
            "novelty_score": 0.78,
            "methodology_score": 0.48,
            "statistical_validity_score": 0.58,
            "reproducibility_score": 0.68,
            "clarity_score": 0.82,
            "recommendation": "major_revision",
            "known_flaws": ["small_dataset", "no_ablation", "overclaimed_conclusions"],
            "keyword_signals": {
                "novelty": ["llm", "law"],
                "methodology": ["ablation", "cases", "small", "dataset"],
                "statistical": ["variance", "eval"],
                "reproducibility": ["prompt"],
                "clarity": ["overclaimed", "obsolete"]
            }
        }
    },
    {
        "paper_id": "paper_12",
        "title": "Dietary Fiber and Lifespan",
        "abstract": "Fiber makes you live longer.",
        "introduction": "Eat fiber.",
        "methods": "Dietary tracking.",
        "results": "p=0.046. Changed primary endpoint to 'healthspan'. Baselines from 1980. CI [0.03, 4.0].",
        "conclusions": "Fiber guarantees immortality.",
        "ground_truth": {
            "novelty_score": 0.58,
            "methodology_score": 0.68,
            "statistical_validity_score": 0.28,
            "reproducibility_score": 0.68,
            "clarity_score": 0.72,
            "recommendation": "major_revision",
            "known_flaws": ["p_value_borderline", "cherry_picked_baselines", "harking", "ci_barely_excludes_null"],
            "keyword_signals": {
                "novelty": ["fiber", "diet"],
                "methodology": ["tracking", "longitudinal"],
                "statistical": ["p=0.046", "harking", "endpoint", "cherry", "baseline"],
                "reproducibility": ["data"],
                "clarity": ["claim"]
            }
        }
    }
]

def get_paper_by_task(task_id: str, step_number: int = 0) -> Dict[str, Any]:
    # Route to appropriate paper pool based on task_id
    # task_easy -> 0, 3, 6, 9
    # task_medium -> 1, 4, 7, 10
    # task_hard -> 2, 5, 8, 11
    if task_id == "task_easy":
        indices = [0, 3, 6, 9]
    elif task_id == "task_medium":
        indices = [1, 4, 7, 10]
    elif task_id == "task_hard":
        indices = [2, 5, 8, 11]
    else:
        raise ValueError(f"Invalid task_id: {task_id}")
        
    idx = indices[step_number % len(indices)]
    return dict(PAPERS[idx])
