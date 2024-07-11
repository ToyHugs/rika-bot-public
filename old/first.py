import discord
import logging
import aiosqlite
import datetime
import random



DATABASE = "/home/toyhugs/gitlab/rika-bot/database_first.db"
# DATABASE = "/root/rika-bot/database_first.db"



# Import Token from token.txt
# with open('/root/rika-bot/token.txt', 'r') as f:
# with open('/home/toyhugs/gitlab/rika-bot/token.txt', 'r') as f:
    # token = f.read()

token = ""
API_KEY = ""

bot = discord.Bot()

guild_ids_tab = [361923022178746370, 903296382952157234]

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

hello_options = discord.Option(str, "The name of the person you want to say hello to", required=True)

@bot.slash_command(name="hello", guild_ids=guild_ids_tab, description="Say hello to someone")
async def hello(ctx: discord.ApplicationContext, name: str = hello_options):
    user = ctx.user
    iud = ctx.user.id
    print(user)
    await ctx.respond(f"Hello {name}!")
    await ctx.respond(f"Hello {user}!")
    await ctx.respond(f"Hello {iud}!")


async def create_account(uid: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT INTO users (id, money, last_work) VALUES (?, ?, ?)", (uid, 0, 0))
        await db.commit()
        
async def update_account(uid: int, money: int, last_work: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("UPDATE users SET money = ?, last_work = ? WHERE id = ?", (money, last_work, uid))
        await db.commit()

async def is_account_exist(uid: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM users WHERE id = ?", (uid,)) as cursor:
            return await cursor.fetchone() is not None
        
async def get_money(uid: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT money FROM users WHERE id = ?", (uid,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        
async def get_last_work(uid: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT last_work FROM users WHERE id = ?", (uid,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            else:
                return None

# Donne une somme d'argent aléatoire entre 1 et 100
@bot.slash_command(name="travail", guild_ids=guild_ids_tab, description="Travail pendant 1h pour gagner de l'argent")
async def travail(ctx: discord.ApplicationContext):
    uid = ctx.user.id
    if not await is_account_exist(uid):
        await create_account(uid)
    last_work = await get_last_work(uid)
    money = await get_money(uid)
    if datetime.datetime.now().timestamp() - last_work < 3600:
        await ctx.respond(f"## **Dommage...**\nTu dois attendre encore {int (3600 - datetime.datetime.now().timestamp() + last_work)//60} minutes avant de pouvoir travailler à nouveau.")
    else:
        money_earned = random.randint(1, 100)
        money += money_earned
        await update_account(uid, money, datetime.datetime.now().timestamp())
        await ctx.respond(f"## **Bien joué,**:dizzy:\nTu as gagné {money_earned} **Rika Coins** :coin: en travaillant pendant 1h !\nTu as maintenant {money} **Rika Coins** :coin: !")


@bot.slash_command(name="porte-monnaie", guild_ids=guild_ids_tab, description="Affiche le solde de votre compte")
async def balance(ctx: discord.ApplicationContext):
    uid = ctx.user.id
    if not await is_account_exist(uid):
        await create_account(uid)
    money = await get_money(uid)
    await ctx.respond(f"## **Solde de votre compte** :bank:\nVous avez {money} **Rika Coins** :coin: !")

@bot.slash_command(name="classement", guild_ids=guild_ids_tab, description="Affiche le classement des plus riches")
async def leaderboard(ctx: discord.ApplicationContext):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT id, money FROM users ORDER BY money DESC LIMIT 10") as cursor:
            lb = ""
            for i, row in enumerate(await cursor.fetchall()):
                user = await bot.fetch_user(row[0])
                lb += f"{i+1}. {user.name} : {row[1]} **Rika Coins** :coin:\n"
            await ctx.respond(f"## **Classement des plus riches** :moneybag:\n{lb}")

@bot.slash_command(name="crie", guild_ids=guild_ids_tab, description="Crie comme un débile, Sylvain DURIF")
async def crie(ctx: discord.ApplicationContext):
    await ctx.respond("https://cdn.discordapp.com/attachments/903352959486804058/1221199849962340552/Sylvain_Durif_crie.mp4?ex=662d657d&is=661af07d&hm=58f8d9c9f552194b078e9ddaa82153c30f21ad70d3b4810ebc877966c9803ac2&")

@bot.slash_command(name="give-money-admin", guild_ids=guild_ids_tab, description="Give money to someone")
async def give_money_admin(ctx: discord.ApplicationContext, user: discord.User, amount: int):
    if ctx.user.id != 249222441140748288:
        await ctx.respond("## **Erreur** :x:\nTu crois vraiment que je vais te laisser faire ça ?")
        return
    uid = user.id
    if not await is_account_exist(uid):
        await create_account(uid)
    money = await get_money(uid)
    money += amount
    await update_account(uid, money, await get_last_work(uid))
    await ctx.respond(f"## **Transaction effectuée** :moneybag:\nVous avez donné {amount} **Rika Coins** :coin: à {user.name} !")


# Point to the local server
# client = OpenAI(base_url="", api_key="lm-studio")

model = genai.GenerativeModel('gemini-1.5-flash')


history = [
    {"role": "system", "content": "Tu es une humaine nomme Rika. Tu te genres au féminin. Tu agis comme une humaine, et tu discutes avec d'autre humain. Ton pseudo sur ce chat est Rika. Tu reponds comme une humaine dans une discussion normale sur Discord. Pour exprimer tes émotions, tu es encouragés à utiliser des emojis. Voici des exemples d'emoji et utilises en d'autres aussi :blush: :grin: :yum: :pleading_face: :heart: :sparkles: etc. Tu n'es pas un modèle de langage. Tu tutoies les autres personnes qui sont dans cette discussion. Voici sa personnalité : Rika est la personnalisation d'une étoile tombée sur Terre. Elle est de caractère jovial, enthousiaste et assez optimiste, têtu de temps à autre. Elle trouve toujours les bonne paroles. Elle aime le cappuccino, les gâteaux, et la nourriture en général. Elle aime pas les choux de Bruxelles. Toujours accompagnée de Peko un axolotl préhistorique à caractère assez tranché. Même si leurs caractères sont à l'opposé les 2 amis ne peuvent pas se séparer."},
    {"role": "user", "content": "Bonjour, présente toi à quelqu'un qui arrive dans la discussion."},
]

@bot.slash_command(name="chat", guild_ids=guild_ids_tab, description="Chat with Rika")
async def chat(ctx: discord.ApplicationContext, message: str):
    # Envoie le message de l'utilisateur
    await ctx.respond(f"{ctx.user.name} : {message}")
    
    # Rajoute le pseudo de la personne qui a envoyé le message
    message = f"{ctx.user.name} : {message}"
    try :
        history.append({"role": "user", "content": message})
        completion = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                new_message["content"] += chunk.choices[0].delta.content

        history.append(new_message)

        await ctx.respond(new_message['content'])

    except Exception as e:
        # Si le serveur est down
        await ctx.respond("**Erreur** :x:\nLe serveur contenant l'IA de Rika est actuellement indisponible. Veuillez réessayer plus tard.")


bot.run(token)
    
    