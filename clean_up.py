# -*- coding: utf-8 -*-

from redis import Redis

from conf import conf


redis = Redis.from_url(conf['redis']['url'])


pattern = input("삭제 패턴(기본 값: *#*#*):")

if len(pattern) == 0 or pattern is None:
    pattern = "*#*#*"
print("===============================\n"
      f"삭제 패턴 : {pattern}\n"
      "===============================\n")

for key in redis.keys(pattern):
    redis.delete(key)
    print(f"삭제 : {key.decode()}")
