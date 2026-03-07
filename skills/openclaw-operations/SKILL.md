# 🤖 OPENCLAW OPERATIONS SKILL

**Skill Name:** openclaw-operations  
**Version:** 1.0  
**Created:** 2026-03-07  
**Target Audience:** Claude Chat, Claude Code  
**Priority:** HIGH

---

## 📋 SKILL OVERVIEW

This skill provides **comprehensive best practices** for running the OpenClaw multi-agent job search system and spinning up specialized sub-agents.

**Key Areas:**
- System startup procedures
- Agent orchestration patterns
- Agent initialization & configuration
- Monitoring & health checks
- Performance optimization
- Troubleshooting workflows
- Graceful shutdown procedures

---

## 🎯 WHEN TO USE THIS SKILL

Use this skill whenever:
- ✅ Starting the OpenClaw system
- ✅ Spinning up individual agents
- ✅ Managing agent lifecycle
- ✅ Monitoring system performance
- ✅ Troubleshooting system issues
- ✅ Optimizing agent execution
- ✅ Scaling the system
- ✅ Deploying new agents

---

## 📚 SKILL CONTENT

### SECTION 1: SYSTEM STARTUP PROCEDURES

#### Prerequisites Check
Before starting OpenClaw, verify:

\`\`\`bash
# Check Python version (3.8+)
python3 --version

# Check required packages
pip3 list | grep -E "anthropic|google|telegram"

# Check environment variables
cat ~/.env | grep -E "NOTION_TOKEN|ANTHROPIC_API_KEY|TELEGRAM"

# Check directory structure
ls -la ~/Projects/mo-automation/openclaw/
\`\`\`

#### Full System Startup

**Procedure:**

1. **Navigate to orchestrator**
   \`\`\`bash
   cd ~/Projects/mo-automation/openclaw/job-search/job-search-orchestrator/src
   \`\`\`

2. **Verify configuration**
   \`\`\`bash
   python3 -c "from main import config; print(config)"
   \`\`\`

3. **Start with parameters**
   \`\`\`bash
   python main.py \\
     --roles "Product Manager" "Business Analyst" \\
     --locations "New York" "Dubai" \\
     --max-applications 50 \\
     --log-level INFO
   \`\`\`

4. **Monitor execution**
   - Watch terminal output
   - Check Telegram for notifications
   - View dashboard: http://localhost:8502
   - Monitor event log: tail -f ~/Projects/mo-automation/openclaw/events.jsonl

#### Full System Startup Best Practices

**Do:**
- ✅ Always check prerequisites first
- ✅ Use meaningful search parameters
- ✅ Start monitoring dashboard before running
- ✅ Have terminal open to watch logs
- ✅ Enable Telegram notifications
- ✅ Set reasonable application limits
- ✅ Document the run parameters

**Don't:**
- ❌ Run without checking .env credentials
- ❌ Use vague search parameters
- ❌ Run multiple instances simultaneously
- ❌ Ignore error messages
- ❌ Set unrealistic application limits
- ❌ Skip prerequisite checks

---

### SECTION 2: INDIVIDUAL AGENT STARTUP

#### Agent Startup Template

**General Pattern:**
\`\`\`bash
cd ~/Projects/mo-automation/openclaw/job-search/[agent-name]
python src/main.py --config config.yaml --verbose
\`\`\`

#### Job-Fetcher-Agent Startup

**Purpose:** Fetch raw job listings

**Startup:**
\`\`\`bash
cd ~/Projects/mo-automation/openclaw/job-search/job-fetcher-agent
python src/fetcher.py \\
  --roles "Product Manager" \\
  --locations "Dubai" "New York" \\
  --max-results 300 \\
  --output jobs_raw.json
\`\`\`

**Configuration:**
- \`--roles\`: Space-separated list of job titles
- \`--locations\`: Space-separated list of cities
- \`--max-results\`: Maximum jobs to fetch (default: 300)
- \`--output\`: Output file name

**Expected Output:**
- JSON file with 50-300 raw jobs
- Console log of fetch progress
- Summary statistics

**Monitoring:**
\`\`\`bash
# Watch fetch progress
tail -f /tmp/job_fetcher.log

# Check output file
wc -l jobs_raw.json
\`\`\`

---

### SECTION 3: AGENT ORCHESTRATION PATTERNS

#### Pattern 1: Sequential Execution (Recommended)

**When to use:** Default workflow for job applications

**Flow:**
\`\`\`
1. Job-Fetcher-Agent (output: jobs_raw.json)
   ↓
2. Keyword-Analyzer-Agent (output: jobs_analyzed.json)
   ↓
3. ATS-Scorer-Agent (output: jobs_scored.json)
   ↓
4. Resume-Updater-Agent (output: resumes/)
   ↓
5. Cover-Letter-Generator-Agent (output: letters/)
   ↓
6. Sheets-Manager-Agent (output: Google Sheets)
   ↓
COMPLETE: 100+ tailored applications ready
\`\`\`

**Implementation:**
\`\`\`bash
# Use job-search-orchestrator
cd ~/Projects/mo-automation/openclaw/job-search/job-search-orchestrator/src
python main.py --roles "Product Manager" --locations "Dubai"
\`\`\`

**Duration:** 12-15 minutes  
**Output:** 100+ job applications

---

### SECTION 4: MONITORING & HEALTH CHECKS

#### Real-time Monitoring

**Dashboard:**
\`\`\`bash
# Terminal 1: Start monitor
cd ~/Projects/mo-automation/openclaw/activity-monitor-agent/src
python monitor.py

# Terminal 2: Start dashboard
streamlit run dashboard.py
\`\`\`

**Access:** http://localhost:8502

#### Event Log Monitoring

**Watch live events:**
\`\`\`bash
tail -f ~/Projects/mo-automation/openclaw/events.jsonl
\`\`\`

---

### SECTION 5: TROUBLESHOOTING WORKFLOWS

#### Issue: Agent Crashes Unexpectedly

**Diagnosis:**
\`\`\`bash
tail -100 ~/Projects/mo-automation/openclaw/events.jsonl | grep -i error
\`\`\`

**Solutions:**
1. Verify .env credentials
2. Check API rate limits
3. Restart the agent
4. Check Python version compatibility
5. Review agent-specific logs

---

### SECTION 6: PERFORMANCE OPTIMIZATION

#### Cost-Optimized Configuration
\`\`\`bash
python main.py \\
  --roles "Product Manager" \\
  --locations "Dubai" \\
  --batch-size 20 \\
  --model haiku \\
  --max-applications 30
\`\`\`

#### Quality-Optimized Configuration
\`\`\`bash
python main.py \\
  --roles "Product Manager" \\
  --locations "Dubai" \\
  --batch-size 5 \\
  --model sonnet \\
  --max-applications 20
\`\`\`

---

## 🔧 QUICK REFERENCE COMMANDS

\`\`\`bash
# Full system startup
cd ~/Projects/mo-automation/openclaw/job-search/job-search-orchestrator/src
python main.py --roles "Product Manager" --locations "Dubai"

# Monitor dashboard
cd ~/Projects/mo-automation/openclaw/activity-monitor-agent/src
streamlit run dashboard.py

# Check event log
tail -f ~/Projects/mo-automation/openclaw/events.jsonl
\`\`\`

---

## 📞 WHEN TO USE THIS SKILL

- ✅ Starting OpenClaw system
- ✅ Spinning up individual agents
- ✅ Troubleshooting issues
- ✅ Optimizing performance
- ✅ Monitoring execution
- ✅ Integrating new components
- ✅ Creating documentation
- ✅ Training on procedures

---

## 📝 SKILL VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-07 | Initial comprehensive skill |

---

**Skill Status:** ✅ Complete and Ready  
**Last Updated:** 2026-03-07
