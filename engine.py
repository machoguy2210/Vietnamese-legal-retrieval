import os
import json
from dotenv import load_dotenv, set_key
import re

def multi_thread(thread_num ,data):
    
    from utils import chunking
    
    length = len(data)
    
    for i,doc in enumerate(data):
        
        print(f"Processing {i+1}/{length}")
        
        number = '1'
        if os.getenv('NUMBER_'+str(thread_num)):
            number = os.environ['NUMBER_'+str(thread_num)]
        else:
            set_key('.env', 'NUMBER_'+str(thread_num), '1')
        print(number)
        chunks = chunking(thread_num, number, doc, 190, overlapping=50)
        
        
        with open(f'chunk_{thread_num}.jsonl', 'a+', encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                
def chunk_data():
    load_dotenv()
    
    with open('vbpl_legal_corpus_filtered.jsonl', 'r', encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
    
    multi_thread(0, data)
    
def gen_query():
    
    from llm import response, clear_conversation
    import time
    
    query_answer = []
    
    number = '1'
    
    
    if os.getenv('QUERY_NUMBER'):
        number = os.environ['QUERY_NUMBER']
    else:
        set_key('.env', 'QUERY_NUMBER', '1')
    
    data = []    
    
    with open('chunk_0.jsonl', 'r', encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if idx < 14397:
                continue
            data.append(json.loads(line))
    
    for doc in data:
        
        print(f"Processing {doc['number']}")
        
        length = len(doc["tokenize_text"].split())
        
        if length < 50:
            continue
        
        try:
            text = str(response(doc['text']))
        except Exception as e:
            print("Error while processing: ", doc['number'])
            continue
        
        try:
            json_data = json.loads(text)
            
        except Exception as e:
            try:
                reply = re.search(r"```(.+)```", text, re.DOTALL).group(1)
                json_data = json.loads(reply)
            except Exception as ex:
                pass
        if json_data:
            for question in json_data['questions']:
                query_answer.append({"number": number, "lawid": doc['lawid'], "question": question, "answer_idx": doc['number']})
                number = str(int(number) + 1)
                
            with open('query_answer.jsonl', 'a+', encoding="utf-8") as f:
                for qa in query_answer:
                    f.write(json.dumps(qa, ensure_ascii=False) + "\n")
                
        query_answer.clear()
                
        set_key('.env', 'QUERY_NUMBER', number)
        
        if (int(doc['number']) % 20 == 0):
            clear_conversation()
        
        time.sleep(1)
    
def zalo_embedd():
    
    from sentence_transformers import SentenceTransformer
    import pickle
    
    model = SentenceTransformer("tanbinh2210/bge-m3-zalo-trained")
    
    model.max_seq_length = 1300
    
    with open('zalo_chunks.jsonl', 'r', encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
        
    chunks = chunks[50000:]
        
    doc_embeddings = []
        
    for chunk in chunks:
        if int(chunk['number']) % 2000 == 1:
            print(f"Processing {chunk['number']}")
        
        embeddings = model.encode(f"{chunk['title']}: {chunk['text']}".lower())
        
        doc_embeddings.append(list(embeddings))           
        
    with open('zalo_embeddings_5.pkl', 'wb') as f:
        pickle.dump(doc_embeddings, f)
                
        
        
if __name__ == '__main__':
    
    load_dotenv()
    
    # chunk_data()
    
    # gen_query()
    
    zalo_embedd()
    
    
    

    
    