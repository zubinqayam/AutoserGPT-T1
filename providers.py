
import os

def _has(var: str) -> bool:
    v = os.getenv(var, "").strip()
    return len(v) > 0 and "your-" not in v.lower()

def available_providers():
    gem_key = _has("GEMINI_API_KEY")
    gem_toggle = os.getenv("GEMINI_PROVIDER", "on").strip().lower() in ("on", "true", "1", "yes")
    return {
        "gemini": gem_key and gem_toggle,
        "openrouter": _has("OPENROUTER_API_KEY"),
        "anthropic": _has("ANTHROPIC_API_KEY"),
        "azure_openai": _has("AZURE_OPENAI_KEY") and _has("AZURE_OPENAI_ENDPOINT"),
    }

def _call_gemini(prompt: str) -> str:
    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"max_output_tokens": 512},
    )
    return getattr(resp, "text", str(resp))

def call_model(prompt: str, provider_hint: str | None = None) -> str:
    provs = available_providers()
    chosen = provider_hint if provider_hint in provs and provs[provider_hint] else None
    if not chosen:
        chosen = next((p for p, ok in provs.items() if ok), "mock")

    if chosen == "mock":
        return f"[MOCK:{provider_hint or 'auto'}] " + prompt[:160]

    if chosen == "gemini":
        try:
            return _call_gemini(prompt)
        except Exception as e:
            return f"[FALLBACK:gemini-error:{type(e).__name__}] " + prompt[:160]

    return f"[UNWIRED:{chosen}] " + prompt[:160]
