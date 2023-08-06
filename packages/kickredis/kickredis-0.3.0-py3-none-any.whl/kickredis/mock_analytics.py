import logging
import asyncio

from kickredis.registry import Question, Stream, object_registry
from kickredis.services import AnalyticsService


log = logging.getLogger("kicker.services.mock")


class MockQuestion(Question):
    async def run(self):
        in_strm: Stream = self.find_in_stream_by_name("temperature")
        out_strm: Stream = self.find_out_stream_by_name("average")
        # read from input and send to output
        async for messages in in_strm.consume(f"q_{self.pk}_consumer"):
            log.info(f"Got {len(messages)} messages")
            for msg in messages:
                await in_strm.acknowledge(msg)
                log.info(f"Processed message :{msg}")
                t = msg.kwargs["temperature"]
                await out_strm.send_value(t)


class MockAnalyticsService(AnalyticsService):
    class Meta:
        name = "AnalyticsService"

    def _parse_question_from_str(self, query: str) -> Question:
        # should parse query like this
        # "device(id == bot_dev).stream(temperature).window(count, 10).compute(average)"
        dev = object_registry.find_device("bot_dev")
        temp_stream = dev.find_stream_by_name("temperature")

        q = MockQuestion(pk=self._gen_id())
        q.query_str = query
        q.in_streams.sadd(temp_stream)

        q.add_out_stream("average")
        return q
