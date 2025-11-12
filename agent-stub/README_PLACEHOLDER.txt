=== AGENT STUB - PLACEHOLDER ===

WARNING: This agent stub intentionally contains NO remote-execution logic and NO payloads.
Nó chỉ dùng để:
 - Đăng ký (register) với server (metadata)
 - Gửi heartbeat định kỳ
 - Tải lên/tải xuống file MẪU (chỉ tài liệu/test)

Mục đích: cho phép bạn test luồng đăng ký/heartbeat/task retrieval/file transfer
MỌI logic thực thi lệnh (ví dụ chạy lệnh từ server) phải do bạn tự thêm trong môi trường LAB riêng, offline,
và **KHÔNG** được commit lên repository công khai.

File chính: `agent.py` (skeleton). Tại chỗ `AGENT_TASK_HANDLER_PLACEHOLDER` bạn có thể thêm behavior khi offline.
