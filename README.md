<div align="center">

# Asyre File

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/yzha0302/asyre-file?style=flat-square&color=7c3aed)](https://github.com/yzha0302/asyre-file/releases)
[![Docker](https://img.shields.io/badge/docker-ready-2496ed?style=flat-square&logo=docker&logoColor=white)](Dockerfile)

**A shared file system between AI agents and humans — command your server AI from the browser.**

[Quick Start](#quick-start) · [Agent API](#agent-api) · [Deployment Guide for AI](#deployment-guide-for-ai-agents) · [中文文档](README_CN.md)

</div>

---

## Who Is This For?

If you run any of these AI agent systems on a server:

- **[OpenClaw / Moltbot](https://github.com/yzha0302)** — multi-agent collaboration
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — Anthropic's CLI coding agent
- **[Codex](https://github.com/openai/codex)** — OpenAI's autonomous coding agent
- **[Aider](https://github.com/paul-gauthier/aider)** / **[Cursor](https://cursor.sh)** / **[Cline](https://github.com/cline/cline)** — coding assistants
- **Any custom AI agent** — if it can make HTTP requests

Then you need Asyre File.

## The Problem

Your AI agent runs on a server. It's capable — writes code, generates reports, edits documents. But there's a fundamental issue:

**You and the AI can't see the same thing.**

The AI operates on server files; you're on your local machine. Between you is an SSH terminal. To see what the AI wrote, you `cat`. To tell the AI what's wrong, you describe "the second sentence in paragraph three" and pray it understands. To show output to a client, you `scp` the file down and email it.

This back-and-forth happens dozens of times a day. **The AI isn't the bottleneck — the communication channel is.**

### What Asyre File Does

It runs on the same server as your AI agent, opens an HTTP port. You open that URL in your browser and you can:

1. **See everything the AI writes** — real-time, no SSH
2. **Tell the AI exactly what to fix** — select lines 12-18, write "too formal", copy. The copied text automatically includes `/home/ubuntu/data/report.md` — the AI locates the file instantly
3. **Upload local files to the server** — drag into the browser. It's a file transfer hub between your local machine and the server
4. **Share output with clients** — generate a link, they open and view, no signup, no install

**The browser is your control interface. As long as it's open, you and the server AI share the same view of every file.**

```
 ┌────────────────────┐        ┌─────────────────────────────┐
 │  Your Browser       │        │  Server                     │
 │  (Mac/Win/Phone)   │◄──────►│                             │
 │                    │ HTTP   │  ┌──────────┐               │
 │  View AI output     │        │  │Asyre File│◄─ REST API ──►│ AI Agent
 │  Annotate → Copy    │        │  │(port 8765)│               │ (Claude Code /
 │  Upload local files│        │  └──────────┘               │  OpenClaw /
 │  Share with clients│        │       │                     │  Codex / Custom)
 └────────────────────┘        │       ▼                     │
                               │  ~/data/ (shared filesystem) │
 ┌────────────────────┐        │                             │
 │  Your Client        │        └─────────────────────────────┘
 │  (via share link)  │
 │  • Read-only view   │
 │  • Or editable      │
 └────────────────────┘
```

<p align="center">
<img src="docs/assets/dark-mode.png" width="80%" alt="Asyre File">
</p>

## Deployment Guide for AI Agents

> **This section is written for AI agents to read.** If you're using Claude Code, OpenClaw, Codex, or any AI agent, paste this into your agent and ask it to deploy.

### Dear AI Agent: How to Deploy Asyre File

Hello, AI. Here are the steps to deploy Asyre File on a server. Execute in order:

```bash
# 1. Clone the repository
git clone https://github.com/yzha0302/asyre-file.git
cd asyre-file

# 2. Start the server (zero dependencies required)
python3 server.py

# 3. For background operation (recommended)
nohup python3 server.py > asyre.log 2>&1 &

# Or with PM2 (if available)
pm2 start server.py --name asyre-file --interpreter python3
```

After starting, visit `http://<server-ip>:8765`. First visit triggers the setup wizard.

For headless servers (no browser):

```bash
python3 server.py --setup
```

This interactively creates an admin account and (optionally) generates an API token.

### How AI Agents Use the API

With an API token (`asf_<32hex>`), you can:

```bash
# Read a file
curl -H "Authorization: Bearer asf_xxx" http://localhost:8765/api/v1/files/path/to/file.md

# Write a file (create or overwrite)
curl -X PUT -H "Authorization: Bearer asf_xxx" \
  -H "Content-Type: application/json" \
  -d '{"content": "file contents here"}' \
  http://localhost:8765/api/v1/files/path/to/file.md

# List all files
curl -H "Authorization: Bearer asf_xxx" http://localhost:8765/api/v1/files

# Search file contents
curl -H "Authorization: Bearer asf_xxx" http://localhost:8765/api/v1/search?q=keyword

# Delete (moves to trash, recoverable)
curl -X DELETE -H "Authorization: Bearer asf_xxx" http://localhost:8765/api/v1/files/path/to/file.md
```

After deployment, tell the user to visit `http://<server-ip>:8765`.

---

## Core Workflows

### Workflow 1: AI writes files, you review

Your agent writes `reports/weekly.md` via the API. Open the browser — it's in the file tree. Click to see rendered Markdown: headings, lists, code blocks, Mermaid diagrams. All live.

No SSH. No `cat`. No waiting.

### Workflow 2: You spot a problem, give precise feedback

Lines 12-18 are too formal. The old way:

1. SSH into server
2. `cat -n reports/weekly.md | head -20`
3. Copy those lines
4. Paste into AI chat
5. Type "this is from reports/weekly.md lines 12-18, please make it conversational"
6. Hope the AI gets it

**Now:** Select lines 12-18 → write "make it conversational" → click **Copy**. Done.

The copied text includes the full server path:

```markdown
# Annotation: /home/ubuntu/data/reports/weekly.md

Date: 2026-04-05T10:30:00Z
By: Asher

---
**[1] Lines 12-18**
```
The quarterly results demonstrate a significant...
```
Feedback: Too formal. Make it conversational, add specific numbers.
```

Paste into Claude Code, OpenClaw, ChatGPT, or any AI — it sees the full path and knows exactly which file and which lines to modify.

![Annotate lines](docs/assets/annotate-lines.png)

![Copied text includes full server path](docs/assets/annotate-copy.png)

### Workflow 3: Batch review multiple files

Client submitted a batch of documents for AI review? **Cmd+Click** to select files → **Annotate** → write feedback → **Copy** or **Save**.

**Save** persists annotations to the server — your AI agent can read them from `annotations/` and process feedback programmatically.

<p align="center">
<img src="docs/assets/annotate-batch-a.png" width="48%" alt="Batch annotate">
<img src="docs/assets/annotate-batch.png" width="48%" alt="Batch result">
</p>

### Workflow 4: Upload local files to server

You have a document on your laptop that the server AI needs to process?

Drag it onto the browser page. It uploads to the server workspace. The AI agent can read it immediately.

Right-click a folder → **Upload here** for precise placement.

**Asyre File is a bidirectional file transfer hub** between your local machine and the server — no `scp`, no FTP, just drag-and-drop.

### Workflow 5: Share with clients

Right-click → **Share** → choose read-only or editable → copy link.

Client opens the link: clean editor UI, rendered Markdown, no registration, no install. If you gave edit permission, they can modify files directly — you and the AI both see the changes.

![Share link](docs/assets/share-link.png)

## Quick Start

### Option 1: Git Clone (recommended)

```bash
git clone https://github.com/yzha0302/asyre-file.git
cd asyre-file
python3 server.py
```

Visit `http://localhost:8765` — setup wizard creates your admin account.

### Option 2: Docker

```bash
git clone https://github.com/yzha0302/asyre-file.git
cd asyre-file
docker compose up -d
```

### Option 3: One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/yzha0302/asyre-file/main/install.sh | bash
```

## Agent API

### Authentication

Token format: `asf_<32hex>`. Stored as SHA-256 hash — even if the token file is compromised, the original token can't be recovered.

### Endpoints

| Method | Path | Description | Permission |
|--------|------|-------------|-----------|
| GET | `/api/v1/status` | Health check + version | `read` |
| GET | `/api/v1/files` | List all files | `read` |
| GET | `/api/v1/files/{path}` | Read file content | `read` |
| PUT | `/api/v1/files/{path}` | Create or overwrite | `write` |
| POST | `/api/v1/files/{path}/move` | Move or rename | `write` |
| DELETE | `/api/v1/files/{path}` | Delete (trash) | `delete` |
| GET | `/api/v1/search?q=xxx` | Full-text search | `read` |

[Full API Reference →](docs/api.md)

## Features

### Editor
- **20+ languages** with syntax highlighting
- **Live preview** — Mermaid, code blocks, tables
- **Dark & light themes** — editor, preview, diagrams all sync

<p align="center">
<img src="docs/assets/dark-mode.png" width="48%" alt="Dark mode">
<img src="docs/assets/light-mode.png" width="48%" alt="Light mode">
</p>

### File Management
- **File tree** with colored SVG icons by type
- **Drag-and-drop** between folders (with reference warnings)
- **Upload** — sidebar button / drag-to-page / right-click "Upload here"
- **Right-click menu** — Open, Rename, Copy path, Copy link, Download, Select, Delete
- **Cmd/Ctrl+Click multi-select** → batch Annotate, Share, Copy, Delete
- **Search** + **trash with restore**

### Collaboration
- **Three roles** — Admin / Editor / Viewer
- **Path permissions** — scope each user to specific folders
- **Share links** — read-only or editable, files or folders
- **PDF & Word export** with signatures and themes

<p align="center">
<img src="docs/assets/export-pdf.png" width="48%" alt="PDF export">
<img src="docs/assets/export-word.png" width="48%" alt="Word export">
</p>

### AI Collaboration
- **Line-level annotations** — copy with full server paths
- **Batch file annotations** — save for agent consumption
- **REST API** with token auth
- **Activity log** — admin panel
- **Recent files** + **word count / reading time**

## Roles & Permissions

| Action | Admin | Editor | Viewer |
|--------|:-----:|:------:|:------:|
| View files | All | Scoped | Scoped |
| Edit / Save | ✓ | Scoped | — |
| Create / Upload | ✓ | Scoped | — |
| Move / Rename / Delete | ✓ | Scoped | — |
| Drag-and-drop | ✓ | ✓ | — |
| Multi-select ops | ✓ | ✓ | — |
| Share links | ✓ | Scoped | — |
| Empty trash | ✓ | — | — |
| User management | ✓ | — | — |

## Problems We Solved

| Problem | Solution |
|---------|----------|
| Tailwind reset breaks CodeMirror | `.CodeMirror * { box-sizing: content-box !important }` |
| Dark/light needs 3 engines in sync | CSS overrides + JS SVG post-processing |
| Image preview via base64 = 10s load | Direct URL `<img src="/api/raw?path=...">` + cache headers |
| Clipboard API needs HTTPS | `execCommand('copy')` fallback for HTTP |
| Permission checks were frontend-only | Backend role + path + logging on all 7 write endpoints |
| Multipart upload crashed JSON parser | Check Content-Type before `json.loads()` |
| `const` temporal dead zone | Move declarations to top of `<script>` |

## Configuration

```bash
ASF_SERVER_PORT=9000
ASF_WORKSPACE_PATH=/data
ASF_AI_ENABLED=true
ASF_AI_APIKEY=sk-...
```

Or edit `config.json`. Priority: env vars > config.json > defaults.

See [docs/configuration.md](docs/configuration.md).

## Architecture

| Layer | Tech | Why |
|-------|------|-----|
| Backend | Python 3 stdlib | Zero deps, `python3 server.py` anywhere |
| Editor | CodeMirror 5 | CDN, 20+ language modes |
| Preview | marked.js + highlight.js + Mermaid | CDN |
| UI | Tailwind CSS + custom | CDN, no build tools |
| Architecture | Single-file server | One `server.py` = complete deployment |

## Docs

- [API Reference](docs/api.md) · [Configuration](docs/configuration.md) · [Deployment](docs/deployment.md)

## License

[MIT](LICENSE)

---

<div align="center">

Built by [Asyre](https://github.com/yzha0302) for humans who work with AI.

</div>
