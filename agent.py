import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq  # Groq-powered LLM
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOllama
from prompt import sql_prompt_template, explain_prompt_template
from tools import sql_tool

load_dotenv()

def generate_sql(user_input):
    llm_groq = ChatGroq(
        temperature=0.0,
        model="llama3-70b-81922",
        api_key=os.getenv("GROQ_API_KEY")
    )
    chain = sql_prompt_template | llm_groq
    sql_result = chain.invoke({"input": user_input})
    return sql_result.content

def create_agent(sql_query, user_question, sql_result):
    formatted_prompt = explain_prompt_template.template.format(
        input=user_question,
        sql_query=sql_query,
        sql_result=sql_result
    )

    llm = ChatOllama(
        model="mistral",
        temperature=0.0,
        base_url="http://localhost:11434/"
    )

    agent = initialize_agent(
        tools=[sql_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={"prefix": formatted_prompt},
        handle_parsing_errors=True
    )
    return agent