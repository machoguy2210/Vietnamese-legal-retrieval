import json
import requests
from bs4 import BeautifulSoup
import re

# URL của trang web
url = 'https://thuvienphapluat.vn/van-ban/Bat-dong-san/Luat-Dat-dai-2024-31-2024-QH15-523642.aspx'

# Gửi yêu cầu HTTP để lấy nội dung của trang web
response = requests.get(url)
response.encoding = 'utf-8'  # Đảm bảo mã hóa đúng để đọc tiếng Việt

# Phân tích nội dung HTML bằng BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm phần liên kết có chứa "Nội dung"
noi_dung_link = soup.find('a', id='aNoiDungVB')

json_data = {
    "Nội dung": ""
}

# Nếu tìm thấy liên kết "Nội dung", trích xuất phần liên quan
if noi_dung_link:
    # Lấy id của mục mà liên kết này trỏ tới (tab1)
    target_id = noi_dung_link['href'].replace('#', '')

    # Tìm phần tử có id bằng với target_id
    content_div = soup.find(id=target_id)
    
    # Trích xuất nội dung có class="content1"
    if content_div:
        content1 = content_div.find(class_='content1')
        
        if content1:
                        
            # Khởi tạo các biến để theo dõi chương và điều hiện tại
            current_chapter = None
            current_article = None
            current_clause = None
            current_point = None
            quotation_marks = False
            

            # Lặp qua tất cả các thẻ <p> để xử lý nội dung
            for p_tag in content1.find_all('p'):
                text = p_tag.get_text().replace('\n', ' ').replace('\r', '').strip()
                
                if len(text) == 0:
                    continue
                
                a_tag = p_tag.find('a', attrs={'name': True})
                
                if a_tag and (name_attr:=a_tag['name']).startswith('chuong_'):
                    if 'p' in name_attr:
                        break
                    if '_name' not in name_attr:
                        chapter_number = name_attr.split('_')[1]
                        content = text
                        json_data[f"Chương {chapter_number}"] = {
                            "Nội dung": content
                        }
                        current_chapter = chapter_number
                        current_article = None
                        current_clause = None
                        current_point = None
                    else:
                        chapter_name = name_attr.split('_')[1]
                        content = text
                        json_data[f"Chương {chapter_number}"]["Nội dung"] += f" {content}"
                elif a_tag and (name_attr:=a_tag['name']).startswith('muc_'):
                    article_number = name_attr.split('_')[1]
                    content = text
                    insertion = False
                    if current_chapter and f"Điều {article_number}" not in json_data[f"Chương {current_chapter}"]:
                        json_data[f"Chương {current_chapter}"][f"Điều {article_number}"] = {
                            "Nội dung": content
                        }
                        insertion = True
                    elif f"Điều {article_number}" not in json_data:
                        json_data[f"Điều {article_number}"] = {
                            "Nội dung": content
                        }
                        insertion = True
                    if insertion:
                        current_article = article_number
                        current_clause = None
                        current_point = None
                elif a_tag and (name_attr:=a_tag['name']).startswith('dieu_'):
                    article_number = name_attr.split('_')[1]
                    content = text
                    if current_chapter:
                        json_data[f"Chương {current_chapter}"][f"Điều {article_number}"] = {
                            "Nội dung": content
                        }
                    else:
                        json_data[f"Điều {article_number}"] = {
                            "Nội dung": content
                        }
                    current_article = article_number
                    current_clause = None
                    current_point = None
                else:
                    if not quotation_marks:
                        first_letter = text[0]
                        if first_letter == '“' or first_letter == '"':
                            quotation_marks = True
                            if current_point:
                                if current_clause:
                                    if current_article:
                                        if current_chapter:
                                            json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                        else:
                                            json_data[f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                elif current_article:
                                    if current_chapter:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                            elif current_clause:
                                if current_article:
                                    if current_chapter:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                                    else:
                                        json_data[f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                            elif current_article:
                                if current_chapter:
                                    json_data[f"Chương {current_chapter}"][f"Điều {current_article}"]["Nội dung"] += f" {text}"
                                else:
                                    json_data[f"Điều {current_article}"]["Nội dung"] += f" {text}"
                            if text.find('”') != -1 or (text.find('\"') != 0 and text.find('\"') != -1):
                                quotation_marks = False
                        elif first_letter.isnumeric():
                            match = re.match(r"(^\d+)[\.|\)]\s(.*)", text)
                            content = text
                            if match:
                                current_clause = match[1]      
                                if current_article:
                                    if current_chapter:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"] = { 
                                            "Nội dung": content 
                                        }
                                    else:
                                        json_data[f"Điều {current_article}"][f"Khoản {current_clause}"] = { 
                                            "Nội dung": content 
                                        }
                                current_point = None                                
                            else:
                                if current_point:
                                    if current_clause:
                                        if current_article:
                                            if current_chapter:
                                                json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                            else:
                                                json_data[f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                    elif current_article:
                                        if current_chapter:
                                            json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                        else:
                                            json_data[f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                elif current_article:
                                    if current_chapter:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                                    else:
                                        json_data[f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                        else:
                            match = re.match(r"(^\w)[\.|\)]\s(.*)", text)
                            content = text
                            if match:
                                current_point = match[1]
                                if current_clause:
                                    if current_article:
                                        if current_chapter:
                                            json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] = content
                                        else:
                                            json_data[f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] = content
                                elif current_article:
                                    if current_chapter:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Điểm {current_point}"] = content
                                        print(f"Chương {current_chapter} Điều {current_article} Điểm {current_point}")
                                    else:
                                        json_data[f"Điều {current_article}"][f"Điểm {current_point}"] = content
                                        print(f"Điều {current_article} Điểm {current_point}")
                            else:
                                if current_point:
                                    if current_clause:
                                        if current_article:
                                            if current_chapter:
                                                json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                            else:
                                                json_data[f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                    elif current_article:
                                        if current_chapter:
                                            json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                        else:
                                            json_data[f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                elif current_clause:
                                    if current_article:
                                        if current_chapter:
                                            json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                                        else:
                                            json_data[f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                                elif current_article:
                                    if current_chapter:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"]["Nội dung"] += f" {text}"
                                    else:
                                        json_data[f"Điều {current_article}"]["Nội dung"] += f" {text}"
                    else:
                        if current_point:
                            if current_clause:
                                if current_article:
                                    if current_chapter:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                            elif current_article:
                                if current_chapter:
                                    json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                        elif current_clause:
                            if current_article:
                                if current_chapter:
                                    json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                                else:
                                    json_data[f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                        elif current_article:
                            if current_chapter:
                                json_data[f"Chương {current_chapter}"][f"Điều {current_article}"]["Nội dung"] += f" {text}"
                            else:
                                json_data[f"Điều {current_article}"]["Nội dung"] += f" {text}"
                        if text.find('”') != -1 or (text.find('\"') != 0 and text.find('\"') != -1):
                            quotation_marks = False
                if '/.' in text:
                    break
                
        else:
            print("Không tìm thấy phần tử với class 'content1'")
    else:
        print(f"Không tìm thấy mục với id '{target_id}'")
else:
    print("Không tìm thấy liên kết 'Nội dung'")
    
# Xuất đối tượng JSON
json_output = json.dumps(json_data, ensure_ascii=False, indent=4)

with open("output.json", "w", encoding="utf-8") as f:
    f.write(json_output)
