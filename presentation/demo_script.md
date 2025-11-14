# Demo Script (5 phút)

1. Khởi động server:
   uvicorn app.main:app --reload

2. Mở Swagger:
   http://localhost:8000/docs

3. Đăng ký agent:
   POST /agents/register

4. Operator login:
   POST /auth/login

5. Tạo task:
   POST /tasks

6. Chạy agent mô phỏng:
   python safe_agent.py

7. Quan sát:
   - Agent nhận task
   - Agent complete
   - Task chuyển trạng thái
   - Audit log ghi lại
   - Metrics tăng số request
