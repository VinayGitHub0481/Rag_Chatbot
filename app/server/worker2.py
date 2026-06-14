
#here this worker is used to respond to the user query and fetch the related data from the Qdrant db.
from dotenv import load_dotenv
load_dotenv()
import os  
os.getenv("OPENAI_API_KEY")

from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import CrossEncoder  #for re-ranking using CrossEncoder
from openai import OpenAI


client=OpenAI()



#here i am performing the re-ranking to the obtained chunks for more accuracy using CrossEncoders model

encoder_llm=CrossEncoder('BAAI/bge-reranker-base')  #this model is used to re-rank the top k chunks from the embedding models



#here based on the user query we perform embeddings() and search in the respective db

embeding_query=OpenAIEmbeddings(
        model='text-embedding-3-large'
    )



#this worker will handles the user query obtain the relvent response data from Qdrant db as output

def retrieve_info(user_query:str):

    vector_data=QdrantVectorStore.from_existing_collection(
        embedding=embeding_query,
        url="http://localhost:6333",
        collection_name="document"             #from existing collection we are checking 
   )
    print("checking in existing collection ")

    data_search=vector_data.similarity_search(
        query=user_query,
        k=15            #here getting top 15 chunks from the db according to their scores 
        )
    print('similarity search')
   
    #here we are performing reranking using CrossEncoder model

    obtained_data=[(user_query,data.page_content) for data in data_search] #we get list of chunks as result by similarity_search with the user_query

    scores=encoder_llm.predict(obtained_data)  #here we obtaining revised scores to the output chunks

    ranked_docs=sorted(
        zip(data_search,scores), 
        key=lambda x:x[1],   #here based on the scores we are sorting 
        reverse=True,   
    ) [:5]   #here top 5 re-ranked data gets obtained


    context="\n\n".join( [f"Content : {docs.page_content}" for docs,_ in ranked_docs])
     #here this is the list of  context we obtained from the re-ranker model 


    SYSTEM_PROMPT=f"""
    Hey AI assistant you should help me to get the context based on the above user query

    Note: you should give output response ONLY and ONLY from the  context 

    Context:
    {context}

    Query:
    {user_query}

    """
        
    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT   #here through the prompt context is given 
            },
            {
                "role":"user",
                "content":user_query    #here user query is given to the model
            }
        ]
)

    return response.choices[0].message.content



    


    




































