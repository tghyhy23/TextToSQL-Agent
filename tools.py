from langchain.tools import Tool
from langchain_community.utilities import SQLDatabase
from db import get_engine

engine = get_engine()
# Tạo đối tượng SQLDatabase dựa vào SQLAlchemy engine
db = SQLDatabase(engine)

def run_query(query: str) -> str:
    try:
        result = db.run(query)
        return str(result)
    except Exception as e:
        return f"Lỗi khi chạy truy vấn: {e}"

def get_db_schema() -> str:
    return db.get_table_info()

sql_tool = Tool(
    name="SQL Query Executor",
    func=run_query,
    description="""
    Dùng để thực thi truy vấn SQL vào bảng 'testing' trong PostgreSQL thật.
    Không được tạo bảng mới. Chỉ được truy vấn dữ liệu có sẵn.
    """
)