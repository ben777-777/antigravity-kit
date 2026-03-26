"""
build_twin.py — Generates TWIN_PROFILE.md and portable AI exports from interview + code analysis.

WHY: The twin profile must be a single, authoritative source of truth derived from
two independent data sources to be reliable: self-reported (interview) + observed (code).
Discrepancies between the two are surfaced as warnings, not silently overridden.

Usage:
    python build_twin.py --interview twin-interview.md [--analysis report.json] --output TWIN_PROFILE.md
    python build_twin.py --test   (runs with mock data to verify output format)
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


EXPORTS_DIR = Path(__file__).parent.parent / "exports"
TWIN_PROFILE_DEFAULT = Path(__file__).parent.parent / "TWIN_PROFILE.md"
INTERVIEW_DEFAULT = Path(__file__).parent.parent / "interview" / "twin-interview.md"


# ---------------------------------------------------------------------------
# Interview parsing
# ---------------------------------------------------------------------------

def parse_interview(interview_path: Path) -> dict:
    """
    Extract answers from twin-interview.md.
    WHY: We parse code-fenced answer blocks and open-text responses separately
    to keep the structure flexible without requiring a rigid YAML format.
    """
    if not interview_path.exists():
        raise FileNotFoundError(f"Interview file not found: {interview_path}")

    content = interview_path.read_text(encoding="utf-8")
    answers = {}

    # Extract all question blocks: the text after each ### heading
    sections = re.split(r"^###\s+(.+)$", content, flags=re.MULTILINE)

    # sections = [pre_text, heading1, body1, heading2, body2, ...]
    for i in range(1, len(sections) - 1, 2):
        heading = sections[i].strip()
        body = sections[i + 1].strip() if i + 1 < len(sections) else ""

        # Extract code-block content (the actual answers)
        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", body, re.DOTALL)
        text_answer = "\n".join(code_blocks).strip() if code_blocks else body

        # Only store non-empty answers
        if text_answer and not all(c in " \n\t" for c in text_answer):
            answers[heading] = text_answer.strip()

    unanswered = sum(1 for v in answers.values() if not v or v.startswith("[") or not v.replace("\n", "").strip())
    return {
        "raw_answers": answers,
        "completion_pct": round((len(answers) - unanswered) / max(len(answers), 1) * 100),
        "unanswered_count": unanswered,
    }


# ---------------------------------------------------------------------------
# Profile synthesis
# ---------------------------------------------------------------------------

def synthesize_profile(interview_data: dict, analysis_data: dict | None) -> dict:
    """
    Merge interview answers and code analysis into a structured profile dict.
    WHY: Keeps the generation logic separate from the rendering logic.
    """
    answers = interview_data.get("raw_answers", {})

    def get(key: str, fallback: str = "_[not yet answered]_") -> str:
        return answers.get(key, fallback)

    profile = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "completion_pct": interview_data.get("completion_pct", 0),
        "style": {
            "naming": get("1.1 Nommage des variables"),
            "function_length": get("1.2 Longueur des fonctions"),
            "comments": get("1.3 Commentaires"),
            "abstraction": get("1.4 Abstraction"),
            "file_size": get("1.5 Longueur des fichiers"),
            "early_return": get("1.8 Early return"),
            "typing": get("1.10 Types et interfaces"),
        },
        "architecture": {
            "folder_structure": get("2.1 Organisation des dossiers"),
            "single_responsibility": get("2.2 Séparation des responsabilités"),
            "dependencies": get("2.3 Dépendances entre modules"),
            "state": get("2.4 État global"),
            "new_dep_rule": get("2.6 New dependency vs custom code"),
        },
        "error_handling": {
            "philosophy": get("3.1 Philosophie d'erreur"),
            "try_catch": get("3.2 try/catch : quand"),
            "error_messages": get("3.3 Messages d'erreur"),
            "logging": get("3.4 Logging"),
            "validation": get("3.5 Validation des inputs"),
        },
        "process": {
            "attack_new_problem": get("4.1 Quand tu attaques un nouveau problème"),
            "refactoring": get("4.3 Refactoring"),
            "code_review_focus": get("4.4 Code review"),
            "done_criteria": get("4.10 Décision d'arrêt"),
        },
        "red_lines": {
            "forbidden_patterns": get("5.1 Ce que tu refuses catégoriquement d'écrire"),
            "forbidden_approaches": get("5.2 Ce que tu refuses d'utiliser comme solution"),
            "triggers_rewrite": get("5.3 Ce qui te fait rewriter du code existant"),
            "security_line": get("5.4 Sécurité"),
            "minimum_always": get("5.5 Ce que tu ferais toujours, même si le deadline est demain"),
        },
        "signature_code": get("B4 — Écris toi-même une fonction « témoin »"),
        "code_analysis": analysis_data,
    }

    # Detect discrepancies between interview and analysis
    warnings = []
    if analysis_data:
        interview_style = profile["style"]["naming"].lower()
        observed_style = analysis_data.get("naming", {}).get("dominant_style", "")

        if observed_style and observed_style.lower() not in interview_style:
            warnings.append(
                f"Naming style discrepancy: you prefer '{interview_style[:30]}...' "
                f"but code analysis found '{observed_style}' dominant."
            )

        avg_fn_length = analysis_data.get("functions", {}).get("avg_length_lines", 0)
        if avg_fn_length > 40:
            warnings.append(
                f"Function length: analysis found avg {avg_fn_length} lines. "
                f"This suggests longer functions than typical. Review your interview answer."
            )

    profile["warnings"] = warnings
    return profile


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_twin_profile(profile: dict) -> str:
    """Render the structured profile dict into TWIN_PROFILE.md format."""
    s = profile["style"]
    a = profile["architecture"]
    e = profile["error_handling"]
    p = profile["process"]
    r = profile["red_lines"]
    ca = profile.get("code_analysis")
    warnings = profile.get("warnings", [])

    analysis_block = ""
    if ca:
        meta = ca.get("meta", {})
        naming = ca.get("naming", {})
        functions = ca.get("functions", {})
        patterns = ca.get("patterns", {})
        density = ca.get("code_density", {})

        analysis_block = f"""
