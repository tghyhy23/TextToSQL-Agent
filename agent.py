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
    You are an AI assistant that executes SQL queries based on user questions.

    Here is the actual database structure:

    {schema}

    - DO NOT create new tables
    - Only query existing tables
    - Returns concise results

    Question: {{input}}
    """)

    #Model dùng Ollama local
    llm = ChatOllama(
        model="mistral",
        temperature=0.0,
        base_url="http://localhost:11434/"
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
