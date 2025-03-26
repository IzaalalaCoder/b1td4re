import discord

class Member():
    def __init__(self, member: discord.Member):
        self._member = member
        self._points = 0
        self._guilds_play = {}
        self._calendar_playing = []

    def contain_guild(self, guild):
        return guild in self._guilds_play

    def get_is_play(self, guild):
        return True if self._guilds_play[guild] else False

    def set_is_play(self, playing, guild):
        self._guilds_play[guild] = playing

    def get_member(self):
        return self._member

    def get_points(self):
        return self._points

    def add_points(self, points : int):
        self._points += 10

    def add_participate(self):
        self._calendar_playing.add(d.date.today())
        pass