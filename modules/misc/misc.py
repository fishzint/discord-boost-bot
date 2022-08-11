import disnake
from disnake.ext import commands

from definitions import settings

class Misc(commands.Cog, name="Misc"):
    """Misc commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @staticmethod
    def isAdmin(inter):
        return str(inter.author.id) in settings["BOT_OWNER_IDS"]

    @staticmethod
    def isWhitelisted(inter):
        return str(inter.author.id) in settings["botWhitelistedId"]
    
    
    @commands.slash_command(name="help", description="Simple help command that shows all of the available commands and what they do.")
    async def help(self, inter: disnake.CommandInter):
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        embed=disnake.Embed(
            title = 'Command Help', 
            colour=0xDB324D,
            description= 
                            f"\n```/boost: Boosts the given server https Invite.\n"
                            f"/restock: Uses a pastebin code to restock the boosting bot with tokens/text entered.\n"
                            f"/restock: Uses a pastebin code to restock the boosting bot with tokens/text entered.\n"
                            f"/stock30: Shows a simple look of how much Three month tokens you have inside of the bot.\n"
                            f"/stock: Shows a simple look of how much tokens you have inside of the bot.\n"
                            f"/whitelist: Command to whitelist users to use the boosting bot. This is limited to only the admins of the bot.\n"
                            f"/card: Command for Nitro services, sends an embed with the card number and cvc for buyers.\n" 
                            f"/btc: Simple payment command for BTC payments.\n" 
                            f"/ltc: Simple payment command for LTC payments.\n" 
                            f"/solana: Simple payment command for Solana payments.\n" 
                            f"/cashapp: Simple payment command for Cashapp payments.\n" 
                            f"/zelle: Simple payment command for Zelle payments.\n" 
                            f"/venmo: Simple payment command for Venmo payments.\n" 
                            f"/disarray: Sends instructions on how to register/use a Disarray key.\n"
                            f"/role: Roles a given user to a given role. Simple as that.\n" 
                            f"/vouch: Sends a simple vouch command for a given buyer, mentions them outside of embed```\n \n"
                            f"If you would like any more help, please contact **fishhub support**"
                            )
        return await inter.response.send_message(embed=embed)

    @commands.slash_command(name="card", description="Sends the VCC info for the nitro services.")
    async def nitrocard(
        self,
        inter: disnake.CommandInteraction,
        vcc: str,
        cvc: str,
    ):
        """
        general command info
        
        Parameters
        ----------
        vcc: VCC card
        cvc: CVC
        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        embed=disnake.Embed(
            colour=0xf47fff,
            description=
                            f"**Card Information**\n"
                            f"> *Card Number*: **4183 4220 {vcc}**\n"
                            f"> *Expiration Date*: **03/24**\n"
                            f"> *CVC*: **{cvc}**\n"
                            f"> *Name on Card*: **Kemal Kemal**\n\n"
                            f"> *Country*: **Turkey**\n"
                            f"> *Address*: **istanbul**\n"
                            f"> *City*: **istanbul**\n"
                            f"> *State*: **istanbul**\n"
                            f"> *Postcode*: **34000**\n\n"
                            f"**What Now?**\n"
                            f"> *Step I*: **Add the payment method from above.**\n"
                            f"https://i.imgur.com/zEo2rhU.png\n\n"
                            f"> *Step II*: **Buy your subscription from Discord Nitro tab.**\n"
                            f"https://i.imgur.com/a1pnSgo.png\n\n"
                            f"> *Step III*: **Open extra Discord tab from your browser or mobile to be able to "
                            f"see my messages to confirm your payment.**\n"
                            f"https://i.imgur.com/lNsMFlB.png\n\n"
                            f"**Must know**\n"
                            f"Do not use vpn.\n"
                            f"Do not use any extra program.\n"
                            f"Do not try to gift it.\n"
                            f"Just buy it through ''subscribe'' button.\n"
                            f"Just buy it like you usually do."
                            )
        return await inter.response.send_message(embed=embed)
        
    @commands.slash_command(name="btc", description="Sends a Bitcoin payment message for a buyer.")
    async def btcpay(
        self,
        inter: disnake.CommandInteraction,
        amount: str,
        person: disnake.Member
    ):
        """
        general command info
        
        Parameters
        ----------
        amount: Amount the buyer pays
        person: Buyer's mention
        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        await inter.send(f'{person.mention} please send `${amount} USD` to: **bc1qc0zk7elze377thlnvm5l6gejtsky5jzgvwltlf**.')
    
    @commands.slash_command(name="paypal", description="Sends a paypal payment message for a buyer.")
    async def paypal(
        self,
        inter: disnake.CommandInteraction,
        amount: int,
        person: disnake.Member
    ):
        """
        general command info
        
        Parameters
        ----------
        amount: Amount the buyer pays
        person: Buyer's mention
        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'Bitch nigga stop.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        await inter.send(f'{person.mention} please send `${amount} USD` as friends & family to: **fishapbc@gmail.com**.')   

    @commands.slash_command(name="ltc", description="Sends a Litecoin payment message for a buyer.")
    async def ltcpay(
        self,
        inter: disnake.CommandInteraction,
        amount: str,
        person: disnake.Member
    ):
        """
        general command info
        
        Parameters
        ----------
        amount: Amount the buyer pays
        person: Buyer's mention
        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        await inter.send(f'{person.mention} please send `${amount} USD` to: **LarT172RV7zQyTNJa5ejfUFppGA52qCyUB**.')

    @commands.slash_command(name="solana", description="Sends a Solana payment message for a buyer.")
    async def solpay(
        self,
        inter: disnake.CommandInteraction,
        amount: str,
        person: disnake.Member
    ):
        """
        general command info
        
        Parameters
        ----------
        amount: Amount the buyer pays
        person: Buyer's mention
        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        await inter.send(f'{person.mention} please send `${amount} USD` to: **9nmnNWXTfUikbyTNewYDJ1D8VHvaqUkuPko1fEfFCxGq**.')

    @commands.slash_command(name="venmo", description="Sends a Venmo payment message for a buyer.")
    async def venmo(
        self,
        inter: disnake.CommandInteraction,
        amount: str,
        person: disnake.Member
    ):
        """
        general command info
        
        Parameters
        ----------
        amount: Amount the buyer pays
        person: Buyer's mention
        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        await inter.send(f'{person.mention} please send `${amount} USD` to: **@TrioHCF**.')

    @commands.slash_command(name="zelle", description="Sends a Zelle payment message for a buyer.")
    async def zelle(
        self,
        inter: disnake.CommandInteraction,
        amount: str,
        person: disnake.Member
    ):
        """
        general command info
        
        Parameters
        ----------
        amount: Amount the buyer pays
        person: Buyer's mention
        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        await inter.send(f'{person.mention} please send `${amount} USD` to: **fishfacefamm@gmail.com**.')

    @commands.slash_command(name="cashapp", description="Sends a Cashapp payment message for a buyer.")
    async def cashapp(
        self,
        inter: disnake.CommandInteraction,
        amount: str,
        person: disnake.Member
    ):
        """
        general command info
        
        Parameters
        ----------
        amount: Amount the buyer pays
        person: Buyer's mention
        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        await inter.send(f'{person.mention} please send `${amount} USD` to: **$fishzint**.')

    @commands.slash_command(name="disarray", description="Sends a message on how to register/use a Disarray key.")
    async def disarray(
    self, 
    inter: disnake.CommandInter, 
    key: str
    ):
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        embed=disnake.Embed(
            colour=0xEDF7F6,
            description=
                            f"1. Make a account on (if you dont have one already): https://disarray.pro/\n"
                            f"2. Head over to: https://disarray.pro/profile \n"
                            f"3. Redeem the following key: `{key}`"
    )
        return await inter.response.send_message(embed=embed)


    @commands.slash_command(name="lastcheat", description="Sends a message on how to register/use a Disarray key.")
    async def lastcheat(
    self, 
    inter: disnake.CommandInter, 
    key: str
    ):
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        embed=disnake.Embed(
            colour=0xEDF7F6,
            description=
                            f"1. Activate your key at: https://licensing.pw/\n"
                            f"2. Loader: https://download.licensing.pw/ \n"
                            f"3. Redeem the following key: `{key}`"
    )
        return await inter.response.send_message(embed=embed)


    

    @commands.slash_command(name="vouch", description="Sends a message on how to vouch.")
    async def vouch(
        self,
        inter: disnake.CommandInteraction,
    ):
        """
        general command info
        
        Parameters
        ----------
        user: Buyer's mention
        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        embed=disnake.Embed(
            colour=0xDB324D,
            description=
                             f"Thank you for buying one of our products! If you would like to vouch for us, please head into <#1001809473561702501>\n\n"
                            f"We appreciate you supporting our small business, and it would mean a lot if you check out our website: https://fishhub.rip, and check around the site.\n\n"
                            f"If you have any more questions for us, we don't mind them! We will help you to the best of our capabilities.\n\n"
                            f"On Site Profiles :\n\n"
                            f"**https://ogu.gg/**: https://ogu.gg/zeroninty\n\n"
                            f"**https://hackforums.net/**: https://hackforums.net/member.php?action=profile&uid=5171018\n\n"
                            f"**https://cracked.io/**: https://cracked.io/fishzint\n\n"
        )
        return await inter.response.send_message(embed=embed)

    @commands.slash_command(name="exchange", description="Says the Exchange Rates")
    async def exchange(self, 
    inter: disnake.CommandInter
    ):

        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(
                title = 'Access Denied', 
                description= 'Bitch nigga stop.' , 
                colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        embed=disnake.Embed(
            colour=0xDB324D,
            title= 
            f"**fishhub Exchange Rates and Fees:**",
            description=
                            f"**Exchange rates and fees**\n"
                            f"**Note: All fees are fixed and not negotiable**\n"
                            f"**$10 minimum on all exchanges**\n"
                            f"**Cashapp Exchange (Balance only)**\n"
                            f"• Cashapp -> Crypto 7%\n"
                            f"• Crypto -> Cashapp 7%\n"
                            f"**PayPal Exchange (Balance F&F only)**\n"
                            f"• PayPal -> Crypto 10%\n"
                            f"• Crypto -> PayPal 10%\n"
                            f"**Apple Pay**\n"
                            f"• Apple Pay -> Crypto 10%\n"
                            f"• Crypto -> Apple Pay 10%\n"
                            f"**Zelle Exchange**\n"
                            f"• Zelle -> Crypto 10%\n"
                            f"• Crypto -> Zelle 10%\n"
                            f"**US Bank Transfer**\n"
                            f"• Crypto -> USBT 10%\n"
                            f"**DO NOT OPEN TICKET AND COMPLAIN ABOUT FEES**"
        )
        return await inter.response.send_message(embed=embed)

    @commands.slash_command(name="mm-rates", description="Says the middleman Rates")
    async def rates(self, 
    inter: disnake.CommandInter
    ):

        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(
                title = 'Access Denied', 
                description= 'Bitch nigga stop.' , 
                colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        embed=disnake.Embed(
            colour=0xDB324D,
            title= 
            f"**fishhub Middle Man Info:**",
            description=
                            f"**Rates & Fees**\n"
                            f"**Note: All fees are fixed and not negotiable**\n"
                            f"**$5%, $5 minnimum fee**\n"
                            f"**• We Will MM anything with monetary value**\n"
                            f"• The Middle Man fee is not refundable when paid\n"
                            f"• Our only role is to hold the funds and send the funds when both parties are ready.\n"
                            f"**• We arenot responsible for anything that happens before, during or after the deal has taken place. (pullback, banned etc)**\n"
                            f"**DO NOT OPEN TICKET AND COMPLAIN ABOUT FEES**"
        )
        return await inter.response.send_message(embed=embed)


    @commands.slash_command(name="payments", description="Says the available payment methods")
    async def payments(self, 
    inter: disnake.CommandInter
    ):

        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(
                title = 'Access Denied', 
                description= 'You are not whitelisted.' , 
                colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        embed=disnake.Embed(
            colour=0xDB324D,
            title= 
            f"fishhub accepted payment methods:",
            description=
                            f"Cash App\n"
                            f"Venmo\n"
                            f"Zelle\n"
                            f"Paypal\n"
                            f"Bitcoin\n"
                            f"Ethereum\n"
                            f"Dodgecoin\n"
                            f"Bitcoin Cash\n"
                            f"ApeCoin\n"
                            f"Dai\n"
                            f"Tether\n"
                            f"USD Coin\n"
                            f"Shiba Inu\n"
                            f"+ more major cryptos! Don't worry about asking us if we accept a coin you would like to pay with!"
        )
        return await inter.response.send_message(embed=embed)

    @commands.slash_command(name="role", description="Sets the role for a user.")
    async def role(
        self,
        inter: disnake.CommandInteraction,
        person: disnake.Member,
        role: disnake.Role
    ):
        """
        general command info
        
        Parameters
        ----------
        person: Buyer's mention
        role: Role to add

        """
        if not self.isWhitelisted(inter):
            noperms=disnake.Embed(title = 'Access Denied', description= 'You are not whitelisted.' , colour=disnake.Colour.red())
            return await inter.response.send_message(embed=noperms)

        await person.add_roles(role)
    
def setup(bot: commands.Bot):
    bot.add_cog(Misc(bot))
    
