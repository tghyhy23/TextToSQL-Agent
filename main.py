from agent import create_agent

def main():
    agent = create_agent()
    print("Text-to-SQL Agent đã khởi tạo. Nhập câu hỏi (gõ 'exit' hoặc 'quit' để dừng):")
    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = agent.run(user_input)
        print("Kết quả:", result)

if __name__ == "__main__":
    main()
