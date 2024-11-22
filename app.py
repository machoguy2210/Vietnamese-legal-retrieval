import gradio as gr
from tools import qna, law_conflict


def function1(query):
    return qna(query)

def function2(query):
    return law_conflict(query)

# Hàm xử lý đầu vào dựa trên nút chức năng được chọn
def handle_query(function_choice, query):
    if function_choice == "Hỏi đáp pháp luật":
        return function1(query)
    elif function_choice == "Xác định các luật xung đột":
        return function2(query)

# Tạo giao diện Gradio
iface = gr.Interface(
    fn=handle_query,  # Hàm sẽ được gọi khi nhấn nút 'Submit'
    inputs=[
        gr.Radio(choices=["Hỏi đáp pháp luật", "Xác định các luật xung đột"], label="Chọn chức năng", value="Hỏi đáp pháp luật"),  # Mặc định chọn chức năng 1
        gr.Textbox(label="Nhập câu hỏi")
    ],
    outputs="text",  # Output trả về dạng văn bản
    title="Hệ thống truy xuất thông tin pháp lý",  # Tiêu đề ứng dụng
    description="Chọn chức năng và nhập câu hỏi để truy xuất thông tin pháp lý"  # Mô tả ứng dụng,
)

# Chạy ứng dụng
iface.launch()
