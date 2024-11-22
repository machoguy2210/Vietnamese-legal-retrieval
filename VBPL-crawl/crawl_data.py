import requests
import re
from bs4 import BeautifulSoup
import json


def crawl_data(url):
    
    response = requests.get(url)
    response.encoding = 'utf-8'
    
    json_data = {
        "number": "",
        "metadata": "Còn hiệu lực",
        "lawid": "",
        "Tiêu đề": ""
    }
    
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find('div', id='toanvancontent')   
    
    table_found = False   
    
    try:
        metadata = soup.find('div', class_='fulltext')
        table = metadata.find('table')
        table_found = True
    except:
        print("Không tìm thấy bảng số hiệu")

    if content:
        
        current_chapter = None
        current_article = None
        current_clause = None
        current_point = None
        quotation_mark = False
        insert_to_title = True
        
        temp_chapter = None
        temp_article = None
        temp_clause = None
        temp_point = None
        
        try:
            if table_found:
                for div_tag in table.find_all('div'):
                    text = div_tag.get_text(strip=True).strip()        
                    if (match := re.match(r"Số:\s*(.*)", text)):
                        json_data["lawid"] += match[1]
                        break
        except:
            pass
            
            
        for p_tag in content.find_all('p'):
            text = p_tag.get_text().strip()
            
            if len(text) == 0:
                continue
            
            chuong = r"^Chương\s+\b(?!trình\b)(\w+)"
            dieu = r"^Điều\s(\d+)"
            khoan = r"(^\d+)[\.|\)]\s(.*)"
            diem = r"(^\w)[\.|\)]\s(.*)"
            
            if insert_to_title:
                strong_tag = p_tag.find('strong')
                if strong_tag:
                    if not re.match(chuong, text) and not re.match(dieu, text):
                        json_data["Tiêu đề"] += f" {text}"
                        continue
                    else:
                        insert_to_title = False
                else:
                    insert_to_title = False
            try:
                if not quotation_mark:
                    if (match := re.match(chuong, text)):
                        current_chapter = match[1]
                        content = text
                        json_data[f"Chương {current_chapter}"] = {
                            "Tiêu đề": content
                        }
                        current_article = None
                        current_clause = None
                        current_point = None
                    elif (match := re.match(dieu, text)):
                        current_article = match[1]
                        content = text
                        if current_chapter:
                            json_data[f"Chương {current_chapter}"][f"Điều {current_article}"] = {
                                "Tiêu đề": content,
                                "Nội dung": ""
                            }
                        else:
                            json_data[f"Điều {current_article}"] = {
                                "Tiêu đề": content,
                                "Nội dung": ""
                            }
                        current_clause = None
                        current_point = None
                    elif (match := re.match(khoan, text)):
                        current_clause = match[1]
                        content = text
                        if current_chapter:
                            if current_article:
                                json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"] = {
                                    "Nội dung": content
                                }
                            else:
                                json_data[f"Chương {current_chapter}"][f"Khoản {current_clause}"] = {
                                    "Nội dung": content
                                }
                        else:
                            if current_article:
                                json_data[f"Điều {current_article}"][f"Khoản {current_clause}"] = {
                                    "Nội dung": content
                                }
                            else:
                                json_data[f"Khoản {current_clause}"] = {
                                    "Nội dung": content
                                }
                        current_point = None
                    elif (match := re.match(diem, text)):
                        current_point = match[1]
                        content = text
                        if current_chapter:
                            if current_article:
                                if current_clause:
                                    json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] = content
                                else:
                                    json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Điểm {current_point}"] = content
                            else:
                                if current_clause:
                                    json_data[f"Chương {current_chapter}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] = content
                                else:
                                    json_data[f"Chương {current_chapter}"][f"Điểm {current_point}"] = content
                        else:
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
                        if strong_tag := p_tag.find('strong'):
                            if strong_tag.get_text().strip() == text:
                                if current_article or current_clause:
                                    continue
                                else:
                                    if current_chapter:
                                        json_data[f"Chương {current_chapter}"]["Tiêu đề"] += f" {text}"
                                        continue          
                                    
                        if current_chapter:
                            if current_article:
                                if current_clause:
                                    if current_point:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                                else:
                                    if current_point:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Chương {current_chapter}"][f"Điều {current_article}"]["Nội dung"] += f" {text}"
                            else:
                                if current_clause:
                                    if current_point:
                                        json_data[f"Chương {current_chapter}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Chương {current_chapter}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                                else:
                                    if current_point:
                                        json_data[f"Chương {current_chapter}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Chương {current_chapter}"]["Tiêu đề"] += f" {text}"
                        else:
                            if current_article:
                                if current_clause:
                                    if current_point:
                                        json_data[f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                                else:
                                    if current_point:
                                        json_data[f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Điều {current_article}"]["Nội dung"] += f" {text}"
                            else:
                                if current_clause:
                                    if current_point:
                                        json_data[f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                    else:
                                        json_data[f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                                else:
                                    if current_point:
                                        json_data[f"Điểm {current_point}"] += f" {text}"
                        if text[0] == '“' or text[0] == '"':
                            quotation_mark = True
                else:
                    if current_chapter:
                        if current_article:
                            if current_clause:
                                if current_point:
                                    json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                            else:
                                if current_point:
                                    json_data[f"Chương {current_chapter}"][f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Chương {current_chapter}"][f"Điều {current_article}"]["Nội dung"] += f" {text}"
                        else:
                            if current_clause:
                                if current_point:
                                    json_data[f"Chương {current_chapter}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Chương {current_chapter}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                            else:
                                if current_point:
                                    json_data[f"Chương {current_chapter}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Chương {current_chapter}"]["Tiêu đề"] += f" {text}"
                    else:
                        if current_article:
                            if current_clause:
                                if current_point:
                                    json_data[f"Điều {current_article}"][f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Điều {current_article}"][f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                            else:
                                if current_point:
                                    json_data[f"Điều {current_article}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Điều {current_article}"]["Nội dung"] += f" {text}"
                        else:
                            if current_clause:
                                if current_point:
                                    json_data[f"Khoản {current_clause}"][f"Điểm {current_point}"] += f" {text}"
                                else:
                                    json_data[f"Khoản {current_clause}"]["Nội dung"] += f" {text}"
                            else:
                                if current_point:
                                    json_data[f"Điểm {current_point}"] += f" {text}"
                        
                
                if text.find('”') != -1 or (text.find('"') != 0 and text.find('"') != -1):
                    quotation_mark = False
                    
                temp_chapter = current_chapter
                temp_article = current_article
                temp_clause = current_clause
                temp_point = current_point
                
            except:
                print("Lỗi ở:", "Chương",current_chapter, "Điều",current_article, "Khoản", current_clause)
                print("Văn bản lỗi:", text)
                current_chapter = temp_chapter
                current_article = temp_article
                current_clause = temp_clause
                current_point = temp_point
                

        # with open('vbpl_legal_corpus.jsonl', 'a+', encoding='utf-8') as f:
        #     json.dump(json_data, f, ensure_ascii=False, indent=4)
        
    else:
        print("Không tìm thấy nội dung")
        return None
    
    if json_data["lawid"] == "":
        json_data["lawid"] = "Không số"
    
    return json_data

if __name__ == '__main__':
    url = "https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=96122&Keyword="
    
    json_data = crawl_data(url)
    
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
                        
    
    
        
    

