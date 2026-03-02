# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a monorepo containing three independent AI automation projects, all Python-based with no Node.js components:

- **macbook-controller/** — Telegram bot for remote MacBook control via Claude AI
- **python-job-agent/** — End-to-end job search pipeline (search → AI tailoring → PDF generation → Google Sheets)
- **openclaw/** — Modular multi-agent architecture for the same job functions using Git submodules
- **job-tracker-utility/** — Lightweight CLI for tracking job applications locally (no external dependencies)

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
This runs an end-to-end test with mock data (no real API calls, minimal AI credit usage).

## Architecture

### macbook-controller
Single-file app (`src/laptop_bot.py`). Flow: Telegram message → authorization check → Claude Haiku parses natural language into a JSON action list → sequential execution of system actions (screenshot, shell commands, file ops, app control, power management) → Telegram response.

### python-job-agent
Pipeline orchestrated by `src/main.py`, with each stage in its own module:

```
job_searcher.py          → Multi-board search (JSearch/Dice/Bayt/Adzuna via RapidAPI)
ai_processor.py          → Claude AI keyword extraction from job descriptions
resume_processor.py      → PDF parsing (pdfplumber), ATS scoring, tailored PDF generation (reportlab)
cover_letter_generator.py → Claude AI personalized cover letters
recruiter_finder.py      → Regex + AI recruiter contact extraction
sheets_handler.py        → Google Sheets read/write (gspread)
```

Configuration is centralized in `config/config.py` — all API keys, job roles, locations, user details, and sheet names live there.

Output artifacts go to `tailored_resumes/` and `cover_letters/` directories.

The same pipeline is accessible via three interfaces: CLI (`main.py`), web dashboard (`app.py` with Streamlit), and Telegram bot (`telegram_bot.py`).

### openclaw
Modular rewrite of python-job-agent as independent Git submodule agents (job-fetcher, resume-updater, keyword-analyzer, ats-scorer, cover-letter-generator, sheets-manager). The `main-orchestrator/` is a work-in-progress placeholder.

### job-tracker-utility
Single-file CLI app (`src/main.py`). Stores applications as JSON in `data/applications.json`. Supports add, list, update status, delete, search, and CSV export. No external dependencies — stdlib only.

## Key Configuration

All python-job-agent settings are in `config/config.py`:
- `JOB_ROLES` — list of job titles to search
- `LOCATIONS` — list of target locations
- `PAGES_PER_SEARCH` — pages per job board query (~10 jobs/page)
- `REQUEST_DELAY` — seconds between API calls (default 1.5s)
- `USER_NAME`, `USER_EMAIL`, `USER_PHONE`, `USER_LOCATION` — used in cover letter generation
- `GOOGLE_CREDENTIALS_FILE` — path to Google service account JSON

Google Sheets credential file (`credentials.json`) must be present in the working directory when running the job agent.

## Claude AI Usage

Both macbook-controller and python-job-agent use `claude-haiku-4-5-20251001` for cost-effective processing. The model is called for:
- Natural language → action JSON (macbook-controller)
- Keyword extraction from job descriptions
- ATS-optimized resume tailoring
- Personalized cover letter generation
- Recruiter contact extraction from unstructured text
