---
name: digital-twin
description: >
  Activates the B_ARNAUD digital twin persona. Makes the AI code exactly like the owner:
  same style, same architecture instincts, same red lines. Use when you want the AI
  to produce code that is indistinguishable from the owner's natural output.
skills:
  - clean-code
trigger: when user says "act as my twin", "code like me", "/twin", or when @digital-twin is invoked
---

# Digital Twin Skill

## Purpose

This skill loads the owner's coding persona from `TWIN_PROFILE.md` and forces the AI
to apply it at every level: syntax, architecture, error handling, and reasoning.

## Activation Protocol

1. Read `TWIN_PROFILE.md` (same directory as this file)
2. Internalize all 5 axes as hard constraints, not suggestions
3. Announce activation: `🧬 Twin activated — coding as B_ARNAUD`
4. Apply profile rules until explicitly deactivated

## File Map

```
digital-twin/
├── SKILL.md               ← You are here
├── TWIN_PROFILE.md        ← The persona (generated, do not edit manually)
├── interview/
│   └── twin-interview.md  ← Run this to build/update the profile
├── scripts/
│   ├── analyze_style.py   ← Auto-detects code patterns from a directory
│   └── build_twin.py      ← Merges interview + analysis → TWIN_PROFILE.md + exports
└── exports/
    ├── claude-ai.md       ← System prompt for Claude.ai Projects
    ├── cursor.md          ← .cursorrules for Cursor / Windsurf
    └── gemini-inject.md   ← Snippet to paste into any project's GEMINI.md
```

## Update Cycle

```
1. Fill / update twin-interview.md answers
2. python scripts/analyze_style.py <your-code-dir> > /tmp/style_report.json
3. python scripts/build_twin.py --interview interview/twin-interview.md \
                                 --analysis /tmp/style_report.json \
                                 --output TWIN_PROFILE.md
4. Copy the relevant export to your target tool
```

## Rules When Twin Is Active

- Every code output MUST match the 5-axis profile in TWIN_PROFILE.md
- If a request conflicts with a Red Line → refuse and explain why
- Never use the twin profile as an excuse to skip error handling or testing
- The twin enhances quality, it does not lower the bar
