from redis import Redis

class RedisConn(Redis):
    def __init__(self):
        super().__init__(host='redis_boot', port=6379, encoding='utf8', db=0, decode_responses=True)

    def __del__(self):
        super().close()

    def dset(self, _key, _dict):
        for _d in _dict:
            super().hset(_key, _d, _dict[_d])
    
    def dget(self, _key):
        return super().hgetall(_key)
