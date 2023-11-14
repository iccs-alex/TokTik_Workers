import redis
import config
from json import loads
from convert import convert_to_mp4
from s3 import getVideo, putVideo
import io

def redis_db():
    redisDB = redis.Redis(host=config.REDIS_HOST,
                          port=config.REDIS_PORT,
                          db=config.REDIS_DB_NUM,
                          decode_responses=True
                          )
    return redisDB


def redis_queue_push(redisDB, message):
    redisDB.publish(config.REDIS_PUSH_QUEUE_NAME, message)


def redis_queue_pop(redisDB):
    _, message_json = redisDB.brpop(config.REDIS_LISTEN_QUEUE_NAME)
    return message_json


def process_message(redisDB, message_json: str):
    message = loads(message_json)
    print(f"Message received: id={message['id']}, message={message}.")


def main():
    redisDB = redis_db()
    pubsub = redisDB.pubsub()
    pubsub.subscribe(config.REDIS_LISTEN_QUEUE_NAME)
    for message in pubsub.listen():
        redisDB.publish("backend", "converting")
        channel = message['channel']
        try:
            data = loads(str(message['data']))
        except:
            print("Couldnt unload message: " + str(message['data']))
            continue
        if type(data) is int:
            continue
        print("Message data: " + str(data))
        videoFile = getVideo(data) # Get video stored in s3
        videoBytes = videoFile["Body"].read()
        videoMp4 = convert_to_mp4(videoBytes) # Convert video to mp4
        putVideo(data, videoMp4) # Put video in s3
        redisDB.publish(config.REDIS_PUSH_QUEUE_NAME, data)
        print("Message processed")


if __name__ == "__main__":
    main()
