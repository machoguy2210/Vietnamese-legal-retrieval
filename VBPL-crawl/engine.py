import json
import requests
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv, set_key
from crawl_data import crawl_data
import time
import threading
import os

def first_phase():
    page = 1

    first = "https://vbpl.vn/VBQPPL_UserControls/Publishing_22/TimKiem/p_KetQuaTimKiemVanBan.aspx?SearchIn=VBPQFulltext&DivID=resultSearch&IsVietNamese=True&Page="
    second = "&type=1&s=0&DonVi=&stemp=1&TimTrong1=Title&TimTrong1=Title1&ddrDiaPhuong=99999&order=VBPQNgayBanHanh&TypeOfOrder=False&LoaiVanBan=15,16,17,19,20,21,22,23&TrangThaiHieuLuc=4,2"
    
    json_data = {
        "link": []
    }

    for page in range(1, 742):
        base_url = first + str(page) + second
        
        response = requests.get(base_url)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        listLaw = soup.find('ul', class_='listLaw')
        
        for p_tag in listLaw.find_all('p', class_ = 'title'):
            link = p_tag.find('a')['href']
            json_data["link"].append("https://vbpl.vn"+link)
        
        time.sleep(2)
            
    with open("links.json", "w") as f:
        json.dump(json_data, f)
        
def second_phase():
    with open("links.json", "r") as f:
        data = json.load(f)
    
    len_data = len(data["link"])
    
        
    def multi_threading(thread_num,data, start, end):
        for i, link in enumerate(data["link"]):
            if i < start:
                continue
            if i >= end:
                break
            print(f"Processing {i+1}/{len_data}")
            data = crawl_data(link)
            
            if data:
                data["number"] = '0'
            
                with open(f"vbpl_legal_corpus_{thread_num}.jsonl", "a+", encoding="utf-8") as f:
                    f.write(json.dumps(data, ensure_ascii=False) + "\n")
            time.sleep(1)
            
    thread_1 = threading.Thread(target=multi_threading, args=(1, data, 20000, 20500)) # Done
    thread_2 = threading.Thread(target=multi_threading, args=(2, data, 20500, 21000)) # Done
    thread_3 = threading.Thread(target=multi_threading, args=(3, data, 21000, 21500)) # Done
    thread_4 = threading.Thread(target=multi_threading, args=(4, data, 21500, 22215)) # Done
    
    
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    
    
            
    

         
if __name__ == "__main__":
    
    load_dotenv()
    
    # Do the first phase to get all the links
    # first_phase()
    
    second_phase()
    
            
        
        
        
        
    
    
