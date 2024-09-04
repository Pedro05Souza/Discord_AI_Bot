from dataclasses import dataclass
from discord.ext.commands import Context
from decorators import AI_check
import discord

@dataclass
class Action:
    user: discord.Member
    context: Context
    user_score: int

    @AI_check()
    async def mute_user(self) -> None:
        """Mutes the user"""
        await self.context.send(f"Muting {self.user.mention}")
        await self.user.edit(mute=True)