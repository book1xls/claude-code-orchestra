#!/usr/bin/env python3
"""
UserPromptSubmit hook: Route to appropriate agent based on user intent.

Analyzes user prompts and suggests the most appropriate agent:
- Codex for design/debug/reasoning
- Gemini for research/multimodal
- claude-local for basic implementation (free, via Ollama)
"""

import json
import sys

# Triggers for Codex (design, debugging, deep reasoning)
CODEX_TRIGGERS = {
    "ja": [
        "設計", "どう設計", "アーキテクチャ",
        "なぜ動かない", "エラー", "バグ", "デバッグ",
        "どちらがいい", "比較して", "トレードオフ",
        "実装方法", "どう実装",
        "リファクタリング", "リファクタ",
        "レビュー", "見て",
        "考えて", "分析して", "深く",
    ],
    "en": [
        "design", "architecture", "architect",
        "debug", "error", "bug", "not working", "fails",
        "compare", "trade-off", "tradeoff", "which is better",
        "how to implement", "implementation",
        "refactor", "simplify",
        "review", "check this",
        "think", "analyze", "deeply",
    ],
}

# Triggers for Gemini (research, multimodal, large context)
GEMINI_TRIGGERS = {
    "ja": [
        "調べて", "リサーチ", "調査",
        "PDF", "動画", "音声", "画像",
        "コードベース全体", "リポジトリ全体",
        "最新", "ドキュメント",
        "ライブラリ", "パッケージ",
    ],
    "en": [
        "research", "investigate", "look up", "find out",
        "pdf", "video", "audio", "image",
        "entire codebase", "whole repository",
        "latest", "documentation", "docs",
        "library", "package", "framework",
    ],
}

# Triggers for claude-local (basic coding, clear specs, free via Ollama)
CLAUDE_LOCAL_TRIGGERS = {
    "ja": [
        "実装して", "書いて", "作って",
        "テストを追加", "テストを書いて",
        "ドキュメント", "docstring",
        "この通りに", "指示通りに",
        "リネーム", "名前を変更",
    ],
    "en": [
        "implement this", "write this", "create this",
        "add tests", "write tests",
        "add documentation", "docstrings",
        "as specified", "as instructed",
        "rename", "change name",
    ],
}

# Indicators that task is too complex for claude-local
COMPLEXITY_INDICATORS = {
    "ja": [
        "どう", "なぜ", "どちら", "比較", "選択",
        "設計", "アーキテクチャ", "トレードオフ",
        "調べ", "リサーチ", "最適",
    ],
    "en": [
        "how should", "why", "which", "compare", "choose",
        "design", "architecture", "trade-off",
        "research", "investigate", "optimal", "best practice",
    ],
}


def _has_complexity_indicators(prompt: str) -> bool:
    """Check if prompt has indicators of complexity needing Codex/Gemini."""
    prompt_lower = prompt.lower()
    for triggers in COMPLEXITY_INDICATORS.values():
        for trigger in triggers:
            if trigger in prompt_lower:
                return True
    return False


def detect_agent(prompt: str) -> tuple[str | None, str]:
    """Detect which agent should handle this prompt.

    Priority order:
    1. Codex (complex/design tasks) - highest priority
    2. Gemini (research tasks) - medium priority
    3. claude-local (basic implementation) - lowest priority, but free
    """
    prompt_lower = prompt.lower()

    # Check Codex triggers first (highest priority for complex tasks)
    for triggers in CODEX_TRIGGERS.values():
        for trigger in triggers:
            if trigger in prompt_lower:
                return "codex", trigger

    # Check Gemini triggers (research has priority over basic implementation)
    for triggers in GEMINI_TRIGGERS.values():
        for trigger in triggers:
            if trigger in prompt_lower:
                return "gemini", trigger

    # Check claude-local triggers (basic implementation, free)
    # Only if no complexity indicators present
    if not _has_complexity_indicators(prompt_lower):
        for triggers in CLAUDE_LOCAL_TRIGGERS.values():
            for trigger in triggers:
                if trigger in prompt_lower:
                    return "claude-local", trigger

    return None, ""


def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        # Skip short prompts
        if len(prompt) < 10:
            sys.exit(0)

        agent, trigger = detect_agent(prompt)

        if agent == "codex":
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Agent Routing] Detected '{trigger}' - this task may benefit from "
                        "Codex CLI's deep reasoning capabilities. Consider: "
                        "`codex exec --model gpt-5.2-codex --sandbox read-only --full-auto "
                        '"{task description}"` for design decisions, debugging, or complex analysis.'
                    )
                }
            }
            print(json.dumps(output))

        elif agent == "gemini":
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Agent Routing] Detected '{trigger}' - this task may benefit from "
                        "Gemini CLI's research capabilities. Consider: "
                        '`gemini -p "Research: {topic}" 2>/dev/null` '
                        "for documentation, library research, or multimodal content."
                    )
                }
            }
            print(json.dumps(output))

        elif agent == "claude-local":
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Agent Routing] Detected '{trigger}' - this is a basic implementation task. "
                        "Consider using claude-local (FREE via Ollama) with: "
                        '`Task(subagent_type="claude-local", prompt="...")` '
                        "for straightforward coding, tests, or documentation."
                    )
                }
            }
            print(json.dumps(output))

        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
