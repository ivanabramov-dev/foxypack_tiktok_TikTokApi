from foxy_entities import EntitiesController
from foxypack import FoxyPack
from foxypack_tiktok_TikTokApi.entities import (
    TikTokSession)

from foxypack_tiktok_TikTokApi.foxyanalysis import FoxyTikTokAnalysis
from foxypack_tiktok_TikTokApi.foxystat import FoxyTikTokStat

parser = FoxyPack().with_foxy_analysis(
    FoxyTikTokAnalysis()
)

print(parser.get_analysis("https://www.tiktok.com/@andruhatrutata/"))


session = TikTokSession(
    ms_token="s5d_lPEGCdwHm8DCZSDHZ9G1zQzDl6LdqhSffaWSxZAKPrOH3HHWpe6wjupnHNxFlxwA29FD8I2KEe58znOVEsX3lYr27jFfSfS5kfpP4WtIg7w7oBgRATXEUrc-TyrheaMFKIis03f5",
    browser="chromium",
)

controller = EntitiesController()
controller.add_entity(session)

parser = parser.with_foxy_stat(
    FoxyTikTokStat(entities_controller=controller)
)

print(parser.get_statistics("https://www.tiktok.com/@andruhatrutata/"))