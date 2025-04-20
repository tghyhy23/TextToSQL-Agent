# main.py
from agent import generate_sql, create_agent
from tools import sql_tool

def main():
    print("\n🤖 Text-to-SQL Agent 2-Stage (Groq + Mixtral) is ready.")
    print("Type your question (or 'exit' to stop):")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        print("\n🧠 Generating SQL using ChatGroq...")
        sql_response = generate_sql(user_input)
        sql_query = sql_response

        print("\n📜 SQL Generated:\n", sql_query)

        print("\n📊 Running SQL and generating explanation using Mixtral (Ollama)...")
        sql_result = sql_tool.run(sql_query)

        agent = create_agent(sql_query, user_input, sql_result)
        result = agent.invoke({"input": user_input})

        print("\n💬 Result:", result)


if __name__ == "__main__":
    main()