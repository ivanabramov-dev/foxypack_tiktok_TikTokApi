from foxypack import AnswersAnalysis

from foxypack_tiktok_TikTokApi.answers import TikTokAnswersAnalysis


class Proxy:
    server : str
    username : str | None
    password : str | None

    def to_dict(self) -> dict:
        
        if self.username and self.password:
            return {
                "server": self.server,
                "username": self.username,
                "password": self.password
            }
        else:
            return {
                "server": self.server
            }


def as_tiktok_analysis(
    analysis: AnswersAnalysis,
) -> TikTokAnswersAnalysis:
    if not isinstance(analysis, TikTokAnswersAnalysis):
        raise TypeError("Analysis is not TikTokAnswersAnalysis")

    return analysis