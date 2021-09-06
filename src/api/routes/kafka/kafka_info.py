from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import typing
from fastapi import WebSocket
from loguru import logger
from src.model.schema.kafka import ConsumerResponse, ProducerMessage, ProducerResponse
from src.core.config import KAFKA_CLIENT, KAFKA_TOPIC, PROJECT_NAME
from starlette.endpoints import WebSocketEndpoint
from starlette.middleware.cors import CORSMiddleware

router = APIRouter()

loop = asyncio.get_event_loop()
aioproducer = AIOKafkaProducer(
    loop=loop, client_id=PROJECT_NAME, bootstrap_servers=KAFKA_CLIENT

)

async def consume(consumer, topicname):
    async for msg in consumer:
        return msg.value.decode()

@router.on_event("startup")
async def startup_event():
    await aioproducer.start()


@router.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()


@router.get("/")
async def getHelloWorld(name: str = None) -> str:
    return {"name": name + " hello world"}

@router.post("/producer/{topicname}")
async def kafka_produce(msg: ProducerMessage, topicname: str):
    await aioproducer.send(topicname, json.dumps(msg.dict()).encode("ascii"))
    response = ProducerResponse(
        name=msg.name, message_id=msg.message_id, topic=topicname
    )

    return response

@router.websocket_route("/consumer/{topicname}")
class WebsocketConsumer(WebSocketEndpoint):
    """
    Consume messages from <topicname>
    This will start a Kafka Consumer from a topic
    And this path operation will:
    * return ConsumerResponse
    """

    async def on_connect(self, websocket: WebSocket) -> None:
        topicname = websocket["path"].split("/")[2]  # until I figure out an alternative

        await websocket.accept()
        await websocket.send_json({"Message: ": "connected"})

        loop = asyncio.get_event_loop()
        self.consumer = AIOKafkaConsumer(
            topicname,
            loop=loop,
            client_id=PROJECT_NAME,
            bootstrap_servers=KAFKA_CLIENT,
            enable_auto_commit=False,
        )

        await self.consumer.start()

        self.consumer_task = asyncio.create_task(
            self.send_consumer_message(websocket=websocket, topicname=topicname)
        )

        logger.info("connected")

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        self.consumer_task.cancel()
        await self.consumer.stop()
        logger.info(f"counter: {self.counter}")
        logger.info("disconnected")
        logger.info("consumer stopped")

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_json({"Message: ": data})

    async def send_consumer_message(self, websocket: WebSocket, topicname: str) -> None:
        self.counter = 0
        while True:
            data = await consume(self.consumer, topicname)
            response = ConsumerResponse(topic=topicname, **json.loads(data))
            logger.info(response)
            await websocket.send_text(f"{response.json()}")
            self.counter = self.counter + 1