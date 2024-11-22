import json
import requests
from bs4 import BeautifulSoup
import re

# URL của trang web
url = 'https://thuvienphapluat.vn/van-ban/Tien-te-Ngan-hang/Nghi-quyet-148-NQ-CP-2023-tiep-tuc-trien-khai-thi-hanh-Nghi-quyet-42-2017-QH14-579993.aspx?v=tvpl-hdsd-firsr&step=step7#'

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
        
        current_article = None
        current_clause = None
        current_point = None
        
        # Nghị quyết: (Điều, khoản) - (Mục, khoản)
        
        for p_tag in content1.find_all('p'):
            text = p_tag.get_text().replace('\n', ' ').replace('\r', '').strip()
            
            if len(text) == 0:
                continue
            
            a_tag = p_tag.find('a', attrs={'name': True})
            
            if a_tag and (name_attr:=a_tag['name']).startswith('muc_'):
                    article_number = name_attr.split('_')[1]
                    content = text
                    if f"Điều {article_number}" not in json_data:
                        json_data[f"Điều {article_number}"] = {
                            "Nội dung": content
                        }
                        current_article = article_number
                        current_clause = None
                        current_point= None
            elif a_tag and (name_attr:=a_tag['name']).startswith('dieu_'):
                    article_number = name_attr.split('_')[1]
                    content = text
                    json_data[f"Điều {article_number}"] = {
                        "Nội dung": content
                    }
                    current_article = article_number
                    current_clause = None
                    current_point = None
                
            else:
                first_letter = text[0]
                if first_letter.isnumeric():
                    match = re.match(r"(^\d+)[\.|\)]\s(.*)", text)
                    current_clause = match[1]
                    content = text
                    if current_article:
                        json_data[f"Điều {current_article}"][f"Khoản {current_clause}"] = {
                            "Nội dung": content
                        }
                    else:
                        json_data[f"Khoản {current_clause}"] = {
                            "Nội dung": content
                        }
                    current_point = None
                else:
                    match = re.match(r"(^\w)[\.|\)]\s(.*)", text)
                    if match:
                        current_point = match[1]
                        content = text
                        if current_article:
                            if current_clause:
                                json_data[f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] = content
                            else:
                                json_data[f"Điều {current_article}"][f"Điểm {current_point}"] = content
                        else:
                            if current_clause:
                                json_data[f"Khoản {current_clause}"][f"Điểm {current_point}"] = content
                            else:
                                json_data[f"Điểm {current_point}"] = content
                    else:
                        if current_point:
                            if current_article:
                                if current_clause:
                                    json_data[f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                            else:
                                if current_clause:
                                    json_data[f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Điểm {current_point}"] += f" {text}"                            
                        elif current_clause:
                            if current_article:
                                json_data[f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                            else:
                                json_data[f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                        elif current_article:
                            json_data[f"Điều {current_article}"]["Nội dung"] += f" {text}"
            if '/.' in text:
                break
                    
    else:
        print(f"Không tìm thấy mục với id '{target_id}'")
else:
    print("Không tìm thấy liên kết 'Nội dung'")
    
# Xuất đối tượng JSON
json_output = json.dumps(json_data, ensure_ascii=False, indent=4)

with open("output.json", "w", encoding="utf-8") as f:
    f.write(json_output)
