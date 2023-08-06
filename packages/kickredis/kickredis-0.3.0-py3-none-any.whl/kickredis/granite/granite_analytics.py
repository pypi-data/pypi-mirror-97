import logging
import asyncio

from kickredis.registry import Question, Stream, object_registry
from kickredis.services import AnalyticsService

import grpc
import kickredis.granite.kicker_pb2_grpc as kicker_engine
import kickredis.granite.kicker_pb2 as kicker_engine_types
import time

RED = "\u001b[31m"
RESET = "\u001b[0m"

log = logging.getLogger("kicker.services.mock")


def query_callback(stream, query_name, color):
    for data in stream:
        print(f"{color} `{query_name}` {RESET} data response: " + data.match)


class GraniteQuestion(Question):
    async def send_to_granite(stub, val):
        stub.PushData(
            kicker_engine_types.Data(
                device="device1",
                stream="stream1",
                timestamp=int(time.time()),
                integer=val,
            )
        )

    async def forward_query_input_to_granite(self, stub):
        in_strm: Stream = self.find_in_stream_by_name("temperature")
        async for messages in in_strm.consume(f"q_{self.pk}_consumer"):
            print(f"Got {len(messages)} messages")
            for msg in messages:
                await in_strm.acknowledge(msg)
                log.info(f"Processed message :{msg}")
                t = msg.kwargs["temperature"]
                await stub.PushData(
                    kicker_engine_types.Data(
                        device="device1",
                        stream="stream1",
                        timestamp=int(time.time()),
                        integer=t,
                    )
                )

    async def forward_granite_query_result_to_redis(self, stream):
        out_strm: Stream = self.find_out_stream_by_name("average")
        async for data in stream:
            log.debug(f"{data.match}")
            await out_strm.send_value(data.match)

    async def run(self):
        channel = grpc.aio.insecure_channel("127.0.0.1:50051")
        stub = kicker_engine.KickerEngineStub(channel)

        response = await stub.AddDevice(
            kicker_engine_types.Device(
                name="device1",
                streams=[kicker_engine_types.Stream(name="stream1")],
                tags=[
                    kicker_engine_types.Tag(key="color", value="green"),
                    kicker_engine_types.Tag(key="type", value="superdevice"),
                ],
            )
        )

        print("Add device response: " + response.message)

        query_result_stream = stub.AddQuery(
            kicker_engine_types.Query(query="device(device1).stream(stream1)")
        )

        asyncio.create_task(
            self.forward_granite_query_result_to_redis(query_result_stream)
        )

        asyncio.create_task(self.forward_query_input_to_granite(stub))


class GraniteAnalyticsService(AnalyticsService):
    class Meta:
        name = "AnalyticsService"

    def _parse_question_from_str(self, query: str) -> Question:
        # should parse query like this
        # "device(id == bot_dev).stream(temperature).window(count, 10).compute(average)"
        dev = object_registry.find_device("bot_dev")
        temp_stream = dev.find_stream_by_name("temperature")

        q = GraniteQuestion(pk=self._gen_id())
        q.query_str = query
        q.in_streams.sadd(temp_stream)

        q.add_out_stream("average")
        return q
