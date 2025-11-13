# API Endpoints (Sketch) — dùng làm base cho OpenAPI

> Lưu ý: Đây chỉ là contract mô tả request/response; không chứa bất kỳ logic nào thực thi mã trên agent.

## Auth
### POST /api/v1/auth/login
- Body: `{ "username": "string", "password": "string" }`
- Response: `{ "access_token": "<jwt>", "refresh_token": "<jwt>", "expires_in": 3600 }`

### POST /api/v1/auth/refresh
- Body: `{ "refresh_token": "string" }`
- Response: `{ "access_token": "...", "expires_in": 3600 }`

## Agents
### POST /api/v1/agents/register
- Body:
```json
{
  "hostname": "agent-host",
  "platform": "linux",
  "tags": ["lab1"],
  "public_key": "optional-base64-or-cert"
}
```
- Response:
```json
{
  "agent_id": "uuid",
  "poll_interval": 60,
  "config": {}
}
```
Notes: public_key optional — if using mTLS or certificate-based auth, include thumbprint.
### POST /api/v1/agents/{agent_id}/heartbeat
- Body: 
```json
{
  "uptime": 12345,
  "load": 0.12,
  "ip": "10.0.0.1",
  "tags": ["lab1"]
}
```
Response: `200 OK`
### GET /api/v1/agents/{agent_id}/tasks
- Query: `?limit=10`
- Response:
```json
[
  {
    "task_id": "uuid",
    "type": "collect-metrics",
    "payload": { "note": "benign descriptor or file_id" },
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```
Notes: payload is descriptor only; do NOT include executable commands.
### POST /api/v1/agents/{agent_id}/upload
- Multipart/form-data with file
- Response: `{ "file_id": "uuid", "url": "signed_url" }`
### GET /api/v1/files/{file_id}
- Auth: operator role required (RBAC)
- Response: file download or 302 -> signed URL
## Tasks (Operator)
### POST /api/v1/tasks
- Body: 
```json
{
  "agent_ids": ["uuid", "uuid"],
  "type": "download-config",
  "meta": { "file_id": "uuid" },
  "expires_in": 3600
}
```
- Response: `{ "task_id": "uuid" }`
## Audit & Logs
### GET /api/v1/audit?agent_id=...&limit=50
- Response: list of audit entries (timestamp, action, actor_id, details)
## Security Notes for Endpoints
- All endpoints enforce TLS.
- Use CSRF protections for UI where applicable.
- Enforce rate-limiting on register & auth endpoints.
- Validate and whitelist uploaded MIME types and size (configurable: `MAX_UPLOAD_MB`).
## Example env vars (placeholders)
- `DATABASE_URL=postgresql://postgres:root@db:5432/customc2` <<THAY_THEO_BAN>>
- `MINIO_ENDPOINT=minio:9000` <<THAY_THEO_BAN>>
- `JWT_SECRET=<32+ char secret>` <<THAY_THEO_BAN>>
- `AGENT_DEFAULT_POLL_SEC=60`
- `MAX_UPLOAD_MB=10`
