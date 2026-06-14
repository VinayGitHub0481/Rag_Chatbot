
from redis import Redis 
from rq import Queue 

#here the redis queue connection has been held

#here we are using this rq because it makes the work in background without blocking the api's 

redis_conn=Redis(
    host='localhost',
    port=6379
)

redis_queue1=Queue(connection=redis_conn)  #here the redis_queue referencing to the QUeue Object

print(type(redis_queue1))

print(redis_conn.ping()) #here by this we can verify the connection is held
#if true then ok





