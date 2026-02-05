---
name: claude-local-system
description: |
  Use claude-local for basic coding tasks that don't require design decisions
  or external research. Free unlimited usage via local Ollama (qwen3-coder-next).
  Perfect for: file modifications, test writing, documentation, mechanical refactoring.
  Explicit triggers: "implement this", "write tests", "add docs", clear specifications.
metadata:
  short-description: Claude Code ↔ Ollama collaboration (basic coding, free)
---

# Claude-Local System — Free Local Worker

**claude-local runs via Ollama for unlimited free coding work.**

> **Detailed rules**: `.claude/rules/claude-local-delegation.md`

## Quick Reference

### When to Use

| Task | claude-local | Why |
|------|-------------|-----|
| **Clear implementation** | ✓ | No design decisions needed |
| **Test writing** | ✓ | Follows existing patterns |
| **Documentation** | ✓ | Follows templates |
| **Mechanical refactor** | ✓ | Clear transformation rules |
| **Bug fix (obvious)** | ✓ | Clear fix needed |
| **Boilerplate code** | ✓ | Repetitive patterns |

### When NOT to Use

| Task | Alternative | Why |
|------|-------------|-----|
| Design decisions | Codex | Needs reasoning |
| Complex debugging | Codex | Needs analysis |
| Research | Gemini | Needs web access |
| Trade-off evaluation | Codex | Needs reasoning |
| Library comparison | Gemini | Needs current info |

## How to Use

### Subagent Pattern (Standard)

```
Task tool parameters:
- subagent_type: "claude-local"
- prompt: |
    Task: {specific task}
    Files: {file paths}
    Spec: {clear specification}
```

### Task Templates

#### Implementation Task

```
Task(
  subagent_type: "claude-local",
  prompt: """
    Implement {feature} in {file}.

    Requirements:
    1. {requirement 1}
    2. {requirement 2}

    Follow existing patterns in {reference file}.
    Add type hints and docstring.
  """
)
```

#### Test Writing Task

```
Task(
  subagent_type: "claude-local",
  prompt: """
    Write unit tests for {function/class} in {file}.

    Test cases:
    1. {happy path}
    2. {edge case 1}
    3. {error case}

    Follow pytest patterns from tests/conftest.py.
  """
)
```

#### Documentation Task

```
Task(
  subagent_type: "claude-local",
  prompt: """
    Add docstrings to all public functions in {file}.

    Format: Google style docstrings
    Include: Args, Returns, Raises, Examples
  """
)
```

#### Refactoring Task

```
Task(
  subagent_type: "claude-local",
  prompt: """
    Refactor {target} in {file}:

    Change: {specific change}
    Scope: {files affected}

    This is a mechanical change, no design decisions needed.
  """
)
```

## Available Tools

| Tool | Purpose | Available |
|------|---------|-----------|
| Read | Read project files | ✓ |
| Edit | Modify existing files | ✓ |
| Write | Create new files | ✓ |
| Bash | Run commands | ✓ |
| Grep | Search code | ✓ |
| Glob | Find files | ✓ |
| Fetch | Access provided URLs | ✓ |
| Context7 MCP | Official library docs | ✓ |
| WebSearch | Web search | ✗ |
| Codex CLI | Design reasoning | ✗ |
| Gemini CLI | Research | ✗ |

## Context7 for Documentation

claude-local can access official library documentation via Context7:

```
1. Resolve library ID:
   mcp__plugin_context7_context7__resolve-library-id
   - libraryName: "fastapi"
   - query: "how to create endpoints"

2. Query documentation:
   mcp__plugin_context7_context7__query-docs
   - libraryId: "/tiangolo/fastapi"
   - query: "request validation with Pydantic"
```

## Handling Blocks

If claude-local cannot complete a task, it reports:

```markdown
## Status: blocked
## Reason: {reason}
## Recommend: {Codex|Gemini|Clarification}
```

**Your response:**

| Block Reason | Action |
|--------------|--------|
| "Design decision needed" | Spawn Codex subagent |
| "Research needed" | Spawn Gemini subagent |
| "Clarification needed" | Ask user |
| "Web search unavailable" | Try Context7 or Gemini |

## Cost Comparison

| Agent | Cost | Best For |
|-------|------|----------|
| **claude-local** | Free | Basic coding, tests, docs |
| Codex | API cost | Design, debugging, trade-offs |
| Gemini | API cost | Research, multimodal |

## Workflow Integration

```
User request
    ↓
Analyze task complexity
    ↓
┌─────────────────────────────────────────┐
│ Simple, clear task?                     │
│ ├── YES → claude-local (FREE)           │
│ │         ├── Success → Done            │
│ │         └── Blocked → Escalate        │
│ └── NO → Codex/Gemini (API cost)        │
└─────────────────────────────────────────┘
```

## Example Workflow

**User:** 「UserServiceにvalidate_emailメソッドを追加して」

**Orchestrator analysis:**
- Task: Add method to existing class
- Spec: Clear (validate email format)
- Design decision: Not needed
- → Use claude-local

**Spawn subagent:**
```
Task(
  subagent_type: "claude-local",
  prompt: """
    Add validate_email method to UserService in src/services/user.py.

    Method signature:
    def validate_email(self, email: str) -> bool

    Logic: Use regex for email validation
    Return: True if valid, False otherwise
    Add type hints and docstring.
  """
)
```

**claude-local response:**
```markdown
## Task: Add validate_email to UserService
## Status: completed
## Changes Made:
- src/services/user.py: Added validate_email method with regex validation
## Notes: None
```

**Report to user (Japanese):**
「UserServiceにvalidate_emailメソッドを追加しました。正規表現によるメール形式検証を実装しています。」
