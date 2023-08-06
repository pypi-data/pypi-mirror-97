from dataclasses import dataclass


@dataclass
class RedisConf:
    port: int = 6379
    host: str = "localhost"


@dataclass
class KConfig:
    redis: RedisConf


kicker_config = KConfig(RedisConf())
