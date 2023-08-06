from fastapi.responses import JSONResponse


class Context:
    """A Discord slash command context."""

    def __init__(self, raw: dict):
        self.raw = raw
        self.channel_id = raw["channel_id"]

        self.data = data = self.raw["data"]

        self.id = data["id"]
        self.name = data["name"]

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
