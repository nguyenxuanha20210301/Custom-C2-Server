import os
import sys
from pathlib import Path

# *** Bật chế độ test / disable auth ***
# conftest được load TRƯỚC khi import app, nên set env ở đây là chuẩn
os.environ.setdefault("AUTH_DISABLED", "true")
os.environ.setdefault("ENVIRONMENT", "test")

# Nếu bạn muốn test dùng sqlite file dev.db, có thể bỏ qua DATABASE_URL.
# Nếu sau này muốn dùng DB riêng cho test thì set thêm biến này:
# os.environ.setdefault("DATABASE_URL", "sqlite:///./dev.db")

# *** Thêm server/src vào sys.path để import app ***
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "server" / "src"

src_str = str(SRC)
if src_str not in sys.path:
    sys.path.insert(0, src_str)
