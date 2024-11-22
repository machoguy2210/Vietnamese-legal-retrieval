from hugchat import hugchat
from hugchat.login import Login
import json
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

cookie_path_dir = "./cookies/"

sign = Login(EMAIL, PASSWORD)

cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

system_prompt = '''You are an advanced legal query generator with specialized skills in analyzing legal documents. When provided with an excerpt from a legal document, your task is to identify from 1 to 5 critical aspects or implications that might interest or impact the readers. These aspects should address various dimensions of the content, focusing on rights, obligations, potential legal issues, or general legal awareness, exclusively within provided grounded content. Do not consider information in document's source for this analysis. 
For each identified critical aspect, generate a single question. These questions should reflect plausible inquiries that an average citizen might have, relating directly to the document but formulated in a manner accessible to someone unfamiliar with the presence of the legal text or information being asked about. Phrase the questions as if coming from a person who has not read or seen the legal text ever.
Your output should be in JSON format, listing the critical aspects identified and a corresponding question for each aspect.0 Please adhere to the following guidelines for creating questions:
            -    Think creatively about real-world scenarios and edge cases the law might apply to, phrase it naturally as if asked by an average citizen.
            -    The queries should be ones that could reasonably be answered by the information exclusively within provided grounded content only. Do not ask information in document's source.
            -    Each query should be one sentence only and its length is no more than 120 words.
            -    Try to phrase each of the questions as detailed as possible, as if you haven't never seen the legal text and are trying to look for it using keywords in the question, you may need to include details in document's source and domain for this aim. You should not quote the exact legal text code (like 02/2017/TT-BQP). The better way is to include information on the content of document as in document's source instead like the executive body published the document (e.g. "Bộ Y tế quy định thế nào về ..."). In the case you have to refer to the legal text, use words like: "Quy định pháp luật", "Pháp luật", "Luật". Don't use the word "này".
            -    Present your analysis and questions in Vietnamese. 
            ...
            Structure your output in the JSON format below:
            ```
            {
            "aspects": [
                [Brief description of the aspect 1],
                [Brief description of the aspect 2],
                ...
            ],
            "questions": [
                [Your question related to aspect 1 of the legal text],
                [Your question related to aspect 2 of the legal text],
                ...
            ]
            }
            ```
            Ensure to replace the placeholders with actual analysis and questions based on the legal text provided, and in Vietnamese. Answer with the JSON and nothing else.'''

def response(document):
    
    # chatbot.new_conversation(switch_to=True, system_prompt=system_prompt)
    
    chatbot.new_conversation(switch_to=True)   

    # document = document

    # message = "The following is the mentioned excerpt:\n" + document

    half1_message = '''You are an advanced legal query generator with specialized skills in analyzing legal documents. When provided with an excerpt from a legal document, your task is to identify 1 - 5 critical aspects or implications that might interest or impact the readers. These aspects should address various dimensions of the content, focusing on rights, obligations, potential legal issues, or general legal awareness, exclusively within provided grounded content. Do not consider information in document's source for this analysis.
The following is the mentioned excerpt:'''

    half2_message = '''...
For each identified critical aspect, generate a single question. These questions should reflect plausible inquiries that an average citizen might have, relating directly to the document but formulated in a manner accessible to someone unfamiliar with the presence of the legal text or information being asked about. Phrase the questions as if coming from a layperson who has not read or seen the legal text ever.
Your output should be in JSON format, listing the critical aspects identified and a corresponding question for each aspect. Please adhere to the following guidelines for creating questions:
-    Think creatively about real-world scenarios and edge cases the law might apply to, phrase it naturally as if asked by an average citizen.
-    The queries should be ones that could reasonably be answered by the information exclusively within provided grounded content only. Do not ask information in document's source.
-    Each query should be one sentence only and its length is no more than 120 words.
-    Try to phrase each of the questions as detailed as possible, as if you haven't never seen the legal text and are trying to look for it using keywords in the question, you may need to include details in document's source and domain for this aim. You should not quote the exact legal text code (like 02/2017/TT-BQP). The better way is to include information on the content of document as in document's source instead like the executive body published the document (e.g. "Bộ Y tế quy định thế nào về ..."). In the case you have to refer to the legal text, use words like: "Quy định pháp luật", "Pháp luật", "Luật". Don't use the word "này".
-    Present your analysis and questions in Vietnamese. 
...
Structure your output in the JSON format below:
```
{
"aspects": [
    [Brief description of the aspect 1],
    [Brief description of the aspect 2],
    ...
],
"questions": [
    [Your question related to aspect 1 of the legal text],
    [Your question related to aspect 2 of the legal text],
    ...
]
}
```
Ensure to replace the placeholders with actual analysis and questions based on the legal text provided, and in Vietnamese. Answer with the JSON and nothing else.'''
                
    message = half1_message + '\n\'\'\'' + document + '\'\'\'\n' + half2_message
    
    message_result = chatbot.chat(message)
    
    message_result.wait_until_done()

    return message_result

