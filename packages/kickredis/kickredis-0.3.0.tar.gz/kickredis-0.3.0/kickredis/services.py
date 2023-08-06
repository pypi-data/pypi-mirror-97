import logging
import asyncio
import lightbus.api

from kickredis.registry import Question, QuestionHandle


log = logging.getLogger("kicker.services")


class AnalyticsService(lightbus.Api):
    def __init__(self):
        self.qn = 0
        self.questions_map = {}

    class Meta:
        name = "AnalyticsService"

    async def new_question(self, query, is_start) -> QuestionHandle:
        log.debug("new_question")
        q: Question = self._parse_question_from_str(query)

        return await self.run_question(q)

    async def run_question(self, q):
        log.debug("run_question")
        task = asyncio.create_task(q.run())
        self.questions_map[q.pk] = task
        return q.get_handle()

    def _parse_question_from_str(self, query: str) -> Question:
        pass

    def _gen_id(self) -> str:
        self.qn += 1
        return f"q_id_{self.qn}"
