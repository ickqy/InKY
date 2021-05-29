import time


from discord.ext import commands
from random import randint


class MyHelpCommand(commands.MinimalHelpCommand):
    messages = [
        "As I say-",
        "Pogchampo",
        "F for PogChamp",
        "If you see this, you are a boomer",
        "Please leave me alone :]",
        "Chicken Nuggets, thats it",
        "imagine doing a bot cause you were bored, pathetic",
    ]

    def get_command_signature(self, command):
        return f"``{self.clean_prefix}{command.qualified_name} {command.signature}``"

    def get_ending_note(self) -> str:
        return self.messages[randint(0, len(self.messages) - 1)]


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.client.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(Help(bot))
