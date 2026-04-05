# Agent REST API

Asyre File provides a REST API for AI agents to interact with the workspace programmatically.

## Authentication

All API requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer asf_<32hex>
```

Tokens are generated during setup or via `python3 server.py --setup`.

## Endpoints

### GET /api/v1/status

Health check and version info.

**Response:**
```json
{"ok": true, "version": "1.0.0", "name": "Asyre File"}
```

### GET /api/v1/files

List all files in the workspace.

**Query params:** `dir` (optional) — filter to a subdirectory.

**Response:**
```json
{
  "ok": true,
  "files": [
    {"path": "notes/todo.md", "size": 1234, "modified": 1712345678}
  ],
  "count": 1
}
```

### GET /api/v1/files/{path}

Read file content.

**Response:**
```json
{"ok": true, "path": "notes/todo.md", "content": "# Todo\n...", "size": 1234}
```

### PUT /api/v1/files/{path}

Create or overwrite a file.

**Body:**
```json
{"content": "# New File\nCreated by agent."}
```

### DELETE /api/v1/files/{path}

Move file to trash.

### POST /api/v1/files/{path}/move

Rename or move a file.

**Body:**
```json
{"to": "new/path/file.md"}
```

### GET /api/v1/search?q={query}

Full-text search across the workspace. Minimum 2 characters.

**Response:**
```json
{
  "ok": true,
  "results": [
    {"path": "notes/todo.md", "match": "content", "snippet": "...keyword..."}
  ],
  "count": 1
}
```

## Token Permissions

Each token has a set of permissions: `read`, `write`, `delete`.

- `read` — list files, read content, search
- `write` — create, update, move/rename files
- `delete` — move files to trash

## Error Responses

```json
{"ok": false, "error": "description"}
```

HTTP status codes: 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found).
