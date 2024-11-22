import json
import requests
from bs4 import BeautifulSoup
import re

# URL của trang web
url = 'https://thuvienphapluat.vn/van-ban/Giao-duc/Lenh-cong-bo-Luat-giao-duc-quoc-phong-va-an-ninh-nam-2013-197979.aspx'

# Gửi yêu cầu HTTP để lấy nội dung của trang web
response = requests.get(url)
response.encoding = 'utf-8'  # Đảm bảo mã hóa đúng để đọc tiếng Việt

# Phân tích nội dung HTML bằng BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm phần liên kết có chứa "Nội dung"
noi_dung_link = soup.find('a', id='aNoiDungVB')

json_data = {
    "Nội dung": ''
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
        
        # Lệnh
        
        # Lấy tất cả các thẻ <table>
        tables = content1.find_all('table')

        # Kiểm tra nếu có ít nhất 2 thẻ <table>
        if len(tables) >= 2:
            # Lấy nội dung giữa hai thẻ <table> đầu tiên
            
            current = tables[0].next_sibling
            while current and current != tables[1]:
                if current.name == 'p':
                    json_data["Nội dung"] += current.get_text().replace('\n', ' ').replace('\r', '').strip() + ' '
                current = current.next_sibling

        else:
            print("Không tìm thấy đủ 2 thẻ <table> trong nội dung.")
                
                            
                
            
                    
    else:
        print(f"Không tìm thấy mục với id '{target_id}'")
else:
    print("Không tìm thấy liên kết 'Nội dung'")
    
# Xuất đối tượng JSON
json_output = json.dumps(json_data, ensure_ascii=False, indent=4)

with open("output.json", "w", encoding="utf-8") as f:
    f.write(json_output)
