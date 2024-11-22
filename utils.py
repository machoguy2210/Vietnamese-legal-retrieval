import json
from dotenv import load_dotenv, set_key
import os
import re

def chunking(thread_num, _number, doc, max_size, overlapping= 50):
    
    from underthesea import word_tokenize
    
    number = _number
    chunks = []
    chunk = []
    temp_chunk = []
    pointer = []
    length = 0

    def traverse(node,prefix=[]):
        nonlocal length, chunk, pointer, chunks, number, temp_chunk
        if isinstance(node, dict):
            for key, value in node.items():
                if "Tiêu đề" in node:  
                    if len(prefix) > 0 and re.match(r"^"+prefix[-1], node["Tiêu đề"]): # Loại bỏ, ví du: "Chương 1" và "Chương 1. Quy định chung"
                        new_prefix = prefix[:-1] + [node["Tiêu đề"]]
                    else:
                        new_prefix = prefix + [node["Tiêu đề"]]
                else:
                    new_prefix = prefix[:]
                if key != "metadata" and key != "lawid" and key != "number":
                    new_new_prefix = new_prefix + [key]
                    traverse(value, new_new_prefix)
        else:
            if len(chunk) == 0:
                pointer = prefix[:]
            if length + len(node.split()) > max_size:
                chunks.append({"number" : number, "lawid": doc["lawid"], "status": doc["metadata"], "title": pointer,"text": (k:=" ".join(temp_chunk+chunk)), "tokenize_text": word_tokenize(k, format="text")})
                number = str(int(number) + 1)
                temp_chunk = " ".join(chunk).split()[-overlapping:]
                chunk.clear()
                length = 0
                pointer = prefix[:]                
            chunk.append(node)
            length += len(node.split())    
    traverse(doc)
    chunks.append({"number" : number, "lawid": doc["lawid"], "status": doc["metadata"], "title": pointer,"text": (k:=" ".join(temp_chunk+chunk)), "tokenize_text": word_tokenize(k, format="text")})
    os.environ['NUMBER_'+str(thread_num)] = str(int(number) + 1)
    set_key('.env', 'NUMBER_' + str(thread_num), str(int(number) + 1))
    return chunks

