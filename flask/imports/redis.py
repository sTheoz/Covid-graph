import redis
import time

def inject_redis(df, data):
    # 0 = database
    r = redis.Redis(host='redis', port=6379, db=0)
    start_time = time.time()
    for key in data['data']:
        r.set(str(key['index']), str(key))
    return (time.time() - start_time)