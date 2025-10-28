import asyncio
from aiokafka import AIOKafkaConsumer

from app.config import Config


async def main():
    consumer = AIOKafkaConsumer(
        "messages",
        bootstrap_servers=Config.KAFKA_BOOTSTRAP_IP,
        group_id="demo-group",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: v.decode("utf-8"),
    )
    await consumer.start()

    try:
        async for msg in consumer:
            print(f"{msg.topic}:{msg.partition}@{msg.offset} key={msg.key} value={msg.value}")

    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
