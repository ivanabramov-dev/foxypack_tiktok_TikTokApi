from foxy_entities import SocialMediaEntity


class TikTokSession(SocialMediaEntity):
    ms_token: str
    browser: str
    # proxy: str