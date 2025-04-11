from agent import create_agent

def main():
    agent = create_agent()
    print("Text-to-SQL Agent is ready. Input your question (type 'exit' or 'quit' to stop):")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = agent.run(user_input)
        print("Result:", result)

if __name__ == "__main__":
    main()
