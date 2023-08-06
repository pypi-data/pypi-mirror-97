import asyncio
import os
from datetime import datetime

from aiounittest import AsyncTestCase

from dev_up import DevUpAPI, models, DevUpException


class TestPremium(AsyncTestCase):
    _loop = None

    URLS = [
        "google.com",
        "vk.com",
        "87.240.190.78"
    ]
    ERROR_URL = "dev-up.ru"
    LINK_CODE = "/4c251"
    USER_ID = 460908267

    @property
    def loop(self):
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    def setUp(self) -> None:
        self.TOKEN = os.environ['TOKEN']
        self.api = DevUpAPI(self.TOKEN, raise_validation_error=True, loop=self.loop)

    def get_event_loop(self):
        return self.loop

    def test_make_request(self):
        result = self.api.make_request("profile.get", dict())
        self.assertIn('response', result)

        self.api = DevUpAPI()
        result = self.api.make_request("profile.get", dict(key=self.TOKEN))
        self.assertIn('response', result)

    async def test_make_request_async(self):
        result = await self.api.make_request_async("profile.get", dict())
        self.assertIn('response', result, 'any')

        self.api = DevUpAPI()
        result = await self.api.make_request_async("profile.get", dict(key=self.TOKEN))
        self.assertIn('response', result, 'any')

    def test_get_web_info_exception(self):
        try:
            self.api.utils.get_web_info(self.ERROR_URL)
        except Exception as ex:
            self.assertIsInstance(ex, DevUpException)

    def test_profile_get(self):
        profile = self.api.profile.get()
        self.assertIsInstance(profile, models.ProfileGet)
        self.assertIsInstance(profile.response.req_datetime, datetime)
        self.assertIsInstance(profile.response.last_online_datetime, datetime)

    def test_profile_balance_buy_premium(self):
        input("> Проверь есть ли у тебя премиум")
        buy_premium = self.api.profile.buy_premium()
        self.assertIsInstance(buy_premium, models.ProfileBuyPremium)

    def test_profile_limit_buy(self):
        buy = self.api.profile.buy_limit(1)
        self.assertIsInstance(buy, models.ProfileBuyLimit)

    def test_get_balance_link(self):
        limit_buy = self.api.profile.get_balance_link(10, self.USER_ID)
        self.assertIsInstance(limit_buy, models.ProfileGetBalanceLink)

    def test_vk_get_stickers(self):
        stickers = self.api.vk.get_stickers(1)
        self.assertIsInstance(stickers, models.VkGetStickers)

    def test_vk_get_sticker_info(self):
        stickers = self.api.vk.get_sticker_info(54983)
        self.assertIsInstance(stickers, models.VkGetStickerInfo)

    def test_vk_get_apps(self):
        apps = self.api.vk.get_apps(1)
        self.assertIsInstance(apps, models.VkGetApps)

    def test_vk_get_groups(self):
        groups = self.api.vk.get_groups(1)
        self.assertIsInstance(groups, models.VkGetGroups)

    def test_utils_md5_generate(self):
        md5 = self.api.utils.md5_generate("text")
        self.assertIsInstance(md5, models.UtilsMD5Generate)

    def test_utils_get_server_time(self):
        server_time = self.api.utils.get_server_time()
        self.assertIsInstance(server_time, models.UtilsGetServerTime)
        self.assertIsInstance(server_time.response.datetime, datetime)

    def test_utils_create_short_link(self):
        short_link = self.api.utils.create_short_link("https://vk.com/lordralinc")
        self.assertIsInstance(short_link, models.UtilsCreateShortLink)
        self.assertIsInstance(short_link.response.create_datetime, datetime)

    def test_utils_notifications_links(self):
        short_link_not = self.api.utils.notifications_links(
            code=self.LINK_CODE,
            status=models.NotificationsLinksStatus.OFF
        )
        self.assertIsInstance(short_link_not, models.UtilsNotificationsLinks)

    def test_get_web_info(self):
        for url in self.URLS:
            info = self.api.utils.get_web_info(url)
            self.assertIsInstance(info, models.UtilsGetWebInfo)

    async def test_profile_get_async(self):
        profile = await self.api.profile.get_async()
        self.assertIsInstance(profile, models.ProfileGet)
        self.assertIsInstance(profile.response.req_datetime, datetime)
        self.assertIsInstance(profile.response.last_online_datetime, datetime)

    async def test_profile_balance_buy_premium_async(self):
        input("> Проверь есть ли у тебя премиум")
        buy_premium = await self.api.profile.buy_premium_async()
        self.assertIsInstance(buy_premium, models.ProfileBuyPremium)

    async def test_profile_limit_buy_async(self):
        limit_buy = await self.api.profile.buy_limit_async(1)
        self.assertIsInstance(limit_buy, models.ProfileBuyLimit)

    async def test_get_balance_link_async(self):
        buy = await self.api.profile.get_balance_link_async(10, self.USER_ID)
        self.assertIsInstance(buy, models.ProfileGetBalanceLink)

    async def test_vk_get_stickers_async(self):
        stickers = await self.api.vk.get_stickers_async(1)
        self.assertIsInstance(stickers, models.VkGetStickers)

    async def test_vk_get_sticker_info_async(self):
        stickers = await self.api.vk.get_sticker_info_async(54983)
        self.assertIsInstance(stickers, models.VkGetStickerInfo)

    async def test_vk_get_apps_async(self):
        apps = await self.api.vk.get_apps_async(1)
        self.assertIsInstance(apps, models.VkGetApps)

    async def test_vk_get_groups_async(self):
        groups = await self.api.vk.get_groups_async(1)
        self.assertIsInstance(groups, models.VkGetGroups)

    async def test_utils_md5_generate_async(self):
        md5 = await self.api.utils.md5_generate_async("text")
        self.assertIsInstance(md5, models.UtilsMD5Generate)

    async def test_utils_get_server_time_async(self):
        server_time = await self.api.utils.get_server_time_async()
        self.assertIsInstance(server_time, models.UtilsGetServerTime)
        self.assertIsInstance(server_time.response.datetime, datetime)

    async def test_utils_create_short_link_async(self):
        short_link = await self.api.utils.create_short_link_async("https://vk.com/lordralinc")
        self.assertIsInstance(short_link, models.UtilsCreateShortLink)
        self.assertIsInstance(short_link.response.create_datetime, datetime)

    async def test_utils_notifications_links_async(self):
        short_link_not = await self.api.utils.notifications_links_async(
            code=self.LINK_CODE,
            status=models.NotificationsLinksStatus.OFF
        )
        self.assertIsInstance(short_link_not, models.UtilsNotificationsLinks)

    async def test_get_web_info_async(self):
        for url in self.URLS:
            info = await self.api.utils.get_web_info_async(url)
            self.assertIsInstance(info, models.UtilsGetWebInfo)
