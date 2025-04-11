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
        return f"Error: {e}"

def get_db_schema() -> str:
    return db.get_table_info()

sql_tool = Tool(
    name="SQL Query Executor",
    func=run_query,
    description="""
    Used to execute SQL queries on the table in real PostgreSQL.
    Do not create new tables. Only query existing data.
    """
)