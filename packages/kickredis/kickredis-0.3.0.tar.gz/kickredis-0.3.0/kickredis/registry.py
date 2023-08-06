import asyncio
import logging
from enum import Enum
from os import stat
import redis
from dataclasses import dataclass
from lightbus.message import EventMessage
from lightbus.transports.redis.event import RedisEventTransport, StreamUse
from astra import models
from kickredis.config import KConfig

log = logging.getLogger("kicker.services")

db = redis.StrictRedis(host="127.0.0.1", decode_responses=True)


event_transport = RedisEventTransport(
    service_name="KickerService",
    consumer_name="KickerConsumer",
    stream_use=StreamUse.PER_EVENT,
)


class Column(models.Model):
    def get_db(self):
        return db

    name = models.CharHash()
    unit = models.CharHash()


class Attribute(models.Model):
    def get_db(self):
        return db

    name = models.CharHash()
    values = models.Set()


class AttributeAbleMixin:
    attributes = models.Set(to=Attribute)

    def attr_set(self, attr_name: str, attr_vals: set):
        pk = self._gen_attr_pk(attr_name)

        attr = Attribute(pk=pk, name=attr_name)

        self.attributes.sadd(attr)

        for v in attr_vals:
            attr.values.sadd(v)

    def attr_get(self, attr_name: str) -> set:
        for attr in self.attributes.smembers():
            if attr.name == attr_name:
                return set(attr.values.smembers())
        return None

    def __getattr__(self, name):
        val = self.attr_get(name)
        if val == None:
            self.__getattribute__(name)
        else:
            return val

    def _gen_attr_pk(self, attr_name):
        # class_name_lowecase = __class__.__name__.lower()
        class_name_lowecase = self.get_class_name()

        return f"{class_name_lowecase}##{self.pk}##{attr_name}"

        for strm in self.streams.smembers():
            if strm.name == stream_name:
                return strm


class Component(models.Model, AttributeAbleMixin):

    REDIS_STREAM_NAME_PREFIX = "KickerComponent"

    @staticmethod
    def get_class_name():
        return "component"

    def get_db(self):
        return db

    name = models.CharHash()
    description = models.CharHash()


class Stream(models.Model, AttributeAbleMixin):

    REDIS_STREAM_NAME_PREFIX = "KickerStream"

    @staticmethod
    def get_class_name():
        return "stream"

    def get_db(self):
        return db

    name = models.CharHash()
    description = models.CharHash()
    sensor_type = models.CharHash()
    units = models.CharHash()
    data_type = models.CharHash()
    rate = models.CharHash()
    min = models.IntegerHash()
    max = models.IntegerHash()

    class Status(Enum):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"
        FAULTY = "FAULTY"
        SLEEP = "SLEEP"
        ERROR = "ERROR"

        @classmethod
        def vals_as_list(cls):
            return [m.value for m in cls]

        def __str__(self):
            return self.name

    status = models.EnumHash(Status.vals_as_list(), default="ACTIVE")

    async def send_value(self, val):
        event_dict = {self.name: val}
        await event_transport.send_event(
            EventMessage(
                api_name=Stream.REDIS_STREAM_NAME_PREFIX,
                event_name=f"{self.pk}",
                id=f"{self.pk}",
                kwargs=event_dict,
            ),
            options={},
        )

    def consume(self, consumer_name: str):
        return event_transport.consume(
            [(Stream.REDIS_STREAM_NAME_PREFIX, f"{self.pk}")],
            consumer_name,
            error_queue=None,
        )

    async def acknowledge(self, msg):
        await event_transport.acknowledge(msg)


class Device(models.Model, AttributeAbleMixin):
    @staticmethod
    def get_class_name():
        return "device"

    def get_db(self):
        return db

    name = models.CharHash()
    uuid = models.CharHash()
    xbee_address = models.CharHash()
    streams = models.Set(to=Stream)
    components = models.Set(to=Component)

    def add_component(self, component_name: str) -> Component:
        stream_id = f"{self.pk}##{component_name}"
        strm = Component(pk=stream_id, name=component_name)
        self.components.sadd(strm)
        return strm

    def find_or_create_component_by_name(self, component_name):
        for strm in self.streams.smembers():
            if strm.name == component_name:
                return strm
        return self.add_component(component_name)

    def add_stream(self, stream_name: str) -> Stream:
        stream_id = f"{self.pk}##{stream_name}"
        strm = Stream(pk=stream_id, name=stream_name)
        self.streams.sadd(strm)
        return strm

    def find_or_create_stream_by_name(self, stream_name):
        for strm in self.streams.smembers():
            if strm.name == stream_name:
                return strm
        return self.add_stream(stream_name)

    def find_stream(self, predicate_fn):
        found_streams = []
        for strm in self.streams.smembers():
            if predicate_fn(strm):
                found_streams.append(strm)
        return found_streams

    @classmethod
    def find_iter(cls):
        for pk in db.scan_iter(match="astra::device*", _type="HASH"):
            yield cls(pk)


@dataclass
class QuestionHandle:
    id: str


class Question(models.Model, AttributeAbleMixin):
    @staticmethod
    def get_class_name():
        return "question"

    def get_db(self):
        return db

    query_str = models.CharHash()
    in_streams = models.Set(to=Stream)
    out_streams = models.Set(to=Stream)

    @staticmethod
    def from_handle(qh: QuestionHandle):
        return Question(pk=qh.id)

    def get_handle(self):
        return QuestionHandle(self.pk)

    def add_out_stream(self, stream_name: str) -> Stream:
        stream_id = f"{self.pk}##{stream_name}"
        strm = Stream(pk=stream_id, name=stream_name)
        self.out_streams.sadd(strm)
        return strm

    def find_in_stream_by_name(self, stream_name: str) -> Stream:
        return self._find_stream_by_name(stream_name, self.in_streams)

    def find_out_stream_by_name(self, stream_name: str) -> Stream:
        return self._find_stream_by_name(stream_name, self.out_streams)

    @staticmethod
    def _find_stream_by_name(stream_name, list_of_streams):
        for strm in list_of_streams.smembers():
            if strm.name == stream_name:
                return strm
        return None


class ObjectRegistry:
    def __init__(self, config: KConfig):
        self.config = config

    def add_device(self, dev_id: str) -> Device:
        dev = Device(pk=dev_id, name="")
        return dev

    def find_device(self, dev_id: str) -> Device:
        dev = Device(pk=dev_id)
        return dev


object_registry = ObjectRegistry(None)