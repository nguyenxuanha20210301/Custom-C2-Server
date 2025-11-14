# SECURITY Model – SCSF

---

## 1. Authentication
- JWT access token + refresh token
- Hết hạn: 60 phút / 7 ngày
- Token chứa:
  - `sub` = user id
  - `role` = admin/operator/auditor

## 2. RBAC
| Role | Quyền |
|------|-------|
| admin | toàn quyền |
| operator | tạo/cancel task |
| auditor | chỉ xem task |

---

## 3. Mã hóa & lưu mật khẩu
- Hash bằng **argon2**
- Không lưu plaintext password

---

## 4. An toàn payload
- Không cho phép:
  - thực thi lệnh
  - reverse shell
  - chạy script
  - tải file thực thi
- Payload chỉ là **JSON mô phỏng**.

---

## 5. Audit
- Ghi log tất cả action quan trọng:
  - tạo task
  - hủy task
  - đăng nhập
  - upload file

---

## 6. Storage security
- Kiểm tra content-type
- Không lưu `.exe`, `.sh`, `.py`, `.bat`

---

## 7. CI/CD security
- Pinned version
- pytest + flake8
- Không cho phép secret leak

---
