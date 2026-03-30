import re
import urllib.parse
from typing_extensions import override

from foxypack import FoxyAnalysis, DenialAnalyticsException
from foxypack_tiktok_TikTokApi.answers import (
    TikTokAnswersAnalysis,
    TikTokEnum,
)


class FoxyTikTokAnalysis(FoxyAnalysis):
    @staticmethod
    def clean_link(link: str) -> str:
        parsed = urllib.parse.urlparse(link)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    @staticmethod
    def get_type_content(link: str) -> str | None:
        parsed = urllib.parse.urlparse(link)
        path = parsed.path.rstrip('/')
        
        if re.match(r'/video/\d+', path):
            return TikTokEnum.video.value

        if re.match(r'@[^/]+$', path):
            return TikTokEnum.profile.value

        return None

    @staticmethod
    def get_code(link: str) -> str:
        parsed = urllib.parse.urlparse(link)
        return parsed.path.replace('@', '').replace('/', '')

    @override
    def get_analysis(self, url: str) -> TikTokAnswersAnalysis:
        type_content = self.get_type_content(url)

        if type_content is None:
            raise DenialAnalyticsException(url)

        return TikTokAnswersAnalysis(
            url=self.clean_link(url),
            social_platform="tiktok",
            type_content=type_content,
            code=self.get_code(url),
        )