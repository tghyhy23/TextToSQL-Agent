from langchain.prompts import PromptTemplate
from tools import get_db_schema

# Get live database schema for accurate prompting
schema = get_db_schema()

# Prompt for SQL generation (used with Groq/ChatGroq)
sql_prompt_template = PromptTemplate.from_template(f"""
You are a PostgreSQL expert with a strong attention to detail.

You can define PostgreSQL queries, analyze query results, and interpret them to answer user questions.

Constraints:
- NEVER use SELECT * (only select relevant columns).
- DO NOT create or alter tables.
- Use only tables and columns listed in the schema.
- Return only the SQL query and nothing else.

Schema:
{schema}

User's input: {{input}}
""")

# Prompt for SQL explanation (used with Mixtral/Ollama)
explain_prompt_template = PromptTemplate.from_template("""
You are an AI assistant that helps users understand SQL query results.

This is the executed SQL query:
{sql_query}

Respond in clear, natural language based on the SQL output.

User's question: {input}
""")
