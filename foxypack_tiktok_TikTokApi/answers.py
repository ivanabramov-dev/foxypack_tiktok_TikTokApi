from enum import Enum

from foxypack.foxypack_abc.answers import (
    AnswersAnalysis,
    AnswersSocialContent,
    AnswersSocialContainer,
)


class TikTokEnum(Enum):
    profile = "profile"
    video = "video"


class TikTokAnswersAnalysis(AnswersAnalysis):
    code: str


class TikTokVideoAnswersStatistics(AnswersSocialContent):
    video_id: str
    description: str | None
    original: bool

    likes: int | None
    shares: int | None
    comments: int | None
    collects : int | None



class TikTokProfileAnswersStatistics(AnswersSocialContainer):
    profile_id: str
    verified: bool | None

    folowing: int | None
    videos: int | None
    friends: int | None

    description: str | None
