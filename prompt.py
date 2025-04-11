from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("""
You are an AI assistant who queries databases.
DO NOT create new tables. Only use existing tables
Convert the user's request into a valid SQL statement.

User's input: {input}
""")
