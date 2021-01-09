import discord
from discord.ext import commands
from random import choice, randint, random
import json

class Fun(commands.Cog):

    def __innit__(self, client):
        self.client = client
        self.pins = []

    # Commands
    @commands.command()
    async def isikyok(self, ctx):
        """- Is IKY ok?"""
        await ctx.send('No, he is bored and wanted to do a bot smhmyhead')
    
    @commands.command(aliases=["fs"])
    async def findseed(self, ctx):
        """- Test your luck in Minecraft"""
        rigged_findseed = {
            564610598248120320: 90000
        }

        if ctx.author.id in rigged_findseed:
            total_eyes = rigged_findseed[ctx.author.id]
        else:
            total_eyes = sum([1 for i in range(12) if randint(1, 10) == 1])
        await ctx.send(
            f"{(ctx.message.author.mention)} -> your seed is a {total_eyes} eye"
        )
        
    @commands.command(aliases=["vfindseed", "visualfindseed", "vfs"])
    async def findseedbutvisual(self, ctx):
        """- Test your luck in Minecraft but visual."""
        emojis = {
            "{air}": "<:empty:754550188269633556>",
            "{frame}": "<:portal:754550231017979995>",
            "{eye}": "<:eye:754550267382333441>",
        }

        eyes = ["{eye}" if randint(1, 10) == 1 else "{frame}" for i in range(12)]
        sel_eye = 0
        portalframe = ""
        for row in range(5):
            for col in range(5):
                if ((col == 0 or col == 4) and (row != 0 and row != 4)) or (
                    (row == 0 or row == 4) and (col > 0 and col < 4)
                ):
                    sel_eye += 1
                    portalframe += eyes[sel_eye - 1]
                else:
                    portalframe += "{air}"
            portalframe += "\n"

        # replace placeholder with portal frame emoji
        for placeholder in emojis.keys():
            portalframe = portalframe.replace(placeholder, emojis[placeholder])

        e = discord.Embed(
            title="findseed but visual",
            description=f"Your seed looks like: \n\n{portalframe}",
            color=discord.Colour(0x38665E),
        )
        e.set_author(
            name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.send(embed=e)

    @commands.command(aliases=["vfsbp"])
    async def findseedbutvisualbutpipega(self, ctx):
        """- Test your luck in Minecraft but visual, and pipega."""
        emojis = {
            "{air}": "<:empty:754550188269633556>",
            "{frame}": "<:piog:797563853902446592>",
            "{eye}": "<:pepiga:797563870793039873>",
        }

        eyes = ["{eye}" if randint(1, 10) == 1 else "{frame}" for i in range(12)]
        sel_eye = 0
        portalframe = ""
        for row in range(5):
            for col in range(5):
                if ((col == 0 or col == 4) and (row != 0 and row != 4)) or (
                    (row == 0 or row == 4) and (col > 0 and col < 4)
                ):
                    sel_eye += 1
                    portalframe += eyes[sel_eye - 1]
                else:
                    portalframe += "{air}"
            portalframe += "\n"

        # replace placeholder with portal frame emoji
        for placeholder in emojis.keys():
            portalframe = portalframe.replace(placeholder, emojis[placeholder])

        e = discord.Embed(
            title="findseed but visual",
            description=f"Your seed looks like: \n\n{portalframe}",
            color=discord.Colour(0x38665E),
        )
        e.set_author(
            name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.send(embed=e)

    @commands.command()
    async def flip(self, ctx):
        """- Flip a coin."""
        await ctx.send(f"You got {choice(['heads', 'tails'])}!")

    @commands.command(aliases=["findgf"])
    async def findgirlfriend(self, ctx):
        """- Find your girlfriend"""
        await ctx.send(f"{choice(['In Walmart getting some snack to Neflix n Chill ', 'With another guy, get a new girlfied smhmyhead', 'You dont have LOL'])}")

    @commands.command(
        usage="(choice)",
        brief="- Rock Paper Scissors with the bot.",
        example="{prefix}rps rock",
    )
    async def rps(self, ctx, choice: str):
        choice = choice.lower()
        rps = ["rock", "paper", "scissors"]
        bot_choice = rps[randint(0, len(rps) - 1)]

        await ctx.send(
            f"You chose ***{choice.capitalize()}***."
            + f" I chose ***{bot_choice.capitalize()}***."
        )
        if bot_choice == choice:
            await ctx.send("It's a Tie!")
        elif bot_choice == rps[0]:

            def f(x):
                return {"paper": "Paper wins!", "scissors": "Rock wins!"}.get(
                    x, "Rock wins!"
                )

            result = f(choice)
        elif bot_choice == rps[1]:

            def f(x):
                return {"rock": "Paper wins!", "scissors": "Scissors wins!"}.get(
                    x, "Paper wins!"
                )

            result = f(choice)
        elif bot_choice == rps[2]:

            def f(x):
                return {"paper": "Scissors wins!", "rock": "Rock wins!"}.get(
                    x, "Scissors wins!"
                )

            result = f(choice)
        else:
            return
        if choice == "noob":
            result = "Noob wins!"
        await ctx.send(result)

    @commands.command()
    async def findsleep(self, ctx):
        """- See how long you sleep."""

        lessSleepMsg = [
            "gn, insomniac!",
            "counting sheep didn't work? try counting chloroform vials!",
            "try a glass of water",
            "some decaf coffee might do the trick!",
        ]

        moreSleepMsg = [
            "waaakeee uuuppp!",
            "are they dead or asleep? I can't tell.",
            "wake up, muffin head",
            "psst... coffeeee \\:D",
        ]

        sleepHrs = randint(0, 24)

        if sleepHrs == 0:
            await ctx.send(
                f"{ctx.author.mention} -> your sleep is 0 hours long - nice try :D"
            )
        elif sleepHrs <= 5:
            if sleepHrs == 1:
                s = ""
            else:
                s = "s"
            await ctx.send(
                f"{ctx.author.mention} -> your sleep is {sleepHrs} hour{s} long - {lessSleepMsg[randint(0, len(lessSleepMsg) - 1)]}"
            )
        else:
            await ctx.send(
                f"{ctx.author.mention} -> your sleep is {sleepHrs} hours long - {moreSleepMsg[randint(0, len(moreSleepMsg) - 1)]}"
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        bad_words = ["fair", "ⓕⓐⓘⓡ", "ɹıɐɟ", "justo", "adil"]
        fair = ""
        for word in bad_words:
            if word in message.content.lower().replace(" ", ""):
                fair += f"{word.title()} "
        if fair:
            try:
                await message.channel.send(fair)
            except UnboundLocalError:
                pass

    @commands.command()
    async def e(self, ctx):
        """- self explanitory"""
        await ctx.send('e')

def setup(client):
    client.add_cog(Fun(client))