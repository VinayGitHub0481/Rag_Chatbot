
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI,UploadFile,File,Query
from client.redis_queue import redis_queue1
from server.worker1 import loading_file
from server.worker2 import retrieve_info


#here main purpose of redis queue is to make the process run in the background using enqueue()

app=FastAPI()


@app.post("/upload")
async def insert_file(file_upload:UploadFile=File(...,description="Insert the file ")):
    content= await file_upload.read()

    job=redis_queue1.enqueue(loading_file,content,file_upload.filename)  #here uploading of file will takes place in the background function


    return {"status":job.get_status(),"job-id":job.id}



@app.post("/query")
def user_query(query:str=Query(
  min_length=8,max_length=80
)):
   
   job=redis_queue1.enqueue(retrieve_info,query)

   return {"job-id":job.id}



@app.get("/info")
def get_data(job_id:str):
   
   job=redis_queue1.fetch_job(job_id)  #here based on the input id the worker checks if there are any job in queue and worker will fetch if related data present 

   if (job.is_finished):
      return {"status":job.get_status(),"result":job.result
              }
   elif (job.is_failed):
       return {"status":job.get_status()}
   else:
      return {"status":job.get_status()}





    
  
    
  


    

































