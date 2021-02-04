import discord
import asyncio
import json
import requests
from discord.ext import commands
from random import choice, randint, random
from .utilities.barter import Piglin

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.pins = []
    
    # Commands
    @commands.command(aliases=["fs"])
    async def findseed(self, ctx):
        """`Test your Minecraft RNG, but in a bot command`"""
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
        """`Test your Minecraft RNG, but you can physaclly see it`"""
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
        """`Test your Minecraft RNG, but you can physaclly see it, and its pipega.`"""
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
            color=discord.Colour(0xF4ABBA),
        )
        e.set_author(
            name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.send(embed=e)

    @commands.command(aliases=["vfsbpog"])
    async def findseedbutvisualbutpog(self, ctx):
        """`Test your Minecraft RNG, but you can physaclly see it,and its pog.`"""
        emojis = {
            "{air}": "<:empty:754550188269633556>",
            "{frame}": "<:pog:798221486803779584>",
            "{eye}": "<:pogmouth:798224025272844288>",
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
            color=discord.Colour(0xD78369),
        )
        e.set_author(
            name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.send(embed=e)

    @commands.command()
    async def flip(self, ctx):
        """`Flip a coin, thats it`"""
        await ctx.send(f"You got {choice(['heads', 'tails'])}!")

    @commands.command(
        usage="(choice)",
        brief="`The Classic Paper Rock Sccicors game, but with no friends, instead its with the bot`",
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
        """`See how long you sleep, this is 100% true I swear`"""

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
        if not message.guild:
            return
        if message.author.bot:
            return
        if (
            "<@!730042011931115560>" in message.content
            or "<@730042011931115560>" in message.content
        ):
            await message.channel.send("<a:angryloikingping:798242294816964658>")

    @commands.command()
    async def e(self, ctx):
        """`If you say e, I say e, yes`"""
        await ctx.send('e')

    @commands.command(aliases=["piglin"])
    async def barter(self, ctx):
        """`Barter with Minecraft's Piglin. (Based on JE 1.16.1, before nerf)`"""
        trade = Piglin()
        e = discord.Embed(
            title = "Bartering with Piglin...",
            description = "You got {} {}!".format(trade.quantity, trade.item),
            colour = discord.Colour.gold()
        )
        e.set_author(
            name=f"{ctx.message.author}",
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.send(embed=e)

    @commands.command()
    async def joke(self, ctx):
        """`Ask the bot a joke and he will tell you a joke that will defenetly make you laugh no cap`"""
        data = requests.get('https://official-joke-api.appspot.com/jokes/random').json()
        embed = discord.Embed(title = data['setup'], description = data['punchline'], color = 0xf4565a)
        await ctx.send(embed=embed)

    @commands.command(aliases = ['guess', 'gtn', 'guessnum'])
    async def guessthenumber(self, ctx):
        """`Guess the number, why did you even do help guess if its self explanitory`"""
        number = randint(1, 100)
        guess = False
        for i in range(1, 86):
            if i == 11:
                await ctx.send("The game is over and you lost.")
                return
            await ctx.send(f'Guess the number! Pick from 1 to 100 and get some hints! This is attempt #{i}.')
            response = await self.client.wait_for('message', check = lambda message: message.author == ctx.author)
            try:
                guess = int(response.content)
            except ValueError:
                await ctx.send("That was not a number. Systems failing..... game aborted")
                break
            if guess > number:
                await ctx.send('The number is smaller than that.')
            elif guess < number:
                await ctx.send('The number is bigger than that')
            else:
                await ctx.send(f'You got it! It took you {i} attempts.')
                guess = True
                break
        if not guess:
            await ctx.send(f"The number was {number}, too bad.")

    @commands.command(aliases=['random'])
    async def rng(self, ctx, minimum: int, maximum: int):
        """`Choose a minimum and a maximum number and the bot will choose a random number`"""
        await ctx.send(randint(minimum, maximum))

    @commands.command()
    async def roll(self, ctx, pool):
        """`Roll the dice`"""
        await ctx.send(f"You rolled a {randint(0, int(pool))}")

    @commands.command(aliases=["8ball"])
    async def ballofwisdom(self, ctx, *, question):
        """Ask the Magic 8Ball your question,a nd he will answer correctly no cap"""
        responses = ["It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."]
        
        e = discord.Embed(
        title=f"🎱  {question}?",
        colour=discord.Colour(0x603593),
        description=choice(responses),
        )
        
        await ctx.send(embed=e)

    @commands.command(aliases=["isimposter"], usage="[impostor count] [player count]")
    async def isimpostor(self, ctx, impostor: int = 1, player: int = 10):
        """Check if you're an impostor or a crewmate."""
        if 3 < impostor < 1:
            await ctx.send("Impostor counter can only be up to 3 impostors")
            return
        chance = 100 * impostor / player / 100
        if random() < chance:
            await ctx.send(f"{ctx.author.mention}, you're a crewmate!")
        else:
            await ctx.send(f"{ctx.author.mention}, you're an impostor!")

    @commands.command()
    async def roast (self, ctx, member: discord.Member = None):
        roast = ["You're as useless as the 'ueue' in 'queue'",
        "If I had a face like yours, I'd sue my parents",
        "Some day you'll go far... and I hope you stay there",
        "You must have been born on a highway cos' that's where most accidents happen",
        "If i had a dollar for every time you said something smart, I'd be broke",
        "When you were born the doctor threw you out the window and the window threw you back",
        "If your brain was dynamite, there wouldn’t be enough to blow your hat off",
        "Your face makes onions cry",
        "I thought of you today, it reminded me to take out the trash",
        "When karma comes back to punch you in the face, I want to be there in case it needs help",
        "I thought I had the flu, but then I realized your face makes me sick to my stomach",
        "You're like Mondays, everyone hates you",
        "Keep rolling your eyes, you might find a barain baxck there",
        "My phone battery lasts longer than your relationships, and my battery only lasts less than an hour FYI",
        "I never forget a face, but in your case I would love to make an exception...",
        "You're so ugly when you look in the mirror your reflection looks away",
        "You're so ugly when you were born, the doctor said aww what a treasure and your mom said yeah lets bury it",
        "Maybe you should eat make-up so you’ll be pretty on the inside too",
        "When you were born, the doctor came out to the waiting room and said to your dad, I'm very sorry. We did everything we could. But he pulled through",
        "It’s a shame you can’t Photoshop your personality",
        "Whoever told you to be yourself gave you really bad advice",
        "If you could use 100 percent of your brain's power, you'd still be incredibly stupid. 100 percent of nothing is still nothing",
        "Go ahead, tell us everything you know. It'll only take ten seconds",
        "It’s not Halloweeen - take your mask off",
        "You have a face like a smoke alarm. Beat at it until it sounds off",
        "I never saw anybody take so long to type, and with such little result",
        "My hair straightener is hotter than you",
        "I’d explain it to you but I left my English-to-Dumbass Dictionary at home",
        "I don't exactly hate you, but if you were on fire and I had water, I'd drink it",
        "I'd love to insult you, but I'm afraid I cannot perform as well as nature did",
        "Everyone brings happiness to a room. I do when I enter, you do when you leave",
        "The zoo called. They're wondering how you got out of your cage",
        "I suggest you do a little soul searching. You might just find one",
        "I’m visualizing duck tape over your mouth",
        "You should use a glue stick instead of chapstick",
        "I love what you have done to your hair/ How'd you get it to come so far of your nostrils?",
        "I would roast you, but my mom said not to burn trash",
        "I'm not saying I hate you, but I would unplug your life support to charge my phone",
        "If tour family were Starwars figures, you'd be the special edition",
        "Over watching paint dry and listening to you, I choose watching paint dry",
        "If you uploaded a video to Youtube with your face, it would get demonetized for `Harmful or dangerous content`",
        "Life is great, you should get one",
        "Fake hair, fake nails, fake smile. Are you sure you weren't made in China?",
        "Your face looks like something I would draw with my non dominant hand.",
        "You're kind of like Rapunzel except instead of letting down your hair, you let down everyone in your life.",
        "I'd agree with you but then we'd both be wrong.",
        "Brains aren't everything, in fact in your case they're nothing.",
        "Why is it acceptable for you to be an idiot but not for me to point it out?",
        "Aww, it’s so cute when you try to talk about things you don’t understand.",
        "At least when I do a handstand my stomach doesn't hit me in the face.",
        "My hair straightener is hotter than you.",
        "If you’re going to be a smart ass, first you have to be smart, otherwise you’re just an ass.",
        "People like you are the reason why people like us need meds and therapy.",
        "Some people drink from the fountain of knowledge - it appears that you merely gargled",
        "When I see your face theres not a thing I would change... Except for the direction im walking in",
        "You sound reasonable... Time to up my medication",
        "I bet your brain feels as good as new, seeing that you never use it",
        "Did your parents ever ask you to run away from home?",
        "Hey, I found your nose, it’s in my business again!",
        "Is your butt jealous of the amount of crap that just came out of your mouth?",
        "Thinking isn't your strong suit, is it?",
        "Roses are red, violets are blue, god made us beautiful, but what happened to you?",
        "Are you in great physical pain, or is that your thinking expression?",
        "Your body fat is about as evenly distributed as wealth in the US economy.",
        "Where’s your off button?",
        "It may be that your whole purpose in life is simply to serve as a warning to others",
        "You're the reason the gene pool needs a lifeguard",
        ]

        no_roast = {
            564610598248120320,
            783159643126890517,
        }

        if member is None:
            member = choice(ctx.guild.members)

        if member.id in no_roast:
            a = discord.Embed(
                colour=discord.Color(0xE41919),
                description="Nope, not doing that",
            )

            await ctx.send(embed=a)
        
        else:
            e = discord.Embed(
                colour=discord.Color(0xE41919),
                description=f'{member.mention} {choice(roast)}',
            )

            await ctx.send(embed=e)

    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command()
    async def someone(self, ctx):
        """Discord's mistake"""
        await ctx.send(choice(ctx.guild.members).mention)

    @commands.command()
    async def findtaxes(self, ctx):
        """`See how much you owe in taxes`"""

        lessTaxesMsg = [
            "You really do pay your taxes",
            "How do you do this",
            "Do you do manual maths?",
            "Im amazed",
        ]

        moreTaxesMsg = [
            "How many years have you gone without paying taxes",
            "How come the IRS has not taken your house",
            "How the hell do you owe so much",
            "The IRS is having a lot of patience on ya",
        ]

        taxmona = randint(0, 1000000)

        if taxmona == 0:
            await ctx.send(
                f"{ctx.author.mention} -> You owe nothing, are you 65 years old?"
            )
        elif taxmona <= 5000:
            if taxmona == 1:
                s = ""
            else:
                s = "s"
            await ctx.send(
                f"{ctx.author.mention} -> you owe ${taxmona} dollar{s} - {lessTaxesMsg[randint(0, len(lessTaxesMsg) - 1)]}"
            )
        else:
            await ctx.send(
                f"{ctx.author.mention} -> you owe ${taxmona} in taxes - {moreTaxesMsg[randint(0, len(moreTaxesMsg) - 1)]}"
            )

    @commands.command()
    async def canihaveahug(self, ctx):
        message = await ctx.send("https://cdn.discordapp.com/attachments/745481731582197780/803337680086761522/giphy.gif")
        await asyncio.sleep(2.5)
        await message.edit(content="https://cdn.discordapp.com/attachments/745481731582197780/803338739882524742/next.png")

    @commands.command(aliases = ['memes'])
    async def meme(self, ctx):
        memejson = requests.get('https://meme-api.herokuapp.com/gimme/memes').json()
        await ctx.send(memejson['url'])

    @commands.group(aliases = ['bb'], example=["group"], invoke_without_command=True)
    async def blackboxgame(self, ctx, arg=None):
        """`A little game I created`"""
        
        emojis = {
            "{bad}": "<:error:783265883228340245>",
            "{good}": "<:greenTick:767209095090274325>"
        }

        # range(25) for 7x7
        goodBad = ["||{bad}||" if randint(1, 7) == 1 else "||{good}||" for i in range(49)]

        output = ""
        stuff = 0
        for row in range(7):
            for col in range(7):
                output += goodBad[stuff]
                stuff += 1
            output += "\n"

        for e in emojis.keys():
            output = output.replace(e, emojis[e])

        e = discord.Embed(
        title="The Black Box Game!",
        description=f"{output}",
        color=discord.Colour(0xE41919),
        )
        e.set_footer(
            text=f"Do -bb htp to learn how to play the game!"
        )
            
        await ctx.send(embed=e)
        
    @blackboxgame.command(name="htp")
    async def bbhtp(self, ctx):
        htp = discord.Embed(
        colour=discord.Color(0xE41919),
        title="**How to Play The Black Box**",
        description="In this game, you are going to press the black boxes, you are going to try and get as many <:greenTick:767209095090274325> as you can.\n"
        + "If you get a <:error:783265883228340245>, you lose.\n"
        + "Every box has a 15% chance of being an <:error:783265883228340245>\n"
        + f"GL! If you want to play do `-bb` to start playing\n"
        + "\n"
        + "**Leaderboards**\n"
        + "To submit a run for this game you need to do the following-\n"
        + "1. You need to submit a video (NOT A PHOTO) so it can be verified\n"
        + "2. You had to do the command\n"
        + "3. The recording has to have you full screen (or only the text channel) and needs to have when you did the command\n"
        + f"To submit, do `-bb submit <Time> <Video>`\n",
        )
        await ctx.send(embed=htp)

    @blackboxgame.command(name="lb")
    async def bblb(self, ctx):
        lb = discord.Embed(
        colour=discord.Color(0xE41919),
        title="**Black Box Game Leaderboards**",
        description="<:1st:806646658016215053> 1st - N/A\n"
        + "<:2nd:806646671735128096> 2nd - N/A\n"
        + "<:3rd:806646682292191242> 3rd - N/A\n"
        + "4rd - N/A\n"
        )
        lb.set_footer(
            text=f"do -bb htp to see leaderboard rules"
        )
        await ctx.send(embed=lb)

    @blackboxgame.command(name="submit")
    async def submit(self, ctx, checks=None, video=None):

        bot_owner = self.client.get_user(564610598248120320)

        if checks == None:
            await ctx.send("Please give me the amout of <:greenTick:767209095090274325> you got in the game")

        elif video == None:
            await ctx.send("Please give me a video link (either YT or a file, do `-bb htsf` to learn how to submit a file)")

        else:
            await bot_owner.send(f'{ctx.author} has submitted a run for The Black Box Game and got {checks} <:greenTick:767209095090274325> and this is the video {video}')
            await ctx.send("You run has been submitted to the Owner, it will get reviewed and if verified added to the leaderboards")

    @blackboxgame.command(name="htsf")
    async def htsf(self, ctx):
        a = discord.Embed(
        colour=discord.Color(0xE41919),
        title="**How to submit a File**",
        description="First, upload your file to Discord (it has to be a mp4 file, if its not, this will not work)",
        )
        b = discord.Embed(
            colour=discord.Colour(0xE41919),
            description="Now that you uploaded it to Discord, right click the video and click `Copy Link`",
        )
        c = discord.Embed(
            colour=discord.Colour(0xE41919),
            description="After that do `-bb [Number of checks you got] [The link you just copied]`",
        )
        d = discord.Embed(
            colour=discord.Colour(0xE41919),
            description="If you need further assistance, ping or DM <@564610598248120320> for help",
        )
        await ctx.send(embed=a)
        await ctx.send("https://cdn.discordapp.com/attachments/806957891939598388/806961381920342078/one.png\n")
        await ctx.send(embed=b)
        await ctx.send("https://cdn.discordapp.com/attachments/806957891939598388/806961400646729749/two.png")
        await ctx.send(embed=c)
        await ctx.send("https://cdn.discordapp.com/attachments/806957891939598388/806961414672613386/three.png")
        await ctx.send(embed=d)

def setup(client):
    client.add_cog(Fun(client))