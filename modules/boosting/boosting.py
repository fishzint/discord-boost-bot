from email.mime import image
import disnake
from disnake.ext import commands
from typing import List
import httpx
import json
import base64
import datetime
from capmonster_python import HCaptchaTask
import asyncio

from definitions import ROOT_PATH, CAPMONSTER_API_KEY, X_SUPER_PROPERTIES, settings


class Boosting(commands.Cog, name="Boosting"):
    """Boosting commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.captchaSolver = HCaptchaTask(CAPMONSTER_API_KEY)

        self.stock: List[str] = json.load(
            open(f"{ROOT_PATH}/modules/boosting/stock.json", "r", encoding="utf-8")
        )
        self.stock30: List[str] = json.load(
            open(f"{ROOT_PATH}/modules/boosting/stock30.json", "r", encoding="utf-8")
        )
        self.failed: List[str] = json.load(
            open(f"{ROOT_PATH}/modules/boosting/failed.json", "r", encoding="utf-8")
        )
        self.used: List[str] = json.load(
            open(f"{ROOT_PATH}/modules/boosting/used.json", "r", encoding="utf-8")
        )

    @staticmethod
    def isAdmin(inter):
        return str(inter.author.id) in settings["BOT_OWNER_IDS"]

    @staticmethod
    def isWhitelisted(inter):
        return str(inter.author.id) in settings["botWhitelistedId"]


    def get_super_properties(self):
        properties = """{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","browser_version":"95.0.4638.54","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":102113,"client_event_source":null}"""
        properties = base64.b64encode(properties.encode()).decode()
        return properties

    def get_fingerprint(self, client):
        try:
            fingerprint = client.get(
                f"https://discord.com/api/v9/experiments", timeout=5
            ).json()["fingerprint"]
            return fingerprint
        except Exception as e:
            # print(e)
            return "Error"

    def get_cookies(self, client, url):
        try:
            cookieinfo = client.get(url, timeout=5).cookies
            dcf = str(cookieinfo).split("__dcfduid=")[1].split(" ")[0]
            sdc = str(cookieinfo).split("__sdcfduid=")[1].split(" ")[0]
            return dcf, sdc
        except:
            return "", ""

    def get_client(self, token):
        while True:
            client = httpx.Client()
            dcf, sdc = self.get_cookies(client, "https://discord.com/")
            fingerprint = self.get_fingerprint(client)
            if fingerprint != "Error":  # Making sure i get both headers
                break

        headers = {
            "authority": "discord.com",
            "method": "POST",
            "path": "/api/v9/users/@me/channels",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US",
            "authorization": token,
            "cookie": f"__dcfduid={dcf}; __sdcfduid={sdc}",
            "origin": "https://discord.com",
            "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-fingerprint": fingerprint,
            "x-super-properties": X_SUPER_PROPERTIES,
        }

        client.headers = headers

        return client

    def getSubscriptionSlots(self, client: httpx.Client, guildID: int) -> List[int]:
        r = client.get(
            "https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots"
        )

        jsonResponse = r.json()

        print(jsonResponse)

        # TODO proper error checking

        # if r.status_code != 200:
        #     print(f"Something went wrong while getting subscription slots, got response:\n{jsonResponse}")
        #     return False

        # if len(jsonResponse) < 1: return False

        return [
            subscriptionSlot["id"]
            for subscriptionSlot in jsonResponse
            if subscriptionSlot["premium_guild_subscription"] is None
        ]

    def joinServer(self, client: httpx.Client, inviteURL: str) -> bool:
        client.headers["content-type"] = "application/json"
        
        r = client.post(
            f"https://discord.com/api/v9/invites/{inviteURL.rsplit('/', maxsplit=1)[1]}"
        , json={})

        responseJson = r.json()

        print(responseJson)
        
        if "captcha_key" in responseJson:
            # if "You need to update your app to join this server." in responseJson["captcha_key"]:
            #     return False
            
            taskID = self.captchaSolver.create_task(
                website_key=responseJson["captcha_sitekey"],
                website_url="https://discord.com/",
            )
            captchaResponseJson = self.captchaSolver.join_task_result(taskID)
            jsonData = {
                "captcha_key": captchaResponseJson["gRecaptchaResponse"],
            }

            r = client.post(
                f"https://discord.com/api/v9/invites/{inviteURL.rsplit('/', maxsplit=1)[1]}",
                json=jsonData,
            )

            responseJson = r.json()

        return not "message" in responseJson and r.status_code == 200

    def getGuildData(self, inviteURL: str) -> None | dict:
        r = httpx.get(
            f"https://discord.com/api/v9/invites/{inviteURL.rsplit('/', maxsplit=1)[1]}"
        )

        # TODO proper error checking
        print(r.json())

        responseJson = r.json()

        if "message" in responseJson:
            return None

        # if r.status_code != 200:
        #     print(f"Something went wrong while getting guild info, got response:\n{r.json()}")
        #     return None

        return {
            "guildID": responseJson["guild"]["id"],
            "guildName": responseJson["guild"]["name"],
            "guildIconID": responseJson["guild"]["icon"],
            "nitroCount": responseJson["guild"]["premium_subscription_count"],
            "inviterUsernameTag": f"{responseJson['inviter']['username']}#{responseJson['inviter']['discriminator']}",
        }

    def boostServer(
        token, client: httpx.Client, guildID: int, subscriptionSlots: List[int]
    ) -> bool:
        jsonData = {"user_premium_guild_subscription_slot_ids": subscriptionSlots}

        r = client.put(
            f"https://discord.com/api/v9/guilds/{guildID}/premium/subscriptions",
            json=jsonData,
        )

        # print(r.json())

        return r.status_code == 201

    @commands.slash_command(name="stock")
    async def stock(self, inter: disnake.CommandInteraction) -> None:

        self.stock = json.load(
            open(f"{ROOT_PATH}/modules/boosting/stock.json", "r", encoding="utf-8")
        )
        self.stock30 = json.load(
            open(f"{ROOT_PATH}/modules/boosting/stock30.json", "r", encoding="utf-8")
        )

        embed = disnake.Embed(
            # timestamp=datetime.datetime.now(),
            colour=0xFF66CC,
            description=f"""
                **90 days stock -**

                **Tokens:** {len(self.stock)}
                **Boosts:** {len(self.stock) * 2}


                **30 days stock -**

                **Tokens:** {len(self.stock30)}
                **Boosts:** {len(self.stock30) * 2}
                """,
        )
        # embed.add_field(name="Available stock", value=f"""
        #         **Tokens:** `{len(self.stock)}`
        #         **Boosts:** `{len(self.stock) * 2}`
        #         """)
        # embed.set_author(name=chr(173), icon_url=inter.guild.icon.url)
        # embed.set_footer(text=inter.author, icon_url=inter.author.avatar.url)
        # embed.set_thumbnail(url=inter.guild.icon.url)
        # embed.set_thumbnail(url=inter.guild.icon.url)

        await inter.response.send_message(embed=embed)

    @commands.command(name="restock")
    async def restock(self, ctx: commands.Context) -> None:
        """Attach a .txt to restock"""
        if len(ctx.message.attachments) < 1:
            embed = disnake.Embed(
                title="No attachment added!",
                timestamp=datetime.datetime.now(),
                colour=0xFF0000,
            )

            return await ctx.send(embed=embed)

        await ctx.message.delete()

        # TODO check duplicates

        self.stock = json.load(
            open(f"{ROOT_PATH}/modules/boosting/stock.json", "r", encoding="utf-8")
        )

        for attachment in ctx.message.attachments:
            if attachment.__str__().endswith(".txt"):
                fileHandle = await attachment.read()
                self.stock += fileHandle.decode().splitlines()
            else:
                embed = disnake.Embed(
                    title="Invalid attachment!",
                    timestamp=datetime.datetime.now(),
                    colour=0xFFFF00,
                    description=attachment.__str__(),
                )

                return await ctx.send(embed=embed)

        json.dump(
            self.stock,
            open(f"{ROOT_PATH}/modules/boosting/stock.json", "w", encoding="utf-8"),
        )

        embed = disnake.Embed(
            title="Stock succesfully added!",
            timestamp=datetime.datetime.now(),
            colour=0x00FF00,
            description=f"Total stock: {len(self.stock) * 2} boosts",
        )

        await ctx.send(embed=embed)

    @commands.command(name="restock30")
    async def restock30(self, ctx: commands.Context) -> None:
        """Attach a .txt to restock"""
        if len(ctx.message.attachments) < 1:
            embed = disnake.Embed(
                title="No attachment added!",
                timestamp=datetime.datetime.now(),
                colour=0xFF0000,
            )

            return await ctx.send(embed=embed)

        await ctx.message.delete()

        # TODO check duplicates

        self.stock = json.load(
            open(f"{ROOT_PATH}/modules/boosting/stock30.json", "r", encoding="utf-8")
        )

        for attachment in ctx.message.attachments:
            if attachment.__str__().endswith(".txt"):
                fileHandle = await attachment.read()
                self.stock += fileHandle.decode().splitlines()
            else:
                embed = disnake.Embed(
                    title="Invalid attachment!",
                    timestamp=datetime.datetime.now(),
                    colour=0xFFFF00,
                    description=attachment.__str__(),
                )

                return await ctx.send(embed=embed)

        json.dump(
            self.stock,
            open(f"{ROOT_PATH}/modules/boosting/stock30.json", "w", encoding="utf-8"),
        )

        embed = disnake.Embed(
            title="Stock succesfully added!",
            timestamp=datetime.datetime.now(),
            colour=0x00FF00,
            description=f"Total stock: {len(self.stock) * 2} boosts",
        )

        await ctx.send(embed=embed)

    async def sendLogEmbed(
        self,
        inter: disnake.CommandInteraction,
        invite: str,
        usedTokens: list,
        failedTokens: list,
        boostAmount: int,
        guildData: dict,
    ) -> None:
        usedTokensString = "\n".join(usedTokens) if len(usedTokens) > 0 else usedTokens
        failedTokensString = (
            "\n".join(failedTokens) if len(failedTokens) > 0 else failedTokens
        )

        description = f"""
        > **Server name:** {guildData['guildName']}
        > **Buyer:** {guildData['inviterUsernameTag']}
        > **Guild id:** {guildData['guildID']}
        > **Server invite:** {invite}
        """

        if len(usedTokens) > 0:
            description += f"""
            **Tokens used:**
            ```
            {usedTokensString}
            ```
            """

        if len(failedTokens) > 0:
            description += f"""
            **Tokens failed:**
            ```
            {failedTokensString}
            ```
            """

        if len(usedTokens) * 2 >= boostAmount:
            colour = 0xFF66CC
        elif len(usedTokens) < 1:
            colour = 0xFF0000
        else:
            colour = 0xFF8C00

        footer = (
            f"Boosted {len(usedTokens) * 2}x successfully"
            if len(failedTokens) < 1
            else f"Boosted {len(usedTokens) * 2}x successfully, {len(failedTokens)} token(s) failed"
        )

        embed = disnake.Embed(
            timestamp=datetime.datetime.now(), colour=colour, description=description
        )
        embed.set_footer(
            text=footer,
            icon_url=f"https://cdn.discordapp.com/icons/{guildData['guildID']}/{guildData['guildIconID']}.webp",
        )

        await self.bot.logChannel.send(embed=embed)
        await inter.author.send(embed=embed)

    @commands.slash_command(name="boost")
    async def boost(
        self, inter: disnake.CommandInteraction, invite: str, amount: int
    ) -> None:
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(
                title = 'Access Denied', 
                description= 'Bitch nigga stop.' , 
                colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)
        

        self.stock = json.load(
            open(f"{ROOT_PATH}/modules/boosting/stock.json", "r", encoding="utf-8")
        )

        if len(self.stock) < 1 or len(self.stock) * 2 < amount:
            embed = disnake.Embed(
                title="No stock or insufficient stock for the requested amount!",
                timestamp=datetime.datetime.now(),
                colour=0xFF0000,
                description=f"Total stock: {len(self.stock) * 2} boosts",
            )

            return await inter.response.send_message(embed=embed, ephemeral=True)

        self.failed = json.load(
            open(f"{ROOT_PATH}/modules/boosting/failed.json", "r", encoding="utf-8")
        )

        guildData = self.getGuildData(invite)

        if guildData is None:
            # TODO add incorrect invite handler
            print(f"Incorrect invite: {invite}")
            return

        embed = disnake.Embed(
            title=f"Boosting {guildData['guildName']} {amount} times!",
            timestamp=datetime.datetime.now(),
            colour=0xFF0000,
            description="Please **wait** for a confirmation.",
        )

        await inter.response.send_message(embed=embed, ephemeral=True)

        totalBoosts = 0
        usedTokens = []
        failedTokens = []

        for token in self.stock:
            await asyncio.sleep(1)
            # client = self.generateClient(token)
            client = self.get_client(token)

            if not self.joinServer(client, invite):
                print("failed js", token)
                failedTokens.append(token)
                continue

            subscriptionSlots = self.getSubscriptionSlots(client, guildData["guildID"])

            if subscriptionSlots == []:
                print("failed ss", token)
                failedTokens.append(token)
                continue

            self.boostServer(client, guildData["guildID"], subscriptionSlots)

            usedTokens.append(token)

            totalBoosts += len(subscriptionSlots)

            if totalBoosts >= amount:
                break

        self.failed += failedTokens
        json.dump(
            self.failed,
            open(f"{ROOT_PATH}/modules/boosting/failed.json", "w", encoding="utf-8"),
        )

        self.used += usedTokens
        json.dump(
            self.used,
            open(f"{ROOT_PATH}/modules/boosting/used.json", "w", encoding="utf-8"),
        )

        json.dump(
            self.stock[len(usedTokens) + len(failedTokens) :],
            open(f"{ROOT_PATH}/modules/boosting/stock.json", "w", encoding="utf-8"),
        )

        await self.sendLogEmbed(
            inter, invite, usedTokens, failedTokens, amount, guildData
        )

    @commands.slash_command(name="boost30")
    async def boost30(
        self, inter: disnake.CommandInteraction, invite: str, amount: int
    ) -> None:
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(
                title = 'Access Denied', 
                description= 'Bitch nigga stop.' , 
                colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        self.stock = json.load(
            open(f"{ROOT_PATH}/modules/boosting/stock30.json", "r", encoding="utf-8")
        )

        if len(self.stock) < 1 or len(self.stock) * 2 < amount:
            embed = disnake.Embed(
                title="No stock or insufficient stock for the requested amount!",
                timestamp=datetime.datetime.now(),
                colour=0xFF0000,
                description=f"Total stock: {len(self.stock) * 2} boosts",
            )

            return await inter.response.send_message(embed=embed, ephemeral=True)

        self.failed = json.load(
            open(f"{ROOT_PATH}/modules/boosting/failed.json", "r", encoding="utf-8")
        )

        guildData = self.getGuildData(invite)

        if guildData is None:
            # TODO add incorrect invite handler
            print(f"Incorrect invite: {invite}")
            return

        embed = disnake.Embed(
            title=f"Boosting {guildData['guildName']} {amount} times!",
            timestamp=datetime.datetime.now(),
            colour=0xFF0000,
            description="Please **wait** for a confirmation.",
        )

        await inter.response.send_message(embed=embed, ephemeral=True)

        totalBoosts = 0
        usedTokens = []
        failedTokens = []

        for token in self.stock:
            await asyncio.sleep(1)
            # client = self.generateClient(token)
            client = self.get_client(token)

            if not self.joinServer(client, invite):
                print("failed js", token)
                failedTokens.append(token)
                continue

            subscriptionSlots = self.getSubscriptionSlots(client, guildData["guildID"])

            if subscriptionSlots == []:
                print("failed ss", token)
                failedTokens.append(token)
                continue

            self.boostServer(client, guildData["guildID"], subscriptionSlots)

            usedTokens.append(token)

            totalBoosts += len(subscriptionSlots)

            if totalBoosts >= amount:
                break

        self.failed += failedTokens
        json.dump(
            self.failed,
            open(f"{ROOT_PATH}/modules/boosting/failed.json", "w", encoding="utf-8"),
        )

        self.used += usedTokens
        json.dump(
            self.used,
            open(f"{ROOT_PATH}/modules/boosting/used.json", "w", encoding="utf-8"),
        )

        json.dump(
            self.stock[len(usedTokens) + len(failedTokens) :],
            open(f"{ROOT_PATH}/modules/boosting/stock30.json", "w", encoding="utf-8"),
        )

        await self.sendLogEmbed(
            inter, invite, usedTokens, failedTokens, amount, guildData
        )

    @commands.command(name="order")
    async def testEmbed(self, ctx: commands.Context,) -> None:
        
        description = f"""
        > **Roled Added:** <@&1001809466188115990>
        > **Feedback** <#1001809473561702501>
        > **Server invite:** https://discord.gg/fishub
        """
        

        embed = disnake.Embed(
            timestamp=datetime.datetime.now(), colour=0xFF66CC, description=description
        )
        embed.set_footer(
            text="Thank-you For buying from fishhub! You've been roled! ",
            icon_url="https://cdn.discordapp.com/attachments/1001809503869743114/1001809509754359878/fish_hu2b.png?size=4096",
        )
        await ctx.send(embed=embed)
        

def setup(bot: commands.Bot):
    bot.add_cog(Boosting(bot))
