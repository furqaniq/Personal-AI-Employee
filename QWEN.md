# Personal AI Employee - Project Context

## Project Overview

This is a **hackathon project** for building an autonomous "Digital FTE" (Full-Time Equivalent) - an AI agent that proactively manages personal and business affairs 24/7. The project uses **Claude Code** as the reasoning engine and **Obsidian** (local Markdown) as the dashboard/memory system.

### Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Personal AI Employee                      │
├─────────────────────────────────────────────────────────────┤
│  Perception (Watchers) → Reasoning (Claude) → Action (MCP)  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Watchers (Python scripts):                                  │
│    • Gmail Watcher - monitors emails                         │
│    • WhatsApp Watcher - monitors messages (Playwright)       │
│    • File System Watcher - monitors drop folders             │
│                                                              │
│  Reasoning: Claude Code with Ralph Wiggum persistence loop   │
│                                                              │
│  Action: MCP Servers (Model Context Protocol)                │
│    • Playwright MCP - browser automation                     │
│    • Email MCP - send/draft emails                           │
│    • Custom MCPs - domain-specific actions                   │
│                                                              │
│  Memory/GUI: Obsidian Vault (Markdown files)                 │
│    • /Inbox - incoming items                                 │
│    • /Needs_Action - pending tasks                           │
│    • /Done - completed tasks                                 │
│    • /Pending_Approval - human-in-the-loop decisions         │
└─────────────────────────────────────────────────────────────┘
```

### Key Concepts

- **Watchers**: Lightweight Python scripts that monitor external systems (Gmail, WhatsApp, filesystems) and create action files in the Obsidian vault
- **Ralph Wiggum Loop**: A persistence pattern using a Stop hook that keeps Claude working autonomously until tasks are complete
- **Human-in-the-Loop (HITL)**: Sensitive actions require approval via file movement (`/Pending_Approval` → `/Approved`)
- **Monday Morning CEO Briefing**: Autonomous weekly audit generating business insights

## Repository Structure

```
Personal-AI-Employee/
├── .agents/skills/           # Agent skills for Claude Code
│   └── browsing-with-playwright/
│       ├── SKILL.md          # Skill documentation
│       ├── scripts/
│       │   ├── mcp-client.py # Universal MCP client (HTTP + stdio)
│       │   ├── start-server.sh
│       │   ├── stop-server.sh
│       │   └── verify.py
│       └── references/
│           └── playwright-tools.md
├── .claude/skills/           # Claude-specific skills (symlink/copy)
├── .qwen/skills/             # Qwen-specific skills (symlink/copy)
├── skills-lock.json          # Skill version tracking
└── Personal AI Employee Hackathon 0_...md  # Full architecture doc
```

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Claude Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Watcher scripts & orchestration |
| Node.js | v24+ LTS | MCP servers |

### Playwright MCP Server

**Start the server:**
```bash
bash .agents/skills/browsing-with-playwright/scripts/start-server.sh
# Or: npx @playwright/mcp@latest --port 8808 --shared-browser-context &
```

**Stop the server:**
```bash
bash .agents/skills/browsing-with-playwright/scripts/stop-server.sh
```

**Verify server is running:**
```bash
python .agents/skills/browsing-with-playwright/scripts/verify.py
```

### MCP Client Usage

The included `mcp-client.py` supports both HTTP and stdio transports:

```bash
# List available tools
python mcp-client.py list --url http://localhost:8808

# Call a tool
python mcp-client.py call --url http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://example.com"}'

# Take a screenshot
python mcp-client.py call --url http://localhost:8808 -t browser_take_screenshot \
  -p '{"type": "png", "fullPage": true}'

# Get page snapshot (accessibility tree)
python mcp-client.py call --url http://localhost:8808 -t browser_snapshot -p '{}'
```

### Common Browser Automation Workflow

```bash
# 1. Navigate
python mcp-client.py call -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://example.com"}'

# 2. Get snapshot to find element refs
python mcp-client.py call -u http://localhost:8808 -t browser_snapshot -p '{}'

# 3. Interact with elements (using refs from snapshot)
python mcp-client.py call -u http://localhost:8808 -t browser_click \
  -p '{"element": "Submit button", "ref": "e42"}'

# 4. Type text
python mcp-client.py call -u http://localhost:8808 -t browser_type \
  -p '{"element": "Search input", "ref": "e15", "text": "hello", "submit": true}'
```

## Development Conventions

### Skill Structure

Each skill in `.agents/skills/` follows this pattern:
- `SKILL.md` - Main documentation with usage examples
- `scripts/` - Executable scripts (MCP client, server management)
- `references/` - Auto-generated tool documentation

### MCP Client Patterns

The `mcp-client.py` is a universal client that can be bundled with any skill:

```bash
# HTTP transport
python mcp-client.py list --url http://localhost:8080

# Stdio transport (for local MCP servers)
python mcp-client.py list --stdio "npx -y @modelcontextprotocol/server-github"

# Emit tool schemas as markdown
python mcp-client.py emit --url http://localhost:8808 --format markdown
```

### Watcher Pattern (for building new watchers)

All watchers follow the base pattern from the architecture doc:

```python
from base_watcher import BaseWatcher
from pathlib import Path

class MyWatcher(BaseWatcher):
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        content = f"""---
type: {item_type}
status: pending
---

## Content
{item_content}
"""
        filepath = self.needs_action / f'{item_type}_{item_id}.md'
        filepath.write_text(content)
        return filepath
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `Personal AI Employee Hackathon 0_...md` | Full architecture blueprint (1200+ lines) |
| `skills-lock.json` | Tracks installed skill versions |
| `.agents/skills/browsing-with-playwright/SKILL.md` | Browser automation skill docs |
| `.agents/skills/browsing-with-playwright/scripts/mcp-client.py` | Universal MCP client |
| `.agents/skills/browsing-with-playwright/references/playwright-tools.md` | All 22 Playwright MCP tools |

## Hackathon Tiers

| Tier | Description | Time |
|------|-------------|------|
| **Bronze** | Foundation: Obsidian vault, one watcher, Claude integration | 8-12h |
| **Silver** | Functional: Multiple watchers, MCP server, HITL workflow | 20-30h |
| **Gold** | Autonomous: Full integration, Ralph Wiggum loop, CEO briefings | 40+h |
| **Platinum** | Production: Cloud deployment, work-zone specialization | 60+h |

## Important Notes

- **Local-first**: All data stored locally in Obsidian Markdown files
- **Privacy**: Secrets never sync (`.env`, tokens, sessions kept local)
- **Claim-by-move rule**: First agent to move item from `/Needs_Action` to `/In_Progress/<agent>/` owns it
- **Single-writer rule**: Only Local writes to `Dashboard.md`
