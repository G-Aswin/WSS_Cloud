from __future__ import annotations

from typing import Optional, Final

from redis.client import Redis

from base import Worker
from constants import IN, COUNT, FNAME


class MyRedis:
  def __init__(self):
    self.rds: Final = Redis(host='localhost', port=6379, password='pass',
                       db=0, decode_responses=False)
    self.rds.flushall()
    self.rds.xgroup_create(IN, Worker.GROUP, id="0", mkstream=True)

  def add_file(self, fname: str):
    self.rds.xadd(IN, {FNAME: fname})

  def top(self, n: int) -> list[tuple[bytes, float]]:
    return self.rds.zrevrangebyscore(COUNT, '+inf', '-inf', 0, n,
                                     withscores=True)
    
  # Add new methods here which interact with the Redis server
  def get_file(self, consumer_name):
    obj =  self.rds.xreadgroup(Worker.GROUP, consumer_name, {IN : ">"}, 1)
    if obj == []:
      return (None, None)
    
    filename = obj[0][1][0][1][b"fname"]
    file_id = obj[0][1][0][0]
    return (filename, file_id)
  
  def increment_word(self, word, count):
    # op = self.rds.zadd(name=COUNT, mapping={word: count}, incr=True)
    self.rds.zincrby(name=COUNT, amount=count, value=word)
    
  def ack(self, file_id):
    self.rds.xack(IN, Worker.GROUP, file_id)
    
  def autoclaim(self, consumer_name):
    obj = self.rds.xautoclaim(IN, Worker.GROUP, consumer_name, 500, "-" )
    print(obj)
    if obj[0] == b'0-0':
      return (None, None)
    
    file_id, dic = obj[1][0]
    filename = dic[b'fname']
    print(filename)
    return (filename, file_id)