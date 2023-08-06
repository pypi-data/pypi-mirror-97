import logging
import asyncio
import lightbus.api
import time

from kickredis.mock_analytics import MockAnalyticsService
from kickredis.granite.granite_analytics import GraniteAnalyticsService
import grpc
import kickredis.granite.kicker_pb2_grpc as kicker_engine
import kickredis.granite.kicker_pb2 as kicker_engine_types


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d - %(name)s/%(threadName)s - %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

log = logging.getLogger("kicker.server")


async def consume_granite(stream):
    # while True:
    #     print(1)
    #     await asyncio.sleep(100)
    async for data in stream:
        print(f"Alexi:{data.match}")


async def push_data(stub):
    for sample in range(int(1e100)):
        stub.PushData(
            kicker_engine_types.Data(
                device="device1",
                stream="stream1",
                timestamp=int(time.time()),
                integer=sample,
            )
        )

        await asyncio.sleep(3)


async def runFlow():
    # async with grpc.aio.insecure_channel("127.0.0.1:50051") as channel:
    channel = grpc.aio.insecure_channel("127.0.0.1:50051")
    stub = kicker_engine.KickerEngineStub(channel)

    # response = await stub.AddDevice(
    #     kicker_engine_types.Device(
    #         name="device1",
    #         streams=[kicker_engine_types.Stream(name="stream1")],
    #         tags=[
    #             kicker_engine_types.Tag(key="color", value="green"),
    #             kicker_engine_types.Tag(key="type", value="superdevice"),
    #         ],
    #     )
    # )

    # print("Add device response: " + response.message)
    stream = stub.AddQuery(
        kicker_engine_types.Query(query="device(device1).stream(stream1)")
    )

    asyncio.create_task(consume_granite(stream))
    asyncio.create_task(push_data(stub))
    # await push_data(stub)


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
    # asyncio.run (main1(), debug=True)
    main()
