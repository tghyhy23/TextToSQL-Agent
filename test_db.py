from db import get_engine
from sqlalchemy import text  # << thêm dòng này

engine = get_engine()

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = result.fetchall()
        print("✅ Kết nối thành công! Danh sách bảng:")
        for table in tables:
            print("-", table[0])
except Exception as e:
    print("❌ Kết nối thất bại:", e)
