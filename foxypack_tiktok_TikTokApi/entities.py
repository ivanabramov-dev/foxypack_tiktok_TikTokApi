from foxy_entities import SocialMediaEntity
from .utils import Proxy

class TikTokSession(SocialMediaEntity):
    ms_token: str
    browser: str
    proxy: Proxy | None