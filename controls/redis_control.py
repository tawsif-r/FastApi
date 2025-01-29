import redis
import json



class RedisControl:
    def __init__(self,redis_host:str,port:str):
        self.redis_client = redis.Redis(host = redis_host,port = port,decode_responses = True)

    def store_data(self,data:list,key:str):
        """
        store the data inside redis cache under the specified key.
        Args:
            data (list):A list of data in the following format->
            [{'fullname': 'jack hanmass', 'name': 'jackss', 'id': 5}, {'fullname': 'jack hanma', 'name': 'jack', 'id': 2}]
            key (str): user-session:123

       
        Returns:
            None
        """
        for i, item in enumerate(data):
            self.redis_client.set(f'{key}:{i}',json.dumps(item))
            print('stored successfully in redis server')
    def get_data_all(self,keys:str)->list:
        """ fetch all the data in the key that
            matches the keys pattern
        keys (str): "user-session:123:*"
        return: list
        """
        keys = self.redis_client.keys(keys)
        retrieved_data = []
        for key in keys:
            retrieved_data.append(json.loads(self.redis_client.get(key)))
        return retrieved_data
    
    def set_expire(self,key:str,expire_time):
        """
        
        Set expire time 

        Args:
            key (str): key for setting the expire time, e.g "user-session:123:*".
            expire_time (int): Set to expire on time. 

        Returns:
            None
        """
        self.redis_client.expire(key, expire_time) 
        