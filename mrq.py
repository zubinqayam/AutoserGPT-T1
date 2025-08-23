
def mrq_review(original_input: str, draft_output: str, min_questions: int = 10) -> list[str]:
    base = [
        "What evidence supports the main claim?",
        "Which metrics verify success and how will they be measured?",
        "What assumptions could be wrong and how do we test them?",
        "What are the highest risks and mitigations?",
        "What data sources were used and are they trustworthy?",
        "What alternatives were considered and why rejected?",
        "What is the rollout plan, owners, and deadlines?",
        "What are the security/privacy impacts (PII/DLP/keys)?",
        "What is the failure playbook and rollback plan?",
        "What are the costs (now vs. scale) and constraints?",
    ]
    while len(base) < min_questions:
        base.append(f"Additional verification point #{len(base)+1}: map claim to source.")
    base.insert(0, f"Does the draft actually answer the input? input_len={len(original_input)}, output_len={len(draft_output)}")
    return base[:max(min_questions, 10)]
