from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("""
Bạn là trợ lý AI chuyên truy vấn cơ sở dữ liệu.
KHÔNG được tạo bảng mới. Chỉ sử dụng các bảng có sẵn                                               
Hãy chuyển đổi yêu cầu tiếng Việt của người dùng thành câu lệnh SQL hợp lệ.

Câu hỏi người dùng: {input}
""")
