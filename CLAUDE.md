# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

Antigravity Kit is a **meta-framework** — a modular template system of AI agent personas, domain skills, and workflows designed to augment coding assistants (Claude, Gemini, Cursor). The primary deliverable is the `.agent/` directory, not a runnable application. The `web/` folder is a separate Next.js documentation site.

## Repository Structure

```
.agent/                  # THE PRODUCT — agent templates, skills, workflows
  agents/                # 20 specialist agent personas (.md files)
  skills/                # 36+ domain skill modules (each a directory with SKILL.md)
  workflows/             # 11 slash command procedures (.md files)
  rules/                 # Global governance rules (GEMINI.md = P0 priority)
  scripts/               # Python validation scripts (checklist.py, verify_all.py)
web/                     # Next.js 16 documentation site (independent package)
AGENT_FLOW.md            # Full architecture & flow documentation
```

## Architecture: How the Agent System Works

1. **Request Classification** — User input is categorized by intent and domain
2. **Agent Routing** — Best specialist agent selected (e.g. `frontend-specialist`, `database-architect`)
3. **Skill Loading** — Agent loads required skills from `.agent/skills/` via progressive disclosure (SKILL.md → references/ → scripts/)
4. **Rule Priority** — `rules/GEMINI.md` (P0) > Agent `.md` (P1) > `SKILL.md` (P2)

Each skill follows a consistent structure:
```
skill-name/
├── SKILL.md           # Required: metadata + instructions
├── references/        # Optional: templates, checklists
├── scripts/           # Optional: Python/Bash helpers
```

## Commands

### Web Documentation Site (web/)

```bash
cd web && npm install        # Install dependencies
cd web && npm run dev        # Dev server at localhost:3000
cd web && npm run build      # Production build
cd web && npm run lint       # ESLint
```

### Validation Scripts (from repo root)

```bash
python .agent/scripts/checklist.py .                              # Quick: security, lint, types, tests, UX, SEO
python .agent/scripts/verify_all.py . --url http://localhost:3000 # Full: above + Lighthouse, E2E, bundle, mobile, i18n
```

### Docker (documentation site)

```bash
docker build -f web/Dockerfile -t antigravity-kit:latest .
docker run -p 3000:3000 antigravity-kit:latest
```

### Deployment

Automated via GitHub Actions on push to `main`: builds Docker image → pushes to ghcr.io → deploys to CapRover.

## Key Conventions

- **Agent files are Markdown** — All agents, skills, and workflows are `.md` files, not code. Edits should preserve their internal structure (frontmatter, sections, skill references).
- **Skills are self-contained modules** — Each skill directory must have a `SKILL.md`. References and scripts are optional. Skills link to related skills for progressive disclosure.
- **Scripts are NOT auto-executed** — Validation scripts in skills are suggested by the AI, approved and run by the user.
- **Web app uses Next.js App Router** — `web/src/app/` with MDX content pages, Tailwind CSS v4, TypeScript 5, React 19.
- **No build system at root** — Root `package.json` is metadata-only. All npm scripts live in `web/package.json`.

## When Editing Agent Content

- Read the target `.md` file before modifying — agents reference specific skills by name in their frontmatter
- When adding a new skill, create the directory under `.agent/skills/` with at minimum a `SKILL.md`
- When adding a new agent, update `.agent/ARCHITECTURE.md` to keep the catalog current
- Workflow `.md` files in `.agent/workflows/` correspond to slash commands — filenames must match the command name
