# 📋 DOCUMENTATION UPDATE CHECKLIST

## When to Update Documentation

Update `OPENCLAW_DOCUMENTATION.md` when:

- [ ] New project created
- [ ] New agent built
- [ ] New Telegram bot deployed
- [ ] New integration added
- [ ] Existing agent functionality changed
- [ ] New API credentials added
- [ ] Workflow process changed
- [ ] Bug fixes or improvements
- [ ] Deployment procedure changed

---

## Update Procedure (Step-by-Step)

### Step 1: Identify Change Type
- Is this a new component? (NEW)
- Is this modifying existing? (UPDATE)
- Is this a bug fix? (FIX)
- Is this adding capability? (ENHANCEMENT)
- Is this adding integration? (INTEGRATION)

### Step 2: Edit Main Documentation
```bash
nano ~/Projects/mo-automation/OPENCLAW_DOCUMENTATION.md
```

- Find relevant section
- Add new content or modify existing
- Update file paths if changed
- Update command examples if changed
- Update any related integrations section

### Step 3: Update the Log
```bash
nano ~/Projects/mo-automation/DOCUMENTATION_UPDATES.log
```

Add entry at top of "Update History" section:
```
### V1.1 - [TITLE OF CHANGE]
- **Date:** 2026-03-07
- **Type:** [NEW/UPDATE/FIX/ENHANCEMENT/INTEGRATION]
- **Changes:**
  * [What was added/changed]
  * [What was added/changed]
  * [What was added/changed]
```

### Step 4: Version Bump
- **Minor changes (V1.0 → V1.1):** Bug fixes, small additions
- **Major changes (V1.1 → V2.0):** New major component, architecture change

Update version in:
1. Top of OPENCLAW_DOCUMENTATION.md: `**Version:** 1.1`
2. In DOCUMENTATION_UPDATES.log section header

### Step 5: Git Commit & Push
```bash
cd ~/Projects/mo-automation

# Add both files
git add OPENCLAW_DOCUMENTATION.md
git add DOCUMENTATION_UPDATES.log

# Commit with proper format
git commit -m "docs: [TYPE] - [DESCRIPTION]"

# Push to GitHub
git push origin main
```

---

## Commit Message Examples

### New Agent Added
```bash
git commit -m "docs: add - New resume-screening-agent with ML capabilities"
```

### Workflow Changed
```bash
git commit -m "docs: update - Modify job search pipeline orchestration"
```

### Bug Fixed in Documentation
```bash
git commit -m "docs: fix - Correct Telegram bot token storage location"
```

### New Integration Added
```bash
git commit -m "docs: integration - Add Slack webhook integration"
```

### Enhancement/Feature Added
```bash
git commit -m "docs: enhancement - Add natural language support to MacBook controller bot"
```

---

## Sections to Update (by Change Type)

### If Adding New Project:
- [ ] PROJECT ECOSYSTEM section
- [ ] Add new project subsection
- [ ] Add project to architecture diagram
- [ ] Add setup instructions
- [ ] Add to file locations table

### If Adding New Agent:
- [ ] CORE AGENTS & COMPONENTS section
- [ ] Add agent subsection with:
  - [ ] Purpose
  - [ ] Key files location
  - [ ] How it works
  - [ ] Output format
  - [ ] Start command
- [ ] Update PROJECT ECOSYSTEM structure
- [ ] Add to QUICK REFERENCE table

### If Adding New Telegram Bot:
- [ ] TELEGRAM BOTS section
- [ ] Add bot subsection with:
  - [ ] Purpose
  - [ ] Location
  - [ ] Token/credentials
  - [ ] Commands (slash style)
  - [ ] Natural language examples
- [ ] Add to integration points

### If Adding New Integration:
- [ ] INTEGRATION POINTS section
- [ ] Add integration subsection with:
  - [ ] Status
  - [ ] Components
  - [ ] Credentials location
  - [ ] Functions available
  - [ ] Usage example
- [ ] Update configuration section
- [ ] Update file locations table

### If Changing Workflow:
- [ ] WORKFLOWS & PROCESSES section
- [ ] Update workflow diagram/steps
- [ ] Update start commands if changed
- [ ] Update expected output/duration
- [ ] Update any affected agent sections

### If Adding New Credential:
- [ ] CONFIGURATION & CREDENTIALS section
- [ ] Add to environment variables list
- [ ] Add to file locations table
- [ ] Add security note if applicable

---

## Quick Checklist Before Commit

Before running `git commit`, verify:

- [ ] Main documentation file updated
- [ ] Update log entry added
- [ ] Version number bumped
- [ ] All file paths are correct
- [ ] All command examples tested
- [ ] No typos or formatting errors
- [ ] New sections follow existing format
- [ ] Tables are properly formatted
- [ ] Links/references are correct

---

## File Format Guidelines

### For Agent Sections
```markdown
#### [Agent-Name-Agent] [Emoji]

**Purpose:** [One sentence describing what it does]

**Key Files:**
- `path/to/file.py`

**How It Works:**
1. First step
2. Second step
3. Third step

**Output:**
- Format
- Structure
- Example

**Start Command:**
\`\`\`bash
command here
\`\`\`
```

### For Bot Sections
```markdown
### Bot [Number]: [Bot-Name] [Emoji]

**Purpose:** [What it does]

**Location:** `path/to/bot.py`

**Token:** Stored in .env

**Interactions:**

#### Commands:
\`\`\`
/command1
/command2
\`\`\`

#### Natural Language:
\`\`\`
"example request"
"another example"
\`\`\`
```

---

## Common Mistakes to Avoid

- ❌ Forget to update version number
- ❌ Update doc but not the log
- ❌ Wrong git commit message format
- ❌ Incomplete information in new sections
- ❌ Forgot to test command examples
- ❌ Inconsistent formatting with existing sections
- ❌ Didn't push to GitHub

---

## Getting Help

If unsure about updating, ask yourself:
1. What component was added/changed?
2. Which section of the doc covers this?
3. What are the key details to include?
4. What commit message best describes this?
5. Does this need version bump (V1.1 or V2.0)?

---

