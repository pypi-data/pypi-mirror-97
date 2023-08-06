import asyncio
from kickredis.granite.granite_analytics import GraniteQuestion
from kickredis.mock_analytics import MockQuestion
from kickredis.registry import Question, Stream, object_registry
import logging
import lightbus

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s,%(msecs)d - %(name)s/%(threadName)s - %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

log = logging.getLogger("kicker.client")

bus = lightbus.create()


async def create_question():
    qh = await bus.AnalyticsService.new_question.call_async(
        query="device(color == red).stream(stream1).window(count, 10).compute(average)",
        is_start=True,
    )
    return qh


async def consume_question_results(question_handle):
    question_id: str = question_handle["id"]
    log.info(f"Start listing for result for question id={question_id}")
    q = GraniteQuestion(pk=question_id)
    kstream = q.find_out_stream_by_name("average")

    async for messages in kstream.consume("mqtt_bridge_consumer1"):
        for msg in messages:
            log.info(f"Processed message :{msg}")
            await kstream.acknowledge(msg)


async def consume_sensor_data():
    device_id = "bot_dev"
    dev = object_registry.find_device(device_id)

    temp_stream: Stream = dev.find_stream_by_name("temperature")

    async for messages in temp_stream.consume("mqtt_bridge_consumer2"):
        log.info(f"Got {len(messages)} messages")
        for msg in messages:
            log.info(f"Processed message :{msg}")
            await temp_stream.acknowledge(msg)


async def runFlow():
    # await consume_sensor_data()
    qHandle = await create_question()
    # qHandle = {"id": "q_id_1"}
    log.info(f"Question created. Handle:{qHandle}")
    await consume_question_results(qHandle)


def main():
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(runFlow())
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process interrupted")
    finally:
        loop.close()
        logging.info("Successfully shutdown")


if __name__ == "__main__":
    main()
