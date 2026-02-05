# Claude-Local Delegation Rule

**claude-local is your free local worker for basic coding tasks.**

## Context Management (CRITICAL)

claude-local runs locally via Ollama = **unlimited usage, no API cost**.

| Situation | Method | Cost |
|-----------|--------|------|
| Basic implementation (clear spec) | claude-local | Free |
| Test writing | claude-local | Free |
| Documentation | claude-local | Free |
| Design decision needed | Codex (via subagent) | API |
| Research needed | Gemini (via subagent) | API |
| Complex debugging | Codex (via subagent) | API |

```
┌──────────────────────────────────────────────────────────────┐
│  Main Claude Code (Orchestrator)                             │
│  → Clear, simple tasks → claude-local (free)                 │
│  → Complex/design tasks → general-purpose → Codex/Gemini     │
└──────────────────────────────────────────────────────────────┘
```

## About claude-local

claude-local uses Ollama with `qwen3-coder-next` model locally.

**Strengths:**
- Free unlimited usage
- No API costs
- Local execution (privacy)
- Continuous coding work

**Limitations:**
- No web search capability
- No design reasoning (follows instructions only)
- No research capability
- Context7 MCP only for documentation

## When to Use claude-local

**Use for straightforward tasks where instructions are clear:**

1. **File modifications** - Add/edit/delete with clear specs
2. **Code generation** - Create files from templates/specs
3. **Refactoring** - Mechanical changes (rename, extract, inline)
4. **Test writing** - Unit tests for existing code
5. **Documentation** - Docstrings, comments, README updates
6. **Formatting** - Code style fixes, linting issues
7. **Boilerplate** - Repetitive code patterns

### Trigger Phrases (User Input)

Consult claude-local when user says:

| Japanese | English |
|----------|---------|
| 「これを実装して」(with clear spec) | "Implement this" (with clear spec) |
| 「テストを書いて」「テストを追加」 | "Write tests" "Add tests" |
| 「ドキュメントを追加」「docstring」 | "Add documentation" "docstrings" |
| 「リファクタして」(mechanical) | "Refactor" (mechanical) |
| 「この通りに作って」「指示通りに」 | "Build as specified" |
| 「〜を〜にリネーム」 | "Rename X to Y" |

## When NOT to Use claude-local

**Escalate to Codex/Gemini when:**

| Situation | Why | Use Instead |
|-----------|-----|-------------|
| "How should I..." | Design decision | Codex |
| "Which is better..." | Trade-off analysis | Codex |
| "Why isn't this working..." | Deep debugging | Codex |
| "Research X" | No web access | Gemini |
| "Latest docs for X" | No web search | Gemini |
| "Compare libraries" | Research needed | Gemini |
| "Analyze this PDF/video" | No multimodal | Gemini |

## Quick Decision Tree

```
Is the task clear and specific?
├── NO → Don't use claude-local
│         (Clarify with user or use Codex)
│
└── YES → Does it require design choices?
          ├── YES → Don't use claude-local
          │         (Use Codex for design)
          │
          └── NO → Does it require external research?
                    ├── YES → Don't use claude-local
                    │         (Use Gemini for research)
                    │
                    └── NO → ✓ Use claude-local (FREE)
```

## How to Call claude-local

### Via Task Tool (Recommended)

```
Task tool parameters:
- subagent_type: "claude-local"
- prompt: |
    Implement the following:
    {clear, specific instructions}

    Files to modify:
    {file paths}

    Expected output:
    {what the code should do}
```

### Example: Implementation Task

```
Task(
  subagent_type: "claude-local",
  prompt: """
    Create a utility function in src/utils/date.py:

    Function: format_iso_date
    Input: datetime object
    Output: ISO 8601 formatted string

    Add type hints and Google-style docstring.
  """
)
```

### Example: Test Writing Task

```
Task(
  subagent_type: "claude-local",
  prompt: """
    Write unit tests for src/utils/date.py:format_iso_date

    Test cases:
    1. Normal datetime input
    2. Datetime with timezone
    3. Edge case: year 2000

    Follow existing test patterns in tests/
  """
)
```

### Example: Documentation Task

```
Task(
  subagent_type: "claude-local",
  prompt: """
    Add Google-style docstrings to all public functions in:
    src/services/user.py

    Include: Args, Returns, Raises, Example
  """
)
```

## claude-local vs Other Agents

| Criteria | claude-local | Codex | Gemini |
|----------|-------------|-------|--------|
| **Cost** | Free | API | API |
| **Task clarity** | Must be clear | Can be ambiguous | Exploratory OK |
| **Design decisions** | No | Yes (primary) | No |
| **Research** | No | Limited | Yes (primary) |
| **Web access** | No | Limited | Yes |
| **Documentation** | Context7 only | Project context | Web + project |
| **Continuous work** | Ideal | API limits | API limits |

## Handling Escalation

If claude-local reports a block, route to appropriate agent:

| claude-local reports | Route to |
|---------------------|----------|
| "Design decision needed" | Codex |
| "Research needed" | Gemini |
| "Clarification needed" | User |
| "Web search unavailable" | Gemini |

## Cost Optimization Strategy

```
1. First, try claude-local (free)
   ↓ (if blocked)
2. Check if Context7 can help (free)
   ↓ (if still blocked)
3. Use Codex/Gemini only when necessary (API cost)
```

**Use claude-local first for eligible tasks. Save API budget for complex work.**

## Language Protocol

1. Give instructions to claude-local in **English**
2. claude-local returns structured response
3. Main orchestrator reports to user in **Japanese**
