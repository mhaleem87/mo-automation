# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Owner & Communication Style

Mohammed Haleem (Mo) — Product Owner / Technical PM, 10+ years experience, currently at Sony Music Entertainment NYC. AI/ML product experience (content authenticity detection, automated QC).

- Direct and efficient. No unnecessary explanations or filler.
- Step-by-step when executing. Plan first, then build.
- Flag problems honestly — don't sugarcoat or over-promise.
- Prefer simple, working solutions over complex architectures.

## Current Priorities (March 2026)

1. Clean up & organize existing projects (audit Haiku-created files)
   - Audit Streamlit web UI (`python-job-agent/src/app.py`) — check purpose, clean up or remove after confirmation
2. Job search / OpenClaw automation
3. Polymarket trading system
4. Marketing agents / revenue generation
5. Crypto & stock trading setup
6. Website & dashboard building (single domain)
   - 6.1 Personal portfolio website
   - 6.2 Dashboard to track all agent status & activities
   - 6.3 Dashboard for job agent output
   - 6.4 Dashboard for Polymarket trading
7. Digital marketing agent
8. Freelancing automation agents
9. Social media activity planning

## Workflow

- **Claude Chat** → Planning, strategy, research, documents, reviews
- **Claude Code** → Building, coding, testing, debugging, file operations, git, system admin
- Pattern: Plan in Chat → Build in Code → Review in Chat

## Important Warnings

- Previous work was done with **Haiku 4.5** which produced unverified, potentially over-engineered output. All Haiku-created files (skills, docs, scripts) need audit before use or commit.
- Notion integration has been **fully removed** (March 8, 2026). Do not reference or recreate.
- Repo is **PUBLIC** on GitHub — never commit secrets, tokens, or API keys. Use env vars or `.env` (gitignored).
- `chat_auto_saver.py` LaunchAgent (`com.mohammedhaleem.chatautosaver`) is Haiku-built — verify before trusting.
- Don't push unverified Haiku work to the repo.
- **Repo structure needs audit** — local filesystem and GitHub project organization may be messy from Haiku 4.5. Verify structure and reorganize if needed before building further.

## Overview

Monorepo containing AI automation projects, all Python-based with no Node.js components:

- **openclaw/** — Modular multi-agent job search architecture using Git submodules
- **python-job-agent/** — End-to-end job search pipeline (search → AI tailoring → PDF generation → Google Sheets)
- **macbook-controller/** — Telegram bot for remote MacBook control via Claude AI
- **job-tracker-utility/** — Lightweight CLI for tracking job applications locally (no external dependencies)
- **skills/** — Empty (March 8, 2026). All 20 Haiku-created skills deleted as generic filler. Rebuild with Opus when needed.

## Key Paths

- Main repo: `~/Projects/mo-automation/`
- Skills: `~/Projects/mo-automation/skills/`
- Chat history: `~/Downloads/Claude Chat History/`
- Code history: `~/Downloads/Claude Code History/`

## Services & Daily Tools

Google Drive/Docs, Gmail, Telegram, GitHub

## Job Search Context

Targeting: Product Owner, Project Manager, Business Analyst, Scrum Master roles in NYC and Middle East (Dubai, Abu Dhabi, Riyadh, Gulf/MENA). Key differentiator: AI/ML product experience at Sony Music.

## Running Projects

### macbook-controller
```bash
cd macbook-controller
python3 src/laptop_bot.py
```
Requires: `anthropic`, `pytelegrambotapi`, `ffmpeg` (for camera), system tools (`screencapture`, `osascript`)

### python-job-agent

Full pipeline (CLI):
```bash
cd python-job-agent
python3 src/main.py
```

Streamlit web UI:
```bash
cd python-job-agent
streamlit run src/app.py
```

Telegram bot interface:
```bash
cd python-job-agent
python3 src/telegram_bot.py
```

### Tests
```bash
cd python-job-agent
python3 src/test_full.py
```
Runs end-to-end test with mock data (no real API calls, minimal AI credit usage).

## Architecture

### macbook-controller
Single-file app (`src/laptop_bot.py`). Flow: Telegram message → auth check → Claude Haiku parses natural language → JSON action list → sequential system actions → Telegram response.

### python-job-agent
Pipeline orchestrated by `src/main.py`:

```
job_searcher.py           → Multi-board search (JSearch/Dice/Bayt/Adzuna via RapidAPI)
ai_processor.py           → Claude AI keyword extraction from job descriptions
resume_processor.py       → PDF parsing (pdfplumber), ATS scoring, tailored PDF generation (reportlab)
cover_letter_generator.py → Claude AI personalized cover letters
recruiter_finder.py       → Regex + AI recruiter contact extraction
sheets_handler.py         → Google Sheets read/write (gspread)
```

Config centralized in `config/config.py` — API keys, job roles, locations, user details, sheet names.
Output: `tailored_resumes/` and `cover_letters/` directories.
Three interfaces: CLI (`main.py`), web dashboard (`app.py`), Telegram bot (`telegram_bot.py`).

### openclaw
Modular rewrite of python-job-agent as independent Git submodule agents (job-fetcher, resume-updater, keyword-analyzer, ats-scorer, cover-letter-generator, sheets-manager). `main-orchestrator/` is WIP.

### job-tracker-utility
Single-file CLI (`src/main.py`). JSON storage at `data/applications.json`. Supports add, list, update, delete, search, CSV export. Stdlib only.

## Key Configuration

All python-job-agent settings in `config/config.py`:
- `JOB_ROLES` — job titles to search
- `LOCATIONS` — target locations
- `PAGES_PER_SEARCH` — pages per query (~10 jobs/page)
- `REQUEST_DELAY` — seconds between API calls (default 1.5s)
- `USER_NAME`, `USER_EMAIL`, `USER_PHONE`, `USER_LOCATION` — cover letter fields
- `GOOGLE_CREDENTIALS_FILE` — path to Google service account JSON

Google Sheets credential file (`credentials.json`) must be present in working directory.

## Claude AI Usage

Both macbook-controller and python-job-agent use `claude-haiku-4-5-20251001` for cost-effective processing:
- Natural language → action JSON (macbook-controller)
- Keyword extraction from job descriptions
- ATS-optimized resume tailoring
- Personalized cover letter generation
- Recruiter contact extraction from unstructured text

## Rules

1. Never commit secrets or API keys. Use environment variables or `.env` files (gitignored).
2. Don't push unverified Haiku work — audit first.
3. Keep commits clean and descriptive.
4. Read existing code first, flag issues before modifying.
5. Conservative daily limits on automated job applications (anti-bot awareness).
6. When in doubt, ask — don't assume.
