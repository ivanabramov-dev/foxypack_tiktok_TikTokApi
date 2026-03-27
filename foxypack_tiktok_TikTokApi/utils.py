from foxypack import AnswersAnalysis

from foxypack_tiktok_TikTokApi.answers import TikTokAnswersAnalysis


def as_tiktok_analysis(
    analysis: AnswersAnalysis,
) -> TikTokAnswersAnalysis:
    if not isinstance(analysis, TikTokAnswersAnalysis):
        raise TypeError("Analysis is not TikTokAnswersAnalysis")

    return analysis