## 6. Signature Patterns (Auto-Detected from Code)

> *Extracted by `analyze_style.py` — reflects actual behavior, not stated preferences.*

| Metric | Value |
|--------|-------|
| Files analyzed | {meta.get("analyzed_files", "n/a")} |
| Dominant naming | `{naming.get("dominant_style", "n/a")}` |
| Avg function length | {functions.get("avg_length_lines", "n/a")} lines |
| Short functions (≤15 lines) | {patterns.get("early_return_usage_pct", "n/a")}% use early return |
| Type hints usage | {patterns.get("type_hints_usage_pct", "n/a")}% of files |
| Comment ratio | {density.get("comment_ratio_pct", "n/a")}% of lines |
"""

    warning_block = ""
    if warnings:
        warning_block = "\n## ⚠️ Discrepancies Detected\n\n"
        for w in warnings:
            warning_block += f"- {w}\n"

    sig_code = r.get("minimum_always", "_not provided_")
    sig_fn = profile.get("signature_code", "_not provided_")

    return f"""# Twin Profile: B_ARNAUD
*Generated: {profile["generated_at"]} — Interview completion: {profile["completion_pct"]}%*

> This profile is the source of truth for the digital twin persona.
> Apply ALL sections as hard constraints, not suggestions.
> Update by re-running `build_twin.py` after modifying `twin-interview.md`.

---

## 1. Code Style DNA

### Naming
{s["naming"]}

### Function Length
{s["function_length"]}

### Comments
{s["comments"]}

### Abstraction Level
{s["abstraction"]}

### Early Return / Guard Clauses
{s["early_return"]}

### Typing
{s["typing"]}

---

## 2. Architecture Mindset

### Folder Structure
{a["folder_structure"]}

### Single Responsibility
{a["single_responsibility"]}

### Dependency Management
{a["dependencies"]}

### Global State
{a["state"]}

### New Dependency Rule
{a["new_dep_rule"]}

---

## 3. Error Philosophy

### General Stance
{e["philosophy"]}

### try/catch Usage
{e["try_catch"]}

### Error Messages
{e["error_messages"]}

### Logging
{e["logging"]}

### Input Validation
{e["validation"]}

---

## 4. Problem-Solving Process

### New Problem Attack
{p["attack_new_problem"]}

### Refactoring Trigger
{p["refactoring"]}

### Code Review Focus
{p["code_review_focus"]}

### Definition of Done
{p["done_criteria"]}

---

## 5. Red Lines (Non-Negotiables)

### Forbidden Patterns
{r["forbidden_patterns"]}

### Forbidden Approaches
{r["forbidden_approaches"]}

### Triggers Immediate Rewrite
{r["triggers_rewrite"]}

### Security Non-Negotiable
{r["security_line"]}

### Minimum Always (even under deadline)
{r["minimum_always"]}
{analysis_block}{warning_block}
---

## Signature Function (Témoin)

```
{sig_fn}
```

---
*End of Twin Profile. Do not edit manually — regenerate with `build_twin.py`.*
"""


def render_claude_ai_export(profile: dict) -> str:
    """Compact system prompt for Claude.ai Projects (≤ 1800 tokens)."""
    r = profile["red_lines"]
    s = profile["style"]
    e = profile["error_handling"]
    p = profile["process"]

    return f"""You are coding as B_ARNAUD's digital twin. Apply these constraints exactly.

