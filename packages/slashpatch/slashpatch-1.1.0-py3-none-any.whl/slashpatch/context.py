from fastapi.responses import JSONResponse
from typing import TypedDict

from .objects import ResolvedUser, ResolvedMember, ResolvedChannel, ResolvedRole


class Context:
    """A Discord slash command context."""

    def __init__(self, raw: dict):
        self.raw = raw
        self.channel_id = int(raw["channel_id"])
        self.guild_id = int(raw.get("guild_id")) if "guild_id" in raw else None
        self.interaction_id = int(raw["id"])

        self.data = data = self.raw["data"]

        self.id = (data["id"])
        self.name = data["name"]

        user = ResolvedUser(raw["member"]["user"])
        self.author = ResolvedMember(user, raw["member"])

        resolved = raw.get("resolved", {})
        self._users: TypedDict[ResolvedUser] = {int(k): ResolvedUser(v) for k, v in resolved.get("users", {})}
        self._members: TypedDict[ResolvedMember] = {int(k): ResolvedMember(self.users[int(k)], v) for k, v in resolved.get("members", {})}
        self._channels: TypedDict[ResolvedChannel] = {int(k): ResolvedChannel(v) for k, v in resolved.get("channels", {})}
        self._roles: TypedDict[ResolvedRole] = {int(k): ResolvedRole(v) for k, v in resolved.get("roles", {})}

    def respond(self, content: str = None, embed: dict = None, ephemeral: bool = False):
        if embed and ephemeral:
            raise Exception("Cannot use an ephemeral response with an embed.")

        data = {}

        if content:
            data["content"] = content
        if embed:
            data["embeds"] = [embed]
        if ephemeral:
            data["flags"] = 64

        return JSONResponse({
            "type": 4,
            "data": data
        })

    def get_user(self, id: str):
        return self._users.get(id, None)

    def get_member(self, id: str):
        return self._members.get(id, None)

    def get_channel(self, id: str):
        return self._channels.get(id, None)

    def get_role(self, id: str):
        return self._roles.get(id, None)
