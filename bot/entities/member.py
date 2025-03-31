import discord
import datetime as d

class Member:
    def __init__(self, member: discord.Member):
        self._member = member
        self._points = 0
        self._guilds_play = {}
        self._calendar_playing = {}

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
        self._points += points

    def add_participate(self, id : int, guild):
        date = d.date.today()
        month = date.month
        year = date.year
        day = date.day

        key = f"{day}/{month}/{year}--{guild}"

        if key not in self._calendar_playing:
            self._calendar_playing[key] = []
        self._calendar_playing[key].append(id)

    def has_realized(self, id : int, guild):
        date = d.date.today()
        month = date.month
        year = date.year
        day = date.day

        key = f"{day}/{month}/{year}--{guild}"
        if key not in self._calendar_playing:
            return False
        else:
            return id in self._calendar_playing[key]

    def get_calendar_playing(self):
        return self._calendar_playing