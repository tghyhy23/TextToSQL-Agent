import json
import sys
from collections import defaultdict
from datetime import datetime
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field
from typing_extensions import Annotated, TypedDict
import faiss

sys.path.append('.')

from src.db.postgres_helper import db
from src.prompts.data_info_prompt import (DATA_FIELDS_MEANING, RELEVANT_DATA_PROMPT)
from src.prompts.gen_code_prompt import CODE_GEN_PROMPT
from src.prompts.sql_agent_prompt import SQL_QUERY_GEN_PROMPT
from src.prompts.question_breakdown import QUESTION_BREAKDOWN_EXAMPLES
from src.utils.llm_helper import (State, convert_string_table_to_markdown, get_explanation,
                                  get_llm_model, preprocess_code, merge_query_descriptions)


# ------------------------------
# Section: SQL Agent
# ------------------------------

class SQLOutput(TypedDict):
    query: str = Field(description="SQL Query")


def sql_gen_agent(state: State):
    print('Starting sql gen')
    relevant_data = []
    llm = get_llm_model(provider='gpt')
    structured_llm = llm.with_structured_output(SQLOutput)
    print(state["steps"])
    for step in state['steps']:
        # if step['data_name'] != "diagram_plan":
        if step['data_name'] in ["train_movement_report", "penalty", "train_config"]:
            human = f"""Given the question: {state['question']}."""
            # print("Query description:", step['query_description'])
            # You must generate SQL query given query description: {step['query_description']}.\n
            system = f"""{SQL_QUERY_GEN_PROMPT}
            
            Only query from table {step['data_name']} with these fields: \n
            {DATA_FIELDS_MEANING.get(step['data_name'])}. Limit your query to 50 rows.
            """.replace('}', '}}').replace('{', '{{')
            sql_gen_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system),
                    ("human", human),
                ]
            )
            sql_gen_model = sql_gen_prompt | structured_llm
            result = sql_gen_model.invoke({})
            print("SQL Query:", result)
            if result != None:

                query = result.get("query")
                # query_description = step['query_description']

                raw_result = db.run_no_throw(query, include_columns=True)
                if "error" in raw_result:
                    query_result = str("Error occurred. Please ask again")
                    query_error = True
                    print(f"Error occurred: {raw_result}")
                elif raw_result == '':
                    query_result = "Query ran successfully, no record found"
                    query_error = False

                else:
                    query_result = raw_result
                    query_result = convert_string_table_to_markdown(raw_result)
                    # query_result = convert_string_table_to_list(raw_result)

                    print("Query Output:\n", query_result)
                    query_error = False
            else:
                query = ""
                query_result = str("No query returned.")
                query_error = True

            relevant_data.append({#'query_description': query_description,
                                  'query_result': query_result,
                                  'query_error': query_error,
                                  'query': query
                                  })
    return {'relevant_data': relevant_data}