## Code Style
- Naming: {s["naming"][:200]}
- Function length: {s["function_length"][:150]}
- Comments: {s["comments"][:150]}
- Early return: {s["early_return"][:150]}
- Typing: {s["typing"][:150]}

## Error Handling
- Philosophy: {e["philosophy"][:200]}
- try/catch: {e["try_catch"][:200]}
- Validation: {e["validation"][:150]}

## Process
- New problem: {p["attack_new_problem"][:300]}
- Done when: {p["done_criteria"][:200]}

## HARD RED LINES (never break these)
{r["forbidden_patterns"][:400]}

## Forbidden approaches
{r["forbidden_approaches"][:300]}

## Security
{r["security_line"][:200]}

## Minimum always (even under deadline)
{r["minimum_always"][:200]}

Apply ALL rules silently. Do not explain the twin unless asked.
"""


def render_cursor_export(profile: dict) -> str:
    """Cursor/Windsurf .cursorrules format."""
    return f"""# .cursorrules — B_ARNAUD Twin Profile
# Generated: {profile["generated_at"]}
# Source: TWIN_PROFILE.md

{render_claude_ai_export(profile)}
"""


def render_gemini_inject(profile: dict) -> str:
    """Snippet to inject into any project's GEMINI.md."""
    return f"""## 🧬 Digital Twin: B_ARNAUD (inject into GEMINI.md)

When @digital-twin is invoked or user says "code like me":
1. Load `TWIN_PROFILE.md` from `.agent/skills/digital-twin/`
2. Apply ALL 5 axes as hard constraints
3. Announce: `🧬 Twin activated — coding as B_ARNAUD`

Key constraints summary:
- **Style**: {profile["style"]["naming"][:100]}
- **Functions**: {profile["style"]["function_length"][:80]}
- **Errors**: {profile["error_handling"]["philosophy"][:100]}
- **Red lines**: See TWIN_PROFILE.md §5

*Profile generated: {profile["generated_at"]}*
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate digital twin profile from interview + code analysis")
    parser.add_argument("--interview", "-i", default=str(INTERVIEW_DEFAULT), help="Path to twin-interview.md")
    parser.add_argument("--analysis", "-a", default=None, help="Path to analyze_style.py output JSON")
    parser.add_argument("--output", "-o", default=str(TWIN_PROFILE_DEFAULT), help="Output path for TWIN_PROFILE.md")
    parser.add_argument("--test", action="store_true", help="Run with mock data to verify output format")
    args = parser.parse_args()

    if args.test:
        print("Running in test mode with mock data...", file=sys.stderr)
        interview_data = {
            "raw_answers": {
                "1.1 Nommage des variables": "snake_case for everything in Python. camelCase for JS/TS variables.",
                "1.2 Longueur des fonctions": "Max 25 lines. If I need to scroll, it's too long.",
                "3.1 Philosophie d'erreur": "C) depends on the layer — fail fast at boundaries, defensive inside.",
                "5.1 Ce que tu refuses catégoriquement d'écrire": "1. bare except:\n2. any()\n3. global state mutation",
                "5.5 Ce que tu ferais toujours, même si le deadline est demain": "Error handling + at least one test.",
                "B4 — Écris toi-même une fonction « témoin »": "def validate_user_input(raw: str) -> str:\n    ...",
            },
            "completion_pct": 42,
            "unanswered_count": 30,
        }
        analysis_data = None
    else:
        try:
            interview_data = parse_interview(Path(args.interview))
            print(f"Interview loaded: {interview_data['completion_pct']}% complete", file=sys.stderr)
        except FileNotFoundError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)

        analysis_data = None
        if args.analysis:
            try:
                analysis_data = json.loads(Path(args.analysis).read_text(encoding="utf-8"))
                print("Code analysis loaded.", file=sys.stderr)
            except (OSError, json.JSONDecodeError) as exc:
                print(f"WARNING: Could not load analysis file: {exc}", file=sys.stderr)

    profile = synthesize_profile(interview_data, analysis_data)

    # Write main profile
    out_path = Path(args.output)
    out_path.write_text(render_twin_profile(profile), encoding="utf-8")
    print(f"✅ TWIN_PROFILE.md written to {out_path}", file=sys.stderr)

    # Write exports
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (EXPORTS_DIR / "claude-ai.md").write_text(render_claude_ai_export(profile), encoding="utf-8")
    (EXPORTS_DIR / "cursor.md").write_text(render_cursor_export(profile), encoding="utf-8")
    (EXPORTS_DIR / "gemini-inject.md").write_text(render_gemini_inject(profile), encoding="utf-8")
    print(f"✅ Exports written to {EXPORTS_DIR}/", file=sys.stderr)

    if profile["warnings"]:
        print("\n⚠️  Warnings:", file=sys.stderr)
        for w in profile["warnings"]:
            print(f"   - {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
