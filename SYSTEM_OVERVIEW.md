# Mo-Automation — System Overview

**Version:** 1.0
**Last Updated:** March 14, 2026
**Author:** Mo (Mohammed Haleem) + Claude Opus 4.6
**Status:** Post-cleanup, actively building

---

## What This Is

This is the master overview of Mo's automation ecosystem. Everything in this document reflects **what actually exists and works** — not aspirations or plans.

---

## Repository Structure

```
~/Projects/mo-automation/
├── CLAUDE.md                          # Claude Code persistent context
├── README.md                          # Repo README
├── .gitignore
├── .gitmodules                        # Legacy submodule refs (pending cleanup)
│
├── Opus/                              # All new work built with Claude Opus 4.6
│   └── openclaw-jobbot/               # Job search automation pipeline (ACTIVE)
│       ├── main.py                    # CLI entry point with subcommands
│       ├── bot.py                     # Telegram bot (natural language)
│       ├── config.yaml                # All settings (roles, locations, thresholds)
│       ├── .env                       # Secrets (gitignored)
│       ├── credentials.json           # Google Sheets auth (gitignored)
│       ├── requirements.txt
│       ├── CLAUDE.md                  # Claude Code context for this project
│       ├── OPENCLAW_JOBBOT_SPEC.md    # Full technical specification
│       ├── shared/                    # Shared foundation
│       ├── system1_discovery/         # Job search + keywords + relevance
│       ├── system2_tailoring/         # Resume + cover letter + recruiter
│       ├── system3_tracking/          # Sheets + files + Telegram
│       ├── output/                    # Generated PDFs (gitignored)
│       └── reference_code/            # Old Haiku code for reference (gitignored)
│
├── skills/                            # Empty — all Haiku skills deleted March 8, 2026
│
├── python-job-agent_Old_Can_Be_Deleted/    # Haiku monolithic job agent (REPLACED)
├── openclaw_Old_Can_Be_Deleted/            # Haiku empty scaffolding (REPLACED)
├── macbook-controller_Old_Can_Be_Deleted/  # Telegram Mac controller (TO REBUILD)
└── job-tracker-utility_Old_Can_Be_Deleted/ # CLI job tracker (TO REBUILD)
```

---

## Process Diagrams

### Existing: OpenClaw JobBot Pipeline

```
                         ┌─────────────────────────────────┐
                         │         ENTRY POINTS            │
                         │                                 │
                         │  CLI: python3 main.py [command] │
                         │  Telegram: Natural Language Bot  │
                         └───────────────┬─────────────────┘
                                         │
                         ┌───────────────▼─────────────────┐
                         │         ORCHESTRATOR            │
                         │  Session ID, JOBID counter,     │
                         │  Config loading, Pipeline ctrl  │
                         └───────────────┬─────────────────┘
                                         │
          ╔══════════════════════════════════════════════════════════╗
          ║              SYSTEM 1: JOB DISCOVERY                    ║
          ╚══════════════════════════════════════════════════════════╝
                                         │
                         ┌───────────────▼─────────────────┐
                         │      Job Search Agent           │
                         │  RapidAPI JSearch → LinkedIn,    │
                         │  Indeed, Glassdoor, Monster,     │
                         │  ZipRecruiter                    │
                         │  Output: Raw job listings        │
                         └───────────────┬─────────────────┘
                                         │
                         ┌───────────────▼─────────────────┐
                         │      Keyword Agent              │
                         │  Claude AI extracts structured   │
                         │  keywords from each job desc     │
                         │  Output: Jobs with keywords      │
                         └───────────────┬─────────────────┘
                                         │
                         ┌───────────────▼─────────────────┐
                         │      Relevance Agent            │
                         │  Claude AI scores relevance     │
                         │  vs Mo's profile (1-10)         │
                         │  Threshold: 5/10                │
                         │  Output: Filtered relevant jobs  │
                         └───────────────┬─────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │                     │
                         ≥ 5/10                  < 5/10
                         RELEVANT               FILTERED OUT
                              │                 (skipped)
                              │
          ╔═══════════════════▼══════════════════════════════════════╗
          ║         SYSTEM 2: RESUME & COVER LETTER TAILORING       ║
          ╚═════════════════════════════════════════════════════════╝
                              │
              ┌───────────────▼─────────────────┐
              │      Resume Parser              │
              │  pdfplumber reads master PDF     │
              │  (cached — runs once per run)    │
              └───────────────┬─────────────────┘
                              │
         ┌────────────────────▼────────────────────┐
         │  FOR EACH RELEVANT JOB:                 │
         │                                         │
         │  ┌─────────────────────────────────┐    │
         │  │  ATS Scorer                     │    │
         │  │  Keyword match % + Score 1-10   │    │
         │  └──────────────┬──────────────────┘    │
         │                 │                        │
         │      ┌──────────┴──────────┐            │
         │      │                     │            │
         │  Score < 7              Score ≥ 7       │
         │  OR Match < 80%        AND Match ≥ 80%  │
         │      │                     │            │
         │      ▼                     ▼            │
         │  ┌──────────────┐  ┌──────────────┐    │
         │  │Resume Tailor │  │ Use Master   │    │
         │  │Claude AI     │  │ Resume As-Is │    │
         │  │(max 2 iter)  │  └──────────────┘    │
         │  └──────┬───────┘                       │
         │         │                               │
         │  ┌──────▼───────────────────────────┐   │
         │  │  Cover Letter Agent              │   │
         │  │  Claude AI generates 3-4 para    │   │
         │  │  personalized cover letter       │   │
         │  └──────────────┬───────────────────┘   │
         │                 │                        │
         │  ┌──────────────▼───────────────────┐   │
         │  │  Recruiter Finder                │   │
         │  │  Regex + Claude AI extracts      │   │
         │  │  name, email, phone              │   │
         │  └──────────────┬───────────────────┘   │
         │                 │                        │
         │                 ▼                        │
         │  ╔══════════════════════════════════╗    │
         │  ║  SYSTEM 3: TRACKING (real-time)  ║    │
         │  ╠══════════════════════════════════╣    │
         │  ║                                  ║    │
         │  ║  File Manager                    ║    │
         │  ║  → Assign JOBID (JOB001, etc)    ║    │
         │  ║  → Save Resume PDF               ║    │
         │  ║  → Save Cover Letter PDF         ║    │
         │  ║                                  ║    │
         │  ║  Sheets Agent                    ║    │
         │  ║  → Append row to Google Sheet    ║    │
         │  ║    (real-time, per job)           ║    │
         │  ║                                  ║    │
         │  ║  Telegram Agent                  ║    │
         │  ║  → Progress notifications        ║    │
         │  ║  → Completion summary            ║    │
         │  ╚══════════════════════════════════╝    │
         │                                         │
         └──────── LOOP NEXT JOB ──────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │   RUN COMPLETE      │
                    │   Stats + Summary   │
                    │   → Terminal output  │
                    │   → Telegram message │
                    │   → Google Sheet     │
                    │     fully populated  │
                    └─────────────────────┘
```

