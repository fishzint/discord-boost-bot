import disnake
from disnake.ext import commands
import os

from definitions import ROOT_PATH, GUILD_ID, BOT_TOKEN, LOG_CHANNEL


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=".",
            help_command=None,
            test_guilds=[GUILD_ID],
            intents=disnake.Intents.all(),
        )

        self.load_modules()

    def load_modules(self) -> None:
        for module_folder in os.listdir(f"{ROOT_PATH}\\modules"):
            for module in os.listdir(f"{ROOT_PATH}\\modules\\{module_folder}"):
                if module_folder == module[:-3]:
                    self.load_extension(f"modules.{module[:-3]}")
                    print(f"""
╔╗          ╔╗    ╔╗
║║          ║║    ║║
║║  ╔══╦══╦═╝╠══╦═╝║
║║ ╔╣╔╗║╔╗║╔╗║║═╣╔╗║
║╚═╝║╚╝║╔╗║╚╝║║═╣╚╝║
╚═══╩══╩╝╚╩══╩══╩══╝: {module}""")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await bot.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.playing, name="fishhub.rip"
            )
        )
        self.logChannel = self.get_channel(LOG_CHANNEL)
        print("""
 ╔═╗   ╔╗ ╔╗    ╔╗
 ║╔╝   ║║ ║║    ║║
╔╝╚╦╦══╣╚═╣╚═╦╗╔╣╚═╗╔═╦╦══╗
╚╗╔╬╣══╣╔╗║╔╗║║║║╔╗║║╔╬╣╔╗║
 ║║║╠══║║║║║║║╚╝║╚╝╠╣║║║╚╝║
 ╚╝╚╩══╩╝╚╩╝╚╩══╩══╩╩╝╚╣╔═╝
                       ║║
                       ╚╝""")

    @commands.Cog.listener()
    async def on_slash_command_error(
        self, inter: disnake.CommandInteraction, error: commands.CommandError
    ):
        """Global error handler"""

        print(error)

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CheckFailure):
            title = "You do not have permissions to use this command!"
        else:
            title = "Oh no! Something went wrong while running the command!"

        embed = disnake.Embed(title=title, color=0xFF0000)

        await inter.response.send_message(embed=embed, ephemeral=True)


if __name__ == "__main__":
    bot = Bot()
    bot.run(BOT_TOKEN)
