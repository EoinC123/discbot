import os
import discord
from discord.ext import commands
import sqlite3


class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    def db_setup(self, guild: discord.Guild):
        proj_dir = os.getcwd()
        if os.path.isfile(f"{proj_dir}/../resources/eco"):
            print("Database currently exists")
            return
        else:
            try:
                # create the file
                con = sqlite3.connect("../resources/eco")
                cur = con.cursor()
                # create table for users and populate with member ID's and roles
                cur.execute("CREATE TABLE users(id TEXT, roles, SquareBucks INTEGER)")
                # for every guild member, populate the user database with the base values as well as their ID and roles
                for i in guild.members:
                    cur.execute(f'INSERT INTO users VALUES({i.id},{i.roles},100)')
                con.close()
            except sqlite3.Error:
                print("error connecting/creating database")
                return False


async def setup(client):
    await client.add_cog(economy(client))