### Future Plan: Full OpenClaw Ecosystem

```
                    ┌─────────────────────────────────────────────┐
                    │           OPENCLAW GATEWAY                  │
                    │  Central orchestrator for all agents        │
                    │  Entry: Telegram (NL) + CLI + Web Dashboard │
                    └─────────────────────┬───────────────────────┘
                                          │
        ┌──────────┬──────────┬───────────┼───────────┬──────────┬──────────┐
        │          │          │           │           │          │          │
        ▼          ▼          ▼           ▼           ▼          ▼          ▼
  ┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐
  │  JOB     ││POLYMARKET││ CRYPTO & ││MARKETING ││FREELANCE ││ DIGITAL  ││ SOCIAL   │
  │  SEARCH  ││ TRADING  ││ STOCK    ││ AGENTS   ││ AGENTS   ││ MARKETING││ MEDIA    │
  │  BOT     ││ SYSTEM   ││ TRADING  ││          ││          ││ AGENT    ││ PLANNER  │
  │ ✅ BUILT ││ 🔲 P3    ││ 🔲 P5    ││ 🔲 P4    ││ 🔲 P8    ││ 🔲 P7    ││ 🔲 P9    │
  └────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘
       │           │           │           │           │           │           │
       │      ┌────┴────┐     │      ┌────┴────┐     │           │           │
       │      │3 Teams  │     │      │Revenue  │     │           │           │
       │      │Conserv. │     │      │Content  │     │           │           │
       │      │Moderate │     │      │Reseller │     │           │           │
       │      │Aggress. │     │      │         │     │           │           │
       │      │6 Strats │     │      │         │     │           │           │
       │      └─────────┘     │      └─────────┘     │           │           │
       │                      │                       │           │           │
       └──────────┬───────────┴───────────┬───────────┴───────────┴───────────┘
                  │                       │
                  ▼                       ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │                    SHARED PLATFORM (Priority 6)                   │
  │                                                                   │
  │  ┌─────────────┐ ┌──────────────┐ ┌─────────────┐ ┌───────────┐ │
  │  │ 6.1         │ │ 6.2          │ │ 6.3         │ │ 6.4       │ │
  │  │ Portfolio   │ │ Agent Status │ │ Job Agent   │ │ Polymarket│ │
  │  │ Website    │ │ Dashboard    │ │ Dashboard   │ │ Dashboard │ │
  │  │ 🔲         │ │ 🔲           │ │ 🔲          │ │ 🔲        │ │
  │  └─────────────┘ └──────────────┘ └─────────────┘ └───────────┘ │
  │                                                                   │
  │  All under single domain · Built with same tech stack             │
  └───────────────────────────────────────────────────────────────────┘
                  │
                  ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │                    SHARED FOUNDATION                              │
  │                                                                   │
  │  Config Management · Secret Management (.env)                     │
  │  Anthropic Claude API · Telegram Bot API                          │
  │  Google Sheets · PDF Generation · Logging                         │
  │  GitHub · Google Drive                                            │
  └───────────────────────────────────────────────────────────────────┘

  Legend: ✅ Built & Working | 🔲 Planned | P# = Priority number
```

