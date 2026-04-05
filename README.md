# Asyre File

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/yzha0302/asyre-file)](https://github.com/yzha0302/asyre-file/releases)

**Self-hosted markdown workspace for humans and AI agents.**

A single-file Python web server with a full-featured editor UI — no build step, no Node.js, zero external dependencies for core functionality.

## Features

- **Live Editor** — CodeMirror with syntax highlighting for 20+ languages
- **Markdown Preview** — Real-time rendering with Mermaid diagrams, math, and code highlighting
- **Multi-User Auth** — Admin / Editor / Viewer roles with path-based permissions
- **File Management** — Tree view, drag-and-drop, upload, rename, search, trash & restore
- **Share Links** — Read-only or editable, single file or folder
- **PDF & Word Export** — With custom signatures and themes (optional deps)
- **Annotations** — Line-range comments for review workflows
- **AI Assistant** — Built-in AI editing with Anthropic/OpenAI support
- **Dark & Light Themes** — Full theme support including CodeMirror and Mermaid
- **Agent REST API** — Token-authenticated CRUD for AI agent integration
- **First-Run Wizard** — Web UI or CLI setup, zero manual config needed

## Quick Start

### Option 1: Git Clone (recommended)

```bash
git clone https://github.com/yzha0302/asyre-file.git
cd asyre-file
python3 server.py
```

Visit `http://localhost:8765` — the setup wizard will create your admin account.

### Option 2: One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/yzha0302/asyre-file/main/install.sh | bash
```

### Option 3: Docker

```bash
docker compose up -d
```

Or without compose:

```bash
docker build -t asyre-file .
docker run -d -p 8765:8765 -v ~/asyre-data:/app/data asyre-file
```

## Configuration

Copy `config.example.json` to `config.json` and edit, or use environment variables:

```bash
# Environment variables (override config.json)
ASF_SERVER_PORT=9000
ASF_WORKSPACE_PATH=/path/to/files
ASF_AI_ENABLED=true
ASF_AI_APIKEY=sk-...
```

See [config.example.json](config.example.json) for all options.

## Agent API

Asyre File exposes a REST API for AI agents to read and write files programmatically.

### Generate a Token

During setup, check "Generate API token for agents", or use the CLI:

```bash
python3 server.py --setup
```

### Endpoints

```bash
# Health check
curl -H "Authorization: Bearer asf_xxx" http://localhost:8765/api/v1/status

# List files
curl -H "Authorization: Bearer asf_xxx" http://localhost:8765/api/v1/files

# Read a file
curl -H "Authorization: Bearer asf_xxx" http://localhost:8765/api/v1/files/notes/todo.md

# Create/update a file
curl -X PUT -H "Authorization: Bearer asf_xxx" \
  -H "Content-Type: application/json" \
  -d '{"content": "# Hello\nCreated by agent"}' \
  http://localhost:8765/api/v1/files/notes/new.md

# Search
curl -H "Authorization: Bearer asf_xxx" http://localhost:8765/api/v1/search?q=keyword

# Delete (moves to trash)
curl -X DELETE -H "Authorization: Bearer asf_xxx" \
  http://localhost:8765/api/v1/files/notes/old.md
```

### Permissions

Tokens support granular permissions: `read`, `write`, `delete`.

## Roles & Permissions

| Action | Admin | Editor | Viewer |
|--------|-------|--------|--------|
| View files | All | Scoped paths | Scoped paths |
| Edit / Save | Yes | Scoped | No |
| Create / Upload | Yes | Scoped | No |
| Move / Rename | Yes | Scoped | No |
| Delete (trash) | Yes | Scoped | No |
| Empty trash | Yes | No | No |
| Share links | Yes | Scoped | No |
| User management | Yes | No | No |

## Export (Optional)

PDF and Word export requires additional dependencies:

```bash
pip install weasyprint python-docx
```

The editor works fully without these — export buttons will show an install prompt.

## Tech Stack

- **Backend**: Python 3 stdlib (`http.server`) — zero required dependencies
- **Editor**: CodeMirror 5
- **Preview**: marked.js + highlight.js + Mermaid
- **UI**: Tailwind CSS + DaisyUI (CDN) + custom components
- **Architecture**: Single-file server with inline HTML/CSS/JS

## License

[MIT](LICENSE)
