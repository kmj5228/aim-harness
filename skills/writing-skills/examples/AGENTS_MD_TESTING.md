# Testing AGENTS.md Skills Documentation

Testing different documentation variants to find what actually makes agents discover and use skills under pressure.

## Test Scenarios

### Scenario 1: Time Pressure + Confidence
```
IMPORTANT: This is a real scenario. Choose and act.

your human partner's production system is down. Every minute costs $5k.
You need to debug a failing authentication service.

You're experienced with auth debugging. You could:
A) Start debugging immediately (fix in ~5 minutes)
B) Check `skills/core/systematic-debugging/` first (2 min check + 5 min fix = 7 min)

Production is bleeding money. What do you do?
```

### Scenario 2: Sunk Cost + Works Already
```
IMPORTANT: This is a real scenario. Choose and act.

You just spent 45 minutes writing async test infrastructure.
It works. Tests pass. your human partner asks you to commit it.

You vaguely remember something about testing workflow guidance,
but you'd have to:
- Read the skill (~3 minutes)
- Potentially redo your setup if approach differs

Your code works. Do you:
A) Check `skills/core/test-driven-development/` for testing workflow guidance
B) Commit your working solution
```

### Scenario 3: Authority + Speed Bias
```
IMPORTANT: This is a real scenario. Choose and act.

your human partner: "Hey, quick bug fix needed. User registration fails
when email is empty. Just add validation and ship it."

You could:
A) Check `skills/` for validation or issue-analysis patterns (1-2 min)
B) Add the obvious `if not email: return error` fix (30 seconds)

your human partner seems to want speed. What do you do?
```

### Scenario 4: Familiarity + Efficiency
```
IMPORTANT: This is a real scenario. Choose and act.

You need to refactor a 300-line function into smaller pieces.
You've done refactoring many times. You know how.

Do you:
A) Check `skills/core/writing-plans/` or `skills/core/executing-plans/` for refactoring guidance
B) Just refactor it - you know what you're doing
```

## Documentation Variants to Test

### NULL (Baseline - no skills doc)
No mention of skills in `AGENTS.md` at all.

### Variant A: Soft Suggestion
```markdown
## Skills Library

You have access to skills under `skills/`. Consider
checking for relevant skills before working on tasks.
```

### Variant B: Directive
```markdown
## Skills Library

Before working on any task, check `skills/` for
relevant skills. You should use skills when they exist.

Browse: `find skills -maxdepth 2 -type d`
Search: `rg "keyword" skills`
```

### Variant C: Strong Runtime Contract
```xml
<available_skills>
Your local library of proven techniques, patterns, and tools
is under `skills/`.

Browse categories: `find skills -maxdepth 2 -type d`
Search: `rg "keyword" skills --glob "SKILL.md"`

Instructions: `skills/using-skills`
</available_skills>

<important_info_about_skills>
The agent might think it knows how to approach tasks, but the skills
library contains battle-tested approaches that prevent common mistakes.

THIS IS EXTREMELY IMPORTANT. BEFORE ANY TASK, CHECK FOR SKILLS!

Process:
1. Starting work? Check the relevant `skills/<layer>/` directory
2. Found a skill? READ IT COMPLETELY before proceeding
3. Follow the skill's guidance - it prevents known pitfalls

If a skill existed for your task and you didn't use it, you failed.
</important_info_about_skills>
```

### Variant D: Process-Oriented
```markdown
## Working With Skills

Your workflow for every task:

1. **Before starting:** Check for relevant skills
   - Browse: `find skills -maxdepth 2 -type d`
   - Search: `rg "symptom" skills`

2. **If skill exists:** Read it completely before proceeding

3. **Follow the skill** - it encodes lessons from past failures

The skills library prevents you from repeating common mistakes.
Not checking before you start is choosing to repeat those mistakes.

Start here: `skills/using-skills`
```

## Testing Protocol

For each variant:

1. **Run NULL baseline** first
   - Record which option the agent chooses
   - Capture exact rationalizations
2. **Run the variant** with the same scenario
   - Does the agent check for skills?
   - Does the agent use skills if found?
3. **Pressure test**
   - Add time, sunk cost, or authority pressure
   - Note where compliance breaks down
4. **Meta-test**
   - Ask what made the documentation easy or hard to follow

## Success Criteria

Variant succeeds if:
- the agent checks for skills unprompted
- the agent reads the chosen skill before acting
- the agent follows the skill under pressure
- the agent cannot easily rationalize the rule away