---

## Active Projects

### 1. OpenClaw JobBot (WORKING)

**Location:** `~/Projects/mo-automation/Opus/openclaw-jobbot/`
**GitHub:** `github.com/mhaleem87/openclaw-jobbot-opus4.6` (private)
**Status:** Built, tested, and deployed. End-to-end pipeline working.
**Built with:** Claude Opus 4.6 (March 8, 2026)

**What it does:**
Automated job search pipeline that finds relevant jobs, tailors resumes, generates cover letters, extracts recruiter contacts, and updates Google Sheets — all with Telegram notifications.

**3-System Architecture:**

| System | Purpose | Agents |
|--------|---------|--------|
| System 1: Discovery | Find and filter jobs | Job Search Agent, Keyword Agent, Relevance Agent |
| System 2: Tailoring | Prepare application materials | Resume Parser, ATS Scorer, Resume Tailor, Cover Letter Agent, Recruiter Finder |
| System 3: Tracking | Save outputs and notify | File Manager, Sheets Agent, Telegram Agent |

**Entry Points:**

| Method | Command |
|--------|---------|
| Full pipeline | `python3 main.py full --notify` |
| Search only | `python3 main.py search --roles "PM" --locations "Dubai"` |
| Tailor resume | `python3 main.py tailor --job-description "..." --title "PO" --company "Google"` |
| Cover letter | `python3 main.py cover-letter --job-description "..." --title "PO" --company "Google"` |
| Extract keywords | `python3 main.py keywords --job-description "..."` |
| Telegram bot | `python3 bot.py` (natural language commands) |

**Key Configurations (config.yaml):**
- Target roles: Project Manager, Product Owner, Business Analyst, Scrum Master
- Target locations: New York, UAE, Dubai, Abu Dhabi, Saudi Arabia, Riyadh
- ATS threshold: 7/10
- Keyword match threshold: 80%
- Relevance threshold: 5/10
- Model: claude-haiku-4-5-20251001

**Integrations:**
- RapidAPI JSearch (LinkedIn, Indeed, Glassdoor, Monster, ZipRecruiter)
- Anthropic Claude API (keyword extraction, resume tailoring, cover letters, recruiter finding, relevance scoring)
- Google Sheets (gspread + service account)
- Telegram Bot API (notifications + natural language interface)
- PDF generation (reportlab)

**Output:**
- Tailored resume PDFs: `output/resumes/JOB001_Company_Title_Resume.pdf`
- Cover letter PDFs: `output/cover_letters/JOB001_Company_Title_Coverletter.pdf`
- Google Sheet: "Jobs Found By AI" (16 columns, real-time updates)

---

## Pending Projects (Not Yet Built)

These are on the priority list but have no working code yet:

| Priority | Project | Status |
|----------|---------|--------|
| 3 | Polymarket Trading System | Planned — 3 teams, 6 strategies. No code yet. |
| 4 | Marketing Agents | Planned — revenue generation. No code yet. |
| 5 | Crypto & Stock Trading | Planned. No code yet. |
| 6.1 | Personal Portfolio Website | Planned. No code yet. |
| 6.2 | Agent Status Dashboard | Planned. No code yet. |
| 6.3 | Job Agent Output Dashboard | Planned. No code yet. |
| 6.4 | Polymarket Trading Dashboard | Planned. No code yet. |
| 7 | Digital Marketing Agent | Planned. No code yet. |
| 8 | Freelancing Agents | Planned. No code yet. |
| 9 | Social Media Planning | Planned. No code yet. |

---

## Old Projects (Pending Deletion)

These were built by Haiku 4.5 and have been replaced or found to be empty scaffolding. Renamed with `_Old_Can_Be_Deleted` suffix. GitHub repos still exist but will be deleted.

