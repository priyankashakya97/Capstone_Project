import re

from disclosure_snippets import DISCLOSURE_SNIPPETS


def extract_signals(snippet: str, mock_llm: int = 1) -> dict:
    """Extracts structured disclosure signals from text.

    Returns:
        {
            "risk_flags": [...],
            "hedging_detected": bool,
            "sentiment": "confident" | "cautious" | "neutral"
        }
    """
    if mock_llm == 1:
        return _extract_signals_mock(snippet)
    else:
        return _extract_signals_llm(snippet)


def _extract_signals_mock(snippet: str) -> dict:
    """Mock mode implementation using rule-based/regex extraction."""
    snippet_lower = snippet.lower()

    # 1. Identify risk flags
    risk_keywords = ["litigation", "regulatory", "customer concentration"]
    risk_flags = []

    for kw in risk_keywords:
        if kw in snippet_lower:
            risk_flags.append(kw)

    # 2. Detect hedging phrases
    hedging_keywords = ["assuming", "cautiously", "visibility"]
    hedging_detected = any(h_kw in snippet_lower for h_kw in hedging_keywords)

    # 3. Classify sentiment
    confident_keywords = ["confident", "approved"]

    if any(c_kw in snippet_lower for c_kw in confident_keywords):
        sentiment = "confident"
    elif hedging_detected:
        sentiment = "cautious"
    else:
        sentiment = "neutral"

    return {
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment,
    }


def _extract_signals_llm(snippet: str) -> dict:
    """Optional MOCK_LLM=0 extension: Prompts an LLM and validates JSON schema.

    Retries once on validation failure before falling back to mock mode.
    """

    # For this exercise, we will just call the mock implementation as a placeholder
    # If MOCK_LLM=0 were truly implemented, this would involve an actual LLM call
    # and JSON schema validation logic as described in the problem statement.
    return _extract_signals_mock(snippet)


# Test Runner for extract_signals
if __name__ == "__main__":
    print("=== Structured Disclosure Extraction ===")
    for idx, snippet in enumerate(DISCLOSURE_SNIPPETS, 1):
        result = extract_signals(snippet, mock_llm=1)
        print(f"Snippet {idx}:")
        print(f'  Text:   "{snippet}"')
        print(f"  Output: {result}\n")
