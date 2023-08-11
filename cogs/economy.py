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
        results = cur.fetchone()
        if results is None:
            await ctx.send(f"Couldnt find wallet for {ctx.author}, try using command !create to start a wallet")
        else:
            await ctx.send(f'{ctx.author} has {results[0]} squarecoins')
        db.close()

    # give another user some cash from your wallet
    @commands.command()
    async def give(self, ctx, *args):
        try:
            amount = int(args[0])
        except Exception as e:
            print("sometin fucky")
            return

        user_sender = ctx.author.id
        user_receiever = int(args[1][2:-1])
        db = sqlite3.connect("economy.db")
        cur = db.cursor()
        cur.execute(f"SELECT cash FROM users WHERE user_id = {user_sender}")
        user_sender_bal = cur.fetchone()[0]
        if user_sender_bal is None:
            await ctx.send(f"You dont have a wallet {user_sender}, you can make one with command !create")
            db.close()
            return
        elif user_sender_bal <= 0:
            await ctx.send(f"You have {user_sender_bal} cash, you cant send anything to anyone.")
            db.close()
            return
        else:
            cur.execute(f'SELECT cash FROM users WHERE user_id = {user_sender}')
            res_x = cur.fetchone()[0]
            new_amount_x = res_x - amount

            cur.execute(f'SELECT cash FROM users WHERE user_id = {user_receiever}')
            res_y = cur.fetchone()[0]
            new_amount_y = res_y + amount

            if new_amount_x < 0:
                await ctx.send(f'You cant give that much away')
                db.close()
                return
            else:
                cur.execute(f"UPDATE users SET cash = {new_amount_x} WHERE user_id = {user_sender}")
                db.commit()
                cur.execute(f'UPDATE users SET cash = {new_amount_y} WHERE user_id = {user_receiever}')
                db.commit()
                db.close()
                await ctx.send(f"{ctx.author} just gave {amount} to {ctx.guild.get_member(user_receiever)}, very noice.")


async def setup(client):
    await client.add_cog(economy(client))
