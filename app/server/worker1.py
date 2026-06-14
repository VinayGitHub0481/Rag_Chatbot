
#here the input pdf file will gets to the worker function

from dotenv import load_dotenv
load_dotenv()
import os  
os.getenv("OPENAI_API_KEY")

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

import uuid



 #here we need to perform embeddings to the chunks to store in the vector db like (Qdrant)
embedded_model=OpenAIEmbeddings(
            model='text-embedding-3-large'
        )


def loading_file(content:bytes,filename:str) :
     try:
        
        filename=f"{uuid.uuid4()}.pdf"  #here by this for each pdf upload new unique id will be generated 

        file_path=os.path.join("temp_files",filename)  #means the filename is stored in the os file_path 

        os.makedirs("temp_files",exist_ok=True)

        with open (file_path,'wb') as f:
            f.write(content)               #here we are writing bytes to the file 

            print("bytes uploaded successful in the filepath")
        
        #step-1: loading of pages in the respective file path
        loader=PyPDFLoader(file_path)
        document=loader.load()   #here the pdf gets loaded and the pages will be obtained



        #here by using RecursiveCharacterTextSplitter we are specifing chunk size and chunk overlap 
        splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200  #here we need to overlap the chunks because to remember the context between the chunks 
            )
        
        print("document splitted ")
        #here by the split_document() instance method we are splitting the document 
        chunks=splitter.split_documents(document)


        #here we perform embeddings to the splitted text 
        QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embedded_model,
            url="http://localhost:6333",
            collection_name="document"    
        )
        print(f"data loaded into the document collection")

        try:
            os.remove(file_path)  #here after uploading the pdf we are cleaning up the path
        except FileNotFoundError:
            pass


        return  "uploaded successfull"
        
     except Exception as e:
         print(e)
      



    


    




















































