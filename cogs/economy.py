import sqlite3

from discord.ext import commands


class economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        db = sqlite3.connect("economy.db")
        cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER, cash INTEGER)''')
        db.commit()
        db.close()

    # command to create a user entry in the DB
    @commands.command()
    async def create(self, ctx):
        user = ctx.author.id
        db = sqlite3.connect("economy.db")
        cur = db.cursor()
        cur.execute(f'SELECT user_id FROM users WHERE user_id={user}')
        result = cur.fetchone()
        if result is None:
            cur.execute(f"INSERT INTO users(user_id,cash) VALUES ({user},50)")
            await ctx.send(f'{ctx.author} has been added to the economy')
            db.commit()
        else:
            await ctx.send(f'{ctx.author}, is already a registered user.')
        db.close()

    # Command to check users wallet
    @commands.command()
    async def wallet(self, ctx):
        user = ctx.author.id
        db = sqlite3.connect("economy.db")
        cur = db.cursor()
        cur.execute(f'SELECT cash FROM users WHERE user_id = {user}')
        results = cur.fetchone()[0]
        if results is None:
            await ctx.send(f"Couldnt find wallet for {ctx.author}, try using command !create to start a wallet")
        else:
            await ctx.send(f'{ctx.author} has {results} squarecoins')
        db.close()




async def setup(client):
    await client.add_cog(economy(client))
