#!/bin/bash

# Documentation Sync Check Script
# Run this to verify documentation is up-to-date

echo "🔍 Checking OpenClaw Documentation Status..."
echo ""

DOC_FILE=~/Projects/mo-automation/OPENCLAW_DOCUMENTATION.md
LOG_FILE=~/Projects/mo-automation/DOCUMENTATION_UPDATES.log
CHECKLIST_FILE=~/Projects/mo-automation/DOC_UPDATE_CHECKLIST.md

# Check if files exist
echo "📋 Verifying documentation files exist..."
echo ""

if [ -f "$DOC_FILE" ]; then
    echo "✅ Main documentation: FOUND"
else
    echo "❌ Main documentation: MISSING"
fi

if [ -f "$LOG_FILE" ]; then
    echo "✅ Update log: FOUND"
else
    echo "❌ Update log: MISSING"
fi

if [ -f "$CHECKLIST_FILE" ]; then
    echo "✅ Update checklist: FOUND"
else
    echo "❌ Update checklist: MISSING"
fi

echo ""
echo "📁 File Information:"
echo ""

# Show file sizes
if [ -f "$DOC_FILE" ]; then
    SIZE=$(ls -lh "$DOC_FILE" | awk '{print $5}')
    echo "Documentation size: $SIZE"
fi

if [ -f "$LOG_FILE" ]; then
    LINES=$(wc -l < "$LOG_FILE")
    echo "Update log entries: $LINES lines"
fi

echo ""
echo "📅 Last Modified Dates:"
echo ""

if [ -f "$DOC_FILE" ]; then
    LAST_MOD=$(stat -f "%Sm" "$DOC_FILE" 2>/dev/null || stat -c %y "$DOC_FILE" 2>/dev/null)
    echo "Documentation: $LAST_MOD"
fi

if [ -f "$LOG_FILE" ]; then
    LAST_MOD=$(stat -f "%Sm" "$LOG_FILE" 2>/dev/null || stat -c %y "$LOG_FILE" 2>/dev/null)
    echo "Update log: $LAST_MOD"
fi

echo ""
echo "📝 Recent Update Log Entries:"
echo ""

if [ -f "$LOG_FILE" ]; then
    head -20 "$LOG_FILE" | tail -10
fi

echo ""
echo "✅ Documentation Check Complete!"
echo ""
