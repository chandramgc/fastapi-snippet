from src.core.config import KAFKA_CLIENT, KAFKA_TOPIC, PROJECT_NAME
from pykafka import KafkaClient
import time

client = KafkaClient(KAFKA_CLIENT)
geostream = client.topcis[KAFKA_TOPIC]


def producer_msg():
    with geostream.get_sync_producer() as producer:
        for i in range(10):
            producer.produce(
                ("Kafka is not just an author " + str(i).encode("ascii")))
            time.sleep(1)


def consumer_msg(topicname):
    for message in client.topics[topicname].get_simple_consumer():
        yield f"i.value.decode()"
