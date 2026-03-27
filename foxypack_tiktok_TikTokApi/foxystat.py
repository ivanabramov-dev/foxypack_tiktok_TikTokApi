import asyncio

from foxy_entities import EntitiesController
from foxypack import (
    FoxyStat,
    InternalCollectionException,
    AnswersAnalysis,
)

from foxypack_tiktok_TikTokApi.answers import (
    TikTokAnswersAnalysis,
    TikTokProfileAnswersStatistics,
    TikTokVideoAnswersStatistics,
)


from typing import Union
from typing_extensions import override

TikTokStatistics = Union[TikTokProfileAnswersStatistics, TikTokVideoAnswersStatistics]



class FoxyTelegramStat(FoxyStat):
    def __init__(self, entities_controller: EntitiesController | None = None) -> None:
        self._entities_controller = entities_controller

    @override
    def get_statistics(self, answers_analysis: AnswersAnalysis) -> TikTokStatistics:
        return asyncio.run(self._get_statistics_async_internal(answers_analysis))

    @override
    async def get_statistics_async(
        self, answers_analysis: AnswersAnalysis
    ) -> TikTokStatistics:
        return await self._get_statistics_async_internal(answers_analysis)


    async def _get_statistics_async_internal(
        self,
        analysis: AnswersAnalysis,
    ) -> TikTokStatistics:
        pass