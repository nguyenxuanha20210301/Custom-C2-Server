# Security Notes (tóm tắt)

- Không commit secrets vào repo. Dùng GitHub Secrets / Vault.
- TLS mandatory between clients & server.
- Xác thực: JWT hoặc OAuth2/OIDC; implement RBAC.
- Rate limiting: ingress/nginx hoặc API gateway.
- Container hardening: non-root user, minimal base image, scan images (Trivy).
- K8s: Pod Security, Network Policies, Resource limits.
- Logging: centralize (ELK/Loki), audit logs immutable.
