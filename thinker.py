
from modules.providers import call_model

def thinker_run(topic: str, language: str = "en", depth: int = 2) -> dict:
    p1 = call_model(
        f"Engine-A (Gemini): Research '{topic}' in {language}. Give 3 bullet insights.",
        provider_hint="gemini"
    )
    p2 = call_model(
        f"Engine-B (Mock): Research '{topic}' in {language}. Give 3 bullet insights.",
        provider_hint=None
    )
    referee = call_model(
        "Referee: Compare Engine-A and Engine-B. "
        "List agreements/disagreements and give a 5-line action brief."
    )
    return {
        "topic": topic,
        "language": language,
        "engine_a": p1,
        "engine_b": p2,
        "referee_brief": referee,
    }
