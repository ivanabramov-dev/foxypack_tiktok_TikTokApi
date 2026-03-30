import asyncio

from datetime import datetime
from typing import Union
from typing_extensions import override

from foxy_entities import EntitiesController
from foxypack import (
    FoxyStat,
    InternalCollectionException,
    AnswersAnalysis,
)

from foxypack_tiktok_TikTokApi.answers import (
    TikTokProfileAnswersStatistics,
    TikTokVideoAnswersStatistics,
)
from foxypack_tiktok_TikTokApi.entities import TikTokSession
from foxypack_tiktok_TikTokApi.utils import as_tiktok_analysis

from TikTokApi import TikTokApi
# from proxyproviders.models.proxy import Proxy
# from proxyproviders import ProxyProvider


# ProxyProvider()

TikTokStatistics = Union[TikTokProfileAnswersStatistics, TikTokVideoAnswersStatistics]



class FoxyTikTokStat(FoxyStat):
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

    def _get_account(self) -> TikTokSession:
        if self._entities_controller is None:
            raise InternalCollectionException

        return self._entities_controller.get_entity(TikTokSession)

    @staticmethod
    def _parse_tiktok_video(
        analysis: AnswersAnalysis,
        data: dict
        ) -> TikTokVideoAnswersStatistics:
        video_id = data.get("id")
        description = data.get("desc")

        create_time = data.get("createTime")
        publish_date = (
            datetime.fromtimestamp(int(create_time)).date()
            if create_time
            else None
        )

        stats = data.get("stats", {})

        likes = int(stats.get("diggCount")) if stats.get("diggCount") else None
        shares = int(stats.get("shareCount")) if stats.get("shareCount") else None
        comments = int(stats.get("commentCount")) if stats.get("commentCount") else None
        collects = int(stats.get("collectCount")) if stats.get("collectCount") else None
        views = int(stats.get("playCount")) if stats.get("playCount") else 0

        original = data.get("originalItem", False)

        title = description or "TikTok video"

        return TikTokVideoAnswersStatistics(
            system_id=str(video_id),
            title=title,
            views=views,
            publish_date=publish_date,
            analysis_status=analysis, 

            video_id=str(video_id),
            description=description,
            original=original,

            likes=likes,
            shares=shares,
            comments=comments,
            collects=collects,
        )

    @staticmethod
    def _parse_tiktok_profile(
        analysis: AnswersAnalysis,
        data: dict
        ) -> TikTokProfileAnswersStatistics:
        user_info = data.get("userInfo", {})
        user = user_info.get("user", {})
        stats = user_info.get("stats", {})

        return TikTokProfileAnswersStatistics(
            system_id="tiktok",
            title=user.get("nickname", ""),
            subscribers=stats.get("followerCount", 0),
            creation_date=None,
            analysis_status=analysis,

            profile_id=user.get("id", ""),
            verified=user.get("verified"),

            folowing=stats.get("followingCount"),
            videos=stats.get("videoCount"),
            friends=stats.get("friendCount"),

            description=user.get("signature"),
        )

    async def _get_statistics_async_internal(
        self,
        analysis: AnswersAnalysis,
    ) -> TikTokStatistics:
        analysis = as_tiktok_analysis(analysis)

        tik_tok_session = self._get_account()

        if analysis.type_content == "profile":
            async with TikTokApi() as api:
                await api.create_sessions(
                    ms_tokens=[tik_tok_session.ms_token],
                    num_sessions=1,
                    sleep_after=3,
                    browser=tik_tok_session.browser,
                    # proxies=[tik_tok_session.proxy] if tik_tok_session.proxy else None,
                )
                
                profile = api.user(
                    analysis.code
                )
                
                data = await profile.info()

                return self._parse_tiktok_profile(analysis, data)
            
        if analysis.type_content == "video":
            async with TikTokApi() as api:
                await api.create_sessions(
                    ms_tokens=[tik_tok_session.ms_token],
                    num_sessions=1,
                    sleep_after=3,
                    browser=tik_tok_session.browser,
                    # proxies=[tik_tok_session.proxy] if tik_tok_session.proxy else None,
                )
                
                video = api.video(
                    url=analysis.url
                )

                data = await video.info()

                return self._parse_tiktok_video(analysis, data)

        raise ValueError(f"Unsupported tiktok content type: {analysis.type_content}")