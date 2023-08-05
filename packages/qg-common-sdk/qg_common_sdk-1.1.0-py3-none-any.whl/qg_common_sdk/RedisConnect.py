
from redis import StrictRedis

def get_redis(config):
    redisConfig = config.get('spring').get('redis')
    redis = StrictRedis(host=redisConfig["host"], port=redisConfig["port"], db=redisConfig["database"], password=redisConfig["password"], decode_responses=True)
    return redis