def zalo_chunking():
    # Chia chunk theo khoản
    # Gộp các chunk để đủ độ dài
    from underthesea import word_tokenize
    with open('legal_corpus.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        
    chunks = []
    chunk = []
    temp_chunk = []
    temp_length = 0
    length = 0
    number = 1
    
    for idx, doc in enumerate(data):
        if idx % 100 == 0:
            print(idx)            
        for article in doc["articles"]:
            lines = article["text"].split('\n')
            for line in lines:
                if re.match(r"^\d+\.", line):
                    if length + temp_length < 256:
                        chunk.extend(temp_chunk)
                        length += temp_length
                        temp_chunk.clear()
                        temp_length = 0
                        temp_chunk.append(line)
                        temp_length += len(line.split())
                    else:
                        if len(chunk) > 0:
                            if length < 350:
                                chunks.append({"number" : number, "lawid": doc["law_id"], "article_id": article["article_id"], "title": article["title"], "text": " ".join(chunk), "tokenize_text": word_tokenize(" ".join(chunk), format="text")})
                                number += 1
                            else:
                                temp = []
                                len_temp = 0
                                for text in chunk:
                                    if len_temp + len(text.split()) < 256:
                                        temp.append(text)
                                        len_temp += len(text.split())
                                    else:
                                        if len(temp) > 0:
                                            chunks.append({"number" : number, "lawid": doc["law_id"], "article_id": article["article_id"], "title": article["title"], "text": " ".join(temp), "tokenize_text": word_tokenize(" ".join(temp), format="text")})
                                            number += 1
                                        temp.clear()
                                        len_temp = 0
                                        temp.append(text)
                                        len_temp += len(text.split())
                                if len(temp) > 0:
                                    chunks.append({"number" : number, "lawid": doc["law_id"], "article_id": article["article_id"], "title": article["title"], "text": " ".join(temp), "tokenize_text": word_tokenize(" ".join(temp), format="text")})
                                    number += 1
                        chunk = temp_chunk[:]
                        length = temp_length
                        temp_chunk.clear()
                        temp_length = 0
                        temp_chunk.append(line)
                        temp_length += len(line.split())
                elif re.match(r"^\w\)", line):
                    temp_chunk.append(line)
                    temp_length += len(line.split())                        
                else:
                    if len(temp_chunk) > 0:
                        temp_chunk.append(line)
                        temp_length += len(line.split())
                    else:
                        chunk.append(line)
                        length += len(line.split())
            if length + temp_length < 256:
                chunk.extend(temp_chunk)
                chunks.append({"number" : number, "lawid": doc["law_id"], "article_id": article["article_id"], "title": article["title"], "text": " ".join(chunk), "tokenize_text": word_tokenize(" ".join(chunk), format="text")})
                number += 1
                chunk.clear()
                temp_chunk.clear()
                temp_length = 0
                length = 0
            else:
                if len(chunk) > 0:  
                    chunks.append({"number" : number, "lawid": doc["law_id"], "article_id": article["article_id"], "title": article["title"], "text": " ".join(chunk), "tokenize_text": word_tokenize(" ".join(chunk), format="text")})
                    number += 1
                if len(temp_chunk) > 0:
                    chunks.append({"number" : number, "lawid": doc["law_id"], "article_id": article["article_id"], "title": article["title"], "text": " ".join(temp_chunk), "tokenize_text": word_tokenize(" ".join(temp_chunk), format="text")})
                    number += 1
                chunk.clear()
                temp_chunk.clear()
                temp_length = 0
                length = 0                
            
            
    with open('zalo_chunks.jsonl', 'w', encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                

def filter_data(docs):
    def condition(doc: dict):
        lawid = doc["lawid"]
        num_keys = len(doc.keys())
        if num_keys == 4:
            return False
        if "UBND" in lawid:
            print(lawid)
            return False
        if "HĐND" in lawid or "HDND" in lawid:
            print(lawid)
            return False
        if "NQ-UB" in lawid:
            print(lawid)
            return False
        return True
    return list(filter(condition, docs))

def data_statistics():
    
    with open('chunk_0.jsonl', 'r', encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
        
    length_statistics_2 = {
        "<100" : 0,
        "100-256" : 0,
        ">256" : 0
    }
    
    length_statistics = {}
    
    max_length = 0
    min_length = 1000000
    
    for doc in chunks:
        length = len(doc["text"].split())
        if length > max_length:
            max_length = length
        if length < min_length and length > 0:
            min_length = length
            
        if length < 100:
            length_statistics_2["<100"] += 1
        elif length >= 100 and length <= 256:
            length_statistics_2["100-256"] += 1
        else:
            length_statistics_2[">256"] += 1
        
        if length > 0:
            if length in length_statistics:
                length_statistics[length] += 1
            else:
                length_statistics[length] = 1
            
    print(max_length, min_length)
    
    print(length_statistics_2)
    
    with open("length_statistics.csv", 'w', encoding="utf-8") as f:
        for key, value in length_statistics.items():
            f.write(f"{key}, {value}\n")
    

def zalo_statistics():
    
    with open("zalo_chunks.jsonl", 'r', encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
    
    zalo_length_statistics = {}
    
    for doc in chunks:
        length = len(doc["text"].split())
        if length in zalo_length_statistics:
            zalo_length_statistics[length] += 1
        else:
            zalo_length_statistics[length] = 1
        
    with open("zalo_length_statistics.csv", 'w', encoding="utf-8") as f:
        for key, value in zalo_length_statistics.items():
            f.write(f"{key}, {value}\n")
         
        
def list_doc():
    
    # with open('chunk_0.jsonl', 'r', encoding="utf-8") as f:
    #     chunks = [json.loads(line) for line in f]
        
    # for doc in chunks:
    #     length = len(doc["tokenize_text"].split())
        
    #     if length < 50:
    #         print(doc["number"], doc["text"], sep=" | ")
    
    with open("legal_corpus.json", 'r', encoding="utf-8") as f:
        data = json.load(f)
        
    for idx, doc in enumerate(data):
        # match = re.match(r"\d+/\d+/.*", doc["law_id"])
        # if not match:
        #     print(doc["law_id"])
        
        if doc["law_id"] == "12/2017/qh14":
            print(idx)
            break
        
def zalo_qna_data_reformat():
    
    import random
    from sklearn.model_selection import train_test_split
    
    with open("train_question_answer.json", 'r', encoding="utf-8") as f:
        data = json.load(f)
        
    print(len(data["items"]))
        
    data = data['items']
    
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=21)
    
    data = train_data
    
    with open('zalo_test_data.json', 'w', encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False)
        
    with open("zalo_chunks.jsonl", 'r', encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
        
    number = 1
    
    items = []
    train_data = []
        
    for qna in data:
        relevant_chunks = []
        for relevant_article in qna["relevant_articles"]:
            lawid = relevant_article["law_id"]
            article_id = relevant_article["article_id"]
            for idx, chunk in enumerate(chunks):
                if chunk["lawid"] == lawid and chunk["article_id"] == article_id:
                    relevant_chunks.append(idx)
        
        for idx in relevant_chunks:
            items.append({ "number": str(number), "query": qna["question"], "title": chunks[idx]["title"], "answer": chunks[idx]["text"], "lawid": chunks[idx]["lawid"], "article_id": chunks[idx]["article_id"]})
            train_data.append({"query": qna["question"], "pos": f"{chunks[idx]['title']}: {chunks[idx]['text']}"})
            number += 1
            
    with open("zalo_qna.jsonl", 'w', encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    random.shuffle(train_data)
            
    with open("zalo_qna_train.json", 'w', encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False)
        
def zalo_qna_train_data():
    import json
    with open("train_question_answer.json", 'r', encoding="utf-8") as f:
        corpus = json.load(f)
    with open("zalo_test_data.json", 'r', encoding="utf-8") as f:
        test_data = json.load(f)
        
    corpus = corpus["items"]
    
    test_question_id = [item["question_id"] for item in test_data]
    
    print(len(test_question_id))
    
    train_data = []
    
    for qna in corpus:
        if qna["question_id"] not in test_question_id:
            train_data.append(qna)
            
    print(len(train_data))
    
    with open("zalo_train_data.json", 'w', encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False)
    
def train_test_splitt():
    import json
    import random
    
    with open("E:\\Code\\DeepLeaning\\Vietnamese-legal-retriever\\data\\qna_filtered_data_on_chunkidx.jsonl", 'r', encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
        
    random.shuffle(data)
    
    train_data = data[:int(len(data)*0.9)]
    print(len(train_data))
    
    test_data = data[int(len(data)*0.9):]
    
    print(len(test_data))
    
    with open("E:\\Code\\DeepLeaning\\Vietnamese-legal-retriever\\data\\qna_filtered_train_data.jsonl", 'w', encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    with open("E:\\Code\\DeepLeaning\\Vietnamese-legal-retriever\\data\\qna_filtered_test_data.jsonl", 'w', encoding="utf-8") as f:
        for item in test_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
def train_data_reformat():
    with open("E:\\Code\\DeepLeaning\\Vietnamese-legal-retriever\\data\\qna_filtered_train_data.jsonl", 'r', encoding="utf-8") as f:
        query_data = [json.loads(line) for line in f]
        
    with open("chunk_0.jsonl", 'r', encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
        
    refomatted_data = []
    
    for qna in query_data:
        answer_idx = int(qna["answer_idx"])
        if(chunks[answer_idx-1]["number"] != str(answer_idx)):
            print("Error")
            exit()
            
        refomatted_data.append({"query": qna["question"], "pos": f"{', '.join(chunks[answer_idx-1]['title'])}: {chunks[answer_idx-1]['text']}".lower()})
        
    with open("E:\\Code\\DeepLeaning\\Vietnamese-legal-retriever\\data\\qna_filtered_train_data_reformatted.json", 'w', encoding="utf-8") as f:
        json.dump(refomatted_data, f, ensure_ascii=False)
        
def zalo_qna_train_reformat():
    import json
    from FlagEmbedding import FlagReranker
    reranker = FlagReranker("BAAI/bge-reranker-v2-m3", use_fp16=True)
    
    with open("zalo_train_data.json", 'r', encoding="utf-8") as f:
        data = json.load(f)
        
    with open("zalo_chunks.jsonl", 'r', encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
        
    qna_list = []
    
    for qna in data:
        pos = []
        for relevant_article in qna["relevant_articles"]:
            for chunk in chunks:
                if chunk["lawid"] == relevant_article["law_id"] and chunk["article_id"] == relevant_article["article_id"]:
                    pos.append(f"{chunk['title']}: {chunk['text']}")
        pairs = [[qna["question"], p] for p in pos]
        scores = reranker.compute_score(pairs, normalize=True)
        new_pos = [pos[idx] for idx, score in enumerate(scores) if score > 0.65]
        for p in new_pos:
            qna_list.append({"query": qna["question"], "pos": p})
    
    with open("zalo_qna_train_reformatted.json", 'w', encoding="utf-8") as f:
        json.dump(qna_list, f, ensure_ascii=False)
        
            
            
if __name__=="__main__":
    
    
    '''Chunking'''
    
    # load_dotenv()
    
    # with open('output.json', 'r', encoding="utf-8") as f:
    #     data = json.load(f)
        
    # chunks = chunking(1,1, data, 190)
    
    # with open('chunks.jsonl', 'a+', encoding="utf-8") as f:
    #     for chunk in chunks:
    #         f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    
    '''Chunking zalo data'''
    # zalo_chunking()
    
    
    '''Filter data để bỏ những văn bản lỗi và không cần thiết'''
    
    # with open('vbpl_legal_corpus.jsonl', 'r', encoding="utf-8") as f:
    #     docs = [json.loads(line) for line in f]        
            
    # print(len(docs))
    
    # docs = filter_data(docs)
    
    # print(len(docs))
    
    # with open('vbpl_legal_corpus_filtered.jsonl', 'w', encoding="utf-8") as f:
    #     for doc in docs:
    #         f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    
    '''Data statistics'''
    
    # data_statistics()
    
    # zalo_statistics()
    
    # list_doc()
    
    '''Zalo QnA data reformat'''
    
    # zalo_qna_data_reformat()
    
    '''Split data'''
    
    # train_test_splitt()
    
    # train_data_reformat()
    
    # zalo_qna_train_data()
    
    zalo_qna_train_reformat() 
    