import redis

redis_client = None

try:
    redis_client = redis.Redis(
        host="redis",
        port=6379,
        db=0,
        socket_connect_timeout=1,   #  fast fail
        socket_timeout=1,           #  fast fail
        retry_on_timeout=False
    )

    redis_client.ping()  # test connection

except:
    print("Redis not available")
    redis_client = None