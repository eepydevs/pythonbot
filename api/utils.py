from rocksdict import Rdict
import redis as rd
import json
import os

class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]
    
class RdictManager(metaclass = Singleton):
    def __init__(self, path: str, name: str = "main", key: str = "main"):
        self._redis = rd.Redis(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"], charset = "utf-8", decode_responses = True)
        self._path = path
        self._rediskey = key
        self._redisname = name

    def __enter__(self) -> dict:
        self._rdict = Rdict(self._path)
        if self._rediskey not in self._rdict:
            if not self._redis.hexists(self._redisname, self._rediskey): self._rdict[self._rediskey] = {}
            else: self._rdict[self._rediskey] = json.loads(self._redis.hget(self._redisname, self._rediskey))
        self._var = self._rdict[self._rediskey]
        return self._var
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._rdict[self._rediskey] = self._var
        if self._rdict[self._rediskey] and json.loads(self._redis.hget(self._redisname, self._rediskey)) != self._rdict[self._rediskey]: self._redis.hset(self._redisname, self._rediskey, json.dumps(self._rdict[self._rediskey]))
        self._rdict.close()