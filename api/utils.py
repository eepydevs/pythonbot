import redis as rd
import json
import os

class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]
    
class RedisManager(metaclass = Singleton):
  def __init__(self, name: str = "main", key: str = None, *, host: str, port: int, password: str, client_name: str, charset: str = "utf-8", decode_responses: bool = True):
    self._redis = rd.Redis(host = host, port = port, password = password, client_name = client_name, charset = charset, decode_responses = decode_responses)
    self._name = name
    self._key = key if key else name
  
  def __enter__(self) -> dict:
    if self._key not in self._redis.keys():
      self._redis.hset(self._name, self._name, "{}")
    self._var = json.loads(self._redis.hget(self._name, self._key))
    return self._var
  
  def __exit__(self, exc_type, exc_value, exc_traceback):
    if self._var != json.loads(self._redis.hget(self._name, self._key)):
      self._redis.hset(self._name, self._key, json.dumps(self._var))