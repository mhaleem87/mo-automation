# mo-automation

A collection of AI-powered automation projects built with Claude AI.

## Projects

### [macbook-controller](https://github.com/mhaleem87/macbook-controller)
Remote control your MacBook via Telegram using natural language. Send messages like "take a screenshot" or "what's my CPU usage" and Claude AI translates them into system actions.

**Capabilities:** screenshots, camera capture, system info, app control, file operations, shell commands, power management.

### [python-job-agent](https://github.com/mhaleem87/python-job-agent)
End-to-end job search automation pipeline. Searches multiple job boards, tailors your resume to each listing, generates cover letters, finds recruiter contacts, and logs everything to Google Sheets.

**Interfaces:** CLI, Streamlit web dashboard, Telegram bot.

### [openclaw](https://github.com/mhaleem87/openclaw)
Modular rewrite of python-job-agent as independent microservice agents (job-fetcher, resume-updater, keyword-analyzer, ats-scorer, cover-letter-generator, sheets-manager). Work in progress.

## Stack
- Python 3
- [Claude AI](https://anthropic.com) (Haiku) for NLP and content generation
- Telegram Bot API for remote interfaces
- Google Sheets API for data storage
- Streamlit for web UI
- RapidAPI for job board aggregation
