import discord

class Member():
    def __init__(self, member: discord.Member):
        self._member = member
        self._points = 0
        self._play = True

    def get_is_play(self):
        return self._play

    def set_is_play(self, playing):
        self._play = playing

    def get_member(self):
        return self._member

    def get_points(self):
        return self._points