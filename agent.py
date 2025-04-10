import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from tools import sql_tool, get_db_schema

load_dotenv()

def create_agent():
    schema = get_db_schema()

    prompt_template = PromptTemplate.from_template(f"""
    Bạn là trợ lý AI chuyên thực thi truy vấn SQL dựa trên câu hỏi của người dùng.

    Dưới đây là cấu trúc CSDL thực tế:

    {schema}

    - KHÔNG được tạo bảng mới
    - Chỉ được truy vấn các bảng đã tồn tại
    - Trả kết quả ngắn gọn bằng tiếng Việt

    Câu hỏi: {{input}}
    """)

    #Model dùng Ollama local
    llm = ChatOllama(
        model="your model",
        temperature=0.0,
        base_url="your url"
    )

    tools = [sql_tool]

    #Khởi tạo Agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={"prefix": prompt_template.template}
    )
    return agent
