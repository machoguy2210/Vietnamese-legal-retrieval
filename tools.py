from sentence_transformers import SentenceTransformer
from FlagEmbedding import FlagReranker

biencoder_model = SentenceTransformer("tanbinh2210/vietnamese-bi-encoder-on-vbpl-with-neg")

reranker_model = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

def connect_wcd():
    import weaviate
    import weaviate.classes as wvc
    from weaviate.classes.query import Filter
    from weaviate.classes.config import Configure
    import os
    # import requests
    from dotenv import load_dotenv

    load_dotenv()

    # Best practice: store your credentials in environment variables
    wcd_url = os.environ["WCD_URL"]
    wcd_api_key = os.environ['WCD_APIKEY']
    huggingface_key = os.environ['HUGGINGFACE_WEAVIATE']
    headers = {
        "X-HuggingFace-Api-Key": huggingface_key,
    }


    vbpl_client = weaviate.connect_to_weaviate_cloud(
        cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
        auth_credentials=wvc.init.Auth.api_key(wcd_api_key),    # Replace with your Weaviate Cloud key           
        headers=headers,
        additional_config=wvc.init.AdditionalConfig(timeout=wvc.init.Timeout(init=100))     
    )
    
    return vbpl_client

def get_collection(vbpl_client):
    vbpl_collection = vbpl_client.collections.get(name="vbplcorpus")
    
    return vbpl_collection

def search_query(vbpl_collection, query):
    from underthesea import word_tokenize
    query = query.lower()

    query_embedding = biencoder_model.encode(word_tokenize(query,format='text'))
    search_results = vbpl_collection.query.near_vector(query_embedding, limit=50)
    
    pair = [[query, item.properties['text']] for item in search_results.objects]
    scores = reranker_model.compute_score(pair)
    rerank_objects = [f'{object[0].properties["lawid"]}, {object[0].properties["title"]}: {object[0].properties["text"]}' for object in sorted(list(zip(search_results.objects, scores)), key=lambda x: x[1], reverse=True)]
    
    return rerank_objects

def qna(query):
    
    from llm import answer, refine
    
    vbpl_client = connect_wcd()
    
    vbpl_collection = get_collection(vbpl_client)
    
    results = search_query(vbpl_collection, query)
    
    vbpl_client.close()
    
    try:
        context = '\n____________________\n'.join(results)
        response = answer(context, query)
        return response
    except Exception as e:
        return "Không tìm thấy câu trả lời cho câu hỏi của bạn"
    
def law_conflict(document):
    
    from llm import chat_with_model , check_conflict
    import json
    import re
    
    vbpl_client = connect_wcd()
    
    vbpl_collection = get_collection(vbpl_client)
    
    text = chat_with_model(document)
    
    json_data = None
    
    try:
        json_data = json.loads(text)
        
    except Exception as e:
        try:
            reply = re.search(r"```(.+)```", text, re.DOTALL).group(1)
            json_data = json.loads(reply)
        except Exception as ex:
            pass
    
    relevant_chunks = []
    
    if json_data:
        for question in json_data['aspects']:
            results = search_query(vbpl_collection, question)
            relevant_chunks.extend(results[:5])
    else:
        vbpl_client.close()
        return "Có lỗi xảy ra trong quá trình xử lý câu hỏi"
    vbpl_client.close()
    
    try:
        context = '\n____________________\n'.join(relevant_chunks)
        response = check_conflict(context, document)
        return response
    except Exception as e:
        return "Có lỗi xảy ra trong quá trình xử lý câu hỏi"
            
            
            
    
    