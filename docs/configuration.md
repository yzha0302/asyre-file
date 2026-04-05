# Configuration

Asyre File uses a three-layer configuration system:

1. **Built-in defaults** (in `config.py`)
2. **`config.json`** file overrides
3. **`ASF_*` environment variables** override everything

## config.json

Copy `config.example.json` to `config.json`:

```json
{
  "server": {"host": "0.0.0.0", "port": 8765},
  "site": {"name": "Asyre File"},
  "workspace": {"path": "./data", "max_upload_mb": 50},
  "auth": {"session_timeout_hours": 72, "allow_registration": false},
  "ai": {"enabled": false, "provider": "anthropic", "api_key": "", "model": "claude-sonnet-4-5-20250514"},
  "export": {"pdf_enabled": true, "word_enabled": true},
  "api": {"enabled": true}
}
```

## Environment Variables

Format: `ASF_SECTION_KEY=value`

| Variable | Default | Description |
|----------|---------|-------------|
| `ASF_SERVER_PORT` | 8765 | Server port |
| `ASF_SERVER_HOST` | 0.0.0.0 | Bind address |
| `ASF_WORKSPACE_PATH` | ./data | File storage directory |
| `ASF_AI_ENABLED` | false | Enable AI assistant |
| `ASF_AI_APIKEY` | | API key for AI provider |
| `ASF_AUTH_SESSIONTIMEOUTHOURS` | 72 | Session expiry |

## Data Files

These files are created automatically and should NOT be committed to git:

| File | Purpose |
|------|---------|
| `users.json` | User accounts and credentials |
| `config.json` | Your configuration |
| `api_tokens.json` | Agent API tokens (hashed) |
| `.sessions.json` | Active login sessions |
| `activity.jsonl` | Activity audit log |
| `data/` | Workspace files |
| `avatars/` | User avatar images |