# models = chatbot.active_model

# print(models)

def clear_conversation():
    chatbot.delete_all_conversations()
    
# def answer(document, query):
    
#     chatbot.new_conversation(switch_to=True)
    
#     message = f'Use only the following pieces of retrieved context to answer the question. If you don\'t have enough information to answer the question, please respond with "I don\'t have enough information to answer the question." and do not try to make up an answer.\nQuestion: {query}\n Context:\n{document} \n Useful answer: '
    
#     message_result = chatbot.chat(message)
#     message_result.wait_until_done()
#     return message_result

def answer(document, query):
    import google.generativeai as genai

    genai.configure(api_key="YOUR_API_KEY")

    model = genai.GenerativeModel("gemini-1.5-flash")

    new_chat = model.start_chat()

    response = new_chat.send_message(f'''Chỉ sử dụng các đoạn văn bản bên dưới để trả lời câu hỏi và không sử dụng kiến thức sẵn có của bạn. Hãy trả lời chi tiết nhất có thể. Nếu bạn không có đủ thông tin cần thiết từ các đoạn văn bản, hãy trả lời bằng "Tôi không có đủ thông tin để trả lời câu hỏi".
    Câu hỏi: {query}
    Các đoạn văn:
    {document}
    Câu trả lời:''')
    
    return response.text



def refine(document, query, prev_ans):
    
    message = f'The original query is as follows: {query} \n We have provided an existing answer: {prev_ans} \n We have the opportunity to refine the existing answer (only if needed) with some more context below: \n _______________ \n {document} \n _______________ \n Given the new context, refine the original answer to better answer the query. Output the refined answer ONLY without any notes. If the context isn\'t useful, return the original answer ONLY without any notes. \n Refined answer: '
    
    message_result = chatbot.chat(message)
    
    message_result.wait_until_done()
    
    return message_result

def chat_with_model(document):
    
    chatbot.new_conversation(switch_to=True)
    
    
    message = f'''You are a legal aspect analyst with specialized skills in analyzing legal documents. When provided with an excerpt from a legal document, your task is to identify 1 to 2 critical aspects or implications that represent the main content of the excerpt. These aspects should focus on rights, obligations, potential legal issues, or general legal awareness, exclusively based on the provided content. Do not consider information from the source of the document for this analysis.
The following is the mentioned excerpt:
{document}

Your output should be in JSON format, listing the critical aspects identified. Please adhere to the following guidelines for identifying aspects:

-   Each aspect should be one sentence only and no longer than 120 words.
-   Do not quote the exact legal text code (like 02/2017/TT-BQP). Instead, use information about the content as in the document's source (e.g., "Bộ Y tế quy định thế nào về ..."). If you must refer to the legal text, use terms like: "Quy định pháp luật," "Pháp luật," or "Luật." Do not use the word "này."
-   Present your analysis and questions in Vietnamese.''' + '''

Structure your output in the JSON format below:

```
{
"aspects": [
    [Brief description of aspect 1],
    [Brief description of aspect 2],
    ...
]
}
```
Ensure to replace the placeholders with actual analysis based on the legal text provided, and in Vietnamese. Answer with the JSON and nothing else.'''
    
    message_result = chatbot.chat(message)
    
    message_result.wait_until_done()
    
    return str(message_result)

def check_conflict(context, document):
    
    chatbot.new_conversation(switch_to=True)
    
    message = f'''You are a legal expert. Your task is to check whether the source document has any legal conflicts with the list of potential conflict documents.

Input: A source document and a list of potential conflict documents.
Output: A list of documents that have legal conflicts with the source document, with each document separated by "______________". If no conflicts are found, return "No conflicts found."
Source document: {document}

List of potential conflict documents: {context}'''
    
    message_result = chatbot.chat(message)
    
    message_result.wait_until_done()
    
    return message_result
    
    

if __name__ == '__main__':

    clear_conversation()
