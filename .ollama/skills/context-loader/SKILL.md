---
name: context-loader
description: Load project context from .claude/ directory. Ensures local Ollama agent aligns with project standards and coding rules.
---

# Context Loader for Ollama

## Purpose

Load shared project context from `.claude/` to align local agent with project standards before executing tasks.

## Workflow

### Step 1: Load Coding Rules

Read from `.claude/rules/`:

```
coding-principles.md → Simplicity, types, early return
dev-environment.md   → uv, ruff, pytest
testing.md           → AAA pattern, naming
security.md          → Input validation, secrets
```

### Step 2: Load Design Document

Read `.claude/docs/DESIGN.md` for:
- Existing patterns
- Library constraints
- Naming conventions
- Architecture decisions

### Step 3: Load Library Constraints

Check `.claude/docs/libraries/` for:
- Specific library usage rules
- Version constraints
- Known issues

### Step 4: Execute Task

With loaded context:
- Follow coding principles
- Match existing patterns
- Use project libraries correctly
- Respect constraints

## Key Rules Summary

### Coding Principles
- **Simplicity** - Readable over clever
- **Single Responsibility** - One function, one thing
- **Early Return** - Avoid deep nesting
- **Types** - All functions typed
- **Immutability** - Create new objects over mutation

### Development Environment
- **uv** - Package management (never pip)
- **ruff** - Linting and formatting
- **pytest** - Testing framework
- **poe** - Task runner

### Testing
- **AAA Pattern** - Arrange, Act, Assert
- **Naming** - `test_{target}_{condition}_{expected}`
- **Mocking** - Mock external dependencies
- **Coverage** - Target 80%+

## When to Load Context

Load context at the start of:
- Implementation tasks
- Test writing tasks
- Refactoring tasks

Skip for simple tasks like:
- Single file edits
- Documentation-only changes
- Formatting fixes

## Integration

This skill is automatically invoked by claude-local agent when context alignment is needed.

```
claude-local receives task
    ↓
Load context (this skill)
    ↓
Execute task with context
    ↓
Report completion
```
