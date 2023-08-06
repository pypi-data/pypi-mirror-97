import logging
import asyncio
import lightbus.api

from kickredis.mock_analytics import MockAnalyticsService
from kickredis.granite.granite_analytics import GraniteAnalyticsService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d - %(name)s/%(threadName)s - %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

log = logging.getLogger("kicker.server")


async def runFlow():
    bus = lightbus.create()
    # bus.client.register_api(MockAnalyticsService())
    bus.client.register_api(GraniteAnalyticsService())
    await bus.client.start_worker()
    log.info("==== Kick Runtime Started ====")


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
