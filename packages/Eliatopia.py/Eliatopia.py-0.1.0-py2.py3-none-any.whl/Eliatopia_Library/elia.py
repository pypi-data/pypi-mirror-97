import requests
import json

api_keys = {"keys":{"online": "http://eliatopiaapi.com/TotalOnline","time": "https://eliatopiaapi.com/Time","other_items":"https://eliatopia-files.s3.us-east-2.amazonaws.com/game_text_files/otherItems.json","leaderboard":"https://www.eliatopia.com/streaming/getRanks.php?name={}"}}

class Eliatopia:
    def __init__(self, version):
        self.version = version

    def getOnline(self):
        url = api_keys["keys"]["online"]
        online = requests.get(f"{url}").json()
        print("Players Online: {}".format(online))

    async def getOnlineDiscord(self, ctx):
        url = api_keys["keys"]["online"]
        online = requests.get(url).json()
        await ctx.send("Players Online: `{}`".format(online))

    def getServerTime(self):
        url = api_keys["keys"]["time"]
        gameTime = requests.get(url).text
        print("Server Time: {}".format(gameTime))

    async def getServerTimeDiscord(self, ctx):
        url = api_keys["keys"]["time"]
        gameTime = requests.get(url).text
        await ctx.send("Server Time: `{}`".format(gameTime))

    def getLeaderboard(self, player):
        url = api_keys["keys"]["leaderboard"]
        playerStats = requests.get(url.format(player)).text
        playerStatsRep = playerStats.replace(",", " ")
        stats = playerStatsRep.split()
        print("Name: {}\nTotal Ranked Levels: {}\nPlayer's Level Rank: {}\nTotal Ranked Kills: {}\nKills Rank: {}\nEnemies Killed: {}".format(player, stats[0], stats[1], stats[2], stats[3], stats[4]))

    async def getLeaderboardDiscord(self, ctx, player):
        url = api_keys["keys"]["leaderboard"]
        playerStats = requests.get(url.format(player)).text
        playerStatsRep = playerStats.replace(",", " ")
        stats = playerStatsRep.split()
        msg_to_send = "Name: `{}`\nTotal Ranked Levels: `{}`\nPlayer's Level Rank: `{}`\nTotal Ranked Kills: `{}`\nKills Rank: `{}`\nEnemies Killed: `{}`".format(player, stats[0], stats[1], stats[2], stats[3], stats[4])
        await ctx.send(msg_to_send)