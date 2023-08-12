import sqlite3
from datetime import datetime
from discord.ext import commands
import string

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
        today = str(datetime.now().date())
        print(today)
        db = sqlite3.connect("economy.db")
        cur = db.cursor()
        cur.execute(f'SELECT user_id FROM users WHERE user_id={ctx.author.id}')
        result = cur.fetchone()
        if result is None:
            cur.execute(f"INSERT INTO users(user_id,cash) VALUES ({ctx.author.id},50)")
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
        # improper input handling
        if len(args) != 2:
            await ctx.send("Inavalid use of command, you need to provide an amount with the @user")
            return
        else:
            try:
                amount = abs(int(args[0]))
            except Exception as e:
                await ctx.send("Invalid use of !give command")
                print("They tried it lol")
                return

            user_sender = ctx.author.id
            try:
                user_receiever = int(args[1][2:-1])
            except Exception as e:
                await ctx.send("Invalid mention, you need to give to a user with @<user>")
                return
            if user_receiever == user_sender:
                await ctx.send("you cant send yourself money")
                return
            elif user_receiever == self.client.user.id:
                await ctx.send("Thanks, but I dont need it.")
                return
            ##############
            # run the transactioin
            db = sqlite3.connect("economy.db")
            cur = db.cursor()
            cur.execute(f"SELECT cash FROM users WHERE user_id = {user_sender}")
            try:
                user_sender_bal = cur.fetchone()[0]
            except Exception as e:
                await ctx.send("You either dont have a wallet or dont have enough money.")
                db.close()
                return
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
                    await ctx.send(f'You cant give that much away, you have a balance of {res_x}')
                    db.close()
                    return
                else:
                    cur.execute(f"UPDATE users SET cash = {new_amount_x} WHERE user_id = {user_sender}")
                    db.commit()
                    cur.execute(f'UPDATE users SET cash = {new_amount_y} WHERE user_id = {user_receiever}')
                    db.commit()
                    db.close()
                    await ctx.send(
                        f"{ctx.author} just gave {amount} to {ctx.guild.get_member(user_receiever)}, very noice.")


async def setup(client):
    await client.add_cog(economy(client))