| Project | What it was | Why it's being deleted |
|---------|------------|----------------------|
| `python-job-agent` | Monolithic job search pipeline | Replaced by OpenClaw JobBot |
| `openclaw` | Multi-agent scaffolding | Empty — only READMEs and requirements.txt, no real code |
| `macbook-controller` | Telegram bot for Mac remote control | Working but Haiku-built — to be rebuilt with Opus |
| `job-tracker-utility` | CLI job application tracker | Working but simple — to be rebuilt or replaced |

---

## Infrastructure

**Machine:** MacBook Pro (Late 2016), macOS via OCLP
**Python:** 3.14.3
**Shell:** bash (zsh available)
**Git:** Configured with SSH to GitHub (`mhaleem87`)

**API Keys (stored in .env files, never in code):**
- Anthropic Claude API
- RapidAPI (JSearch)
- Telegram Bot API
- Google Sheets (service account credentials.json)

**GitHub Repos:**
- `mhaleem87/mo-automation` — public monorepo (main)
- `mhaleem87/openclaw-jobbot-opus4.6` — private (active JobBot)
- `mhaleem87/python-job-agent` — private (to be deleted)
- `mhaleem87/openclaw` — public (to be deleted)
- `mhaleem87/macbook-controller` — status unknown (to be deleted)
- `mhaleem87/job-tracker-utility` — status unknown (to be deleted)

---

## Credentials & Secrets

All secrets are stored in `.env` files, never hardcoded. Each project has its own `.env`.

| Secret | Used By | Location |
|--------|---------|----------|
| ANTHROPIC_API_KEY | JobBot (keyword extraction, tailoring, cover letters) | `Opus/openclaw-jobbot/.env` |
| RAPIDAPI_KEY | JobBot (JSearch job board API) | `Opus/openclaw-jobbot/.env` |
| TELEGRAM_BOT_TOKEN | JobBot (notifications + bot) | `Opus/openclaw-jobbot/.env` |
| TELEGRAM_CHAT_ID | JobBot (Mo's chat for notifications) | `Opus/openclaw-jobbot/.env` |
| credentials.json | Google Sheets service account | `Opus/openclaw-jobbot/credentials.json` |

**Security notes:**
- Old `python-job-agent/config/config.py` had hardcoded API keys — never committed to public repo (repo is private)
- Notion API token was revoked (Notion integration fully removed March 8, 2026)
- All `.env` and `credentials.json` files are gitignored

---

## Key File Paths (Mac)

| What | Path |
|------|------|
| Main project directory | `~/Projects/mo-automation/` |
| Active JobBot | `~/Projects/mo-automation/Opus/openclaw-jobbot/` |
| Master resume | `~/Downloads/job_ai_agent/resume.pdf` |
| Google credentials | `~/Projects/mo-automation/Opus/openclaw-jobbot/credentials.json` |
| Chat history | `~/Downloads/Claude Chat History/` |
| Code history | `~/Downloads/Claude Code History/` |

---

## Workflow

| Task | Tool |
|------|------|
| Planning, strategy, research, documents | Claude Chat (claude.ai) |
| Building, coding, testing, debugging | Claude Code (terminal) |
| File operations, git, system admin | Claude Code (terminal) |
| Pattern | Plan in Chat → Build in Code → Review in Chat |

---

## Cleanup History

| Date | Action |
|------|--------|
| March 8, 2026 | Removed all Notion integration (files, app, memory, git references) |
| March 8, 2026 | Deleted all 20 Haiku-created skill files (generic filler) |
| March 8, 2026 | Deleted OPENCLAW_DOCUMENTATION.md (aspirational fiction) |
| March 8, 2026 | Deleted doc maintenance files (DOCUMENTATION_UPDATES.log, DOC_UPDATE_CHECKLIST.md, check_doc_sync.sh, .claude-code-memory.txt) |
| March 8, 2026 | Killed chat_auto_saver.py LaunchAgent |
| March 8, 2026 | Built OpenClaw JobBot from scratch with Opus (3 systems, 10 agents) |
| March 8, 2026 | Renamed old Haiku projects with _Old_Can_Be_Deleted suffix |
| March 8, 2026 | Memory cleaned: 12 entries → 4 entries |

---

## Outstanding TODOs

- [ ] Delete old GitHub repos (python-job-agent, openclaw, macbook-controller, job-tracker-utility)
- [ ] Remove submodule references from mo-automation
- [ ] Delete renamed `_Old_Can_Be_Deleted` local folders
- [ ] Rotate API keys (Anthropic, RapidAPI, Telegram) — old ones were in Haiku code
- [ ] Test Telegram bot (bot.py) live
- [ ] Run full-scale job search (all roles × all locations, no --limit)
- [ ] Rebuild macbook-controller with Opus
- [ ] Update mo-automation CLAUDE.md to reflect new structure
- [ ] Start Polymarket trading system (Priority 3)
