from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from discord_interactions import verify_key
from asyncio import iscoroutinefunction as iscoro

from .context import Context
from .command import Cog
from .objects import OptionType, String, Integer, Boolean, User, Channel, Role, SubCommand, SubCommandGroup


class Server(FastAPI):
    def __init__(self, public_key: str, *args, interactions_path: str = "/interactions", **kwargs):
        super().__init__(*args, **kwargs)

        self.pubkey = public_key
        self.add_route(interactions_path, self.__recv, methods=["POST"])

        self.commands = {}
        self.cogs = {}

    async def __recv(self, req: Request):
        body = await req.body()

        sig = req.headers["X-Signature-Ed25519"]
        ts = req.headers["X-Signature-Timestamp"]

        if not verify_key(body, sig, ts, self.pubkey):
            raise HTTPException(400)

        data = await req.json()
        context = Context(data)
        args = self.parse_data(context.data)

        name = context.name
        if name in self.commands:
            cog, cmd = self.commands[name]

            result = await cmd(cog, context, *args)
            if isinstance(result, JSONResponse):
                return result

            raise Exception("Command responses must be valid JSONResponse objects.")

        raise HTTPException(404, "Command not found.")

    def parse_data(self, data: dict):
        options = data.get("options", [])

        args = []

        for option in options:
            type = option["type"]

            if type == OptionType.STRING:
                c = String
            elif type == OptionType.INTEGER:
                c = Integer
            elif type == OptionType.BOOLEAN:
                c = Boolean
            elif type == OptionType.USER:
                c = User
            elif type == OptionType.CHANNEL:
                c = Channel
            elif type == OptionType.ROLE:
                c = Role
            elif type == OptionType.SUB_COMMAND:
                args.append(SubCommand(option["name"], option.get("options", [])))
                continue
            elif type == OptionType.SUB_COMMAND_GROUP:
                args.append(SubCommandGroup(option["name"], option.get("options", [])))
                continue
            else:
                raise TypeError(f"Invalid option received! <Type={type}>")

            args.append(c(option["name"], option["value"]))

        return args

    def add_command(self, cog: Cog, func, name: str = None):
        name = name or func.__name__

        if not iscoro(func):
            raise TypeError("Command functions must be coroutines.")

        self.commands[name] = (cog, func)

    def add_cog(self, cog: Cog):
        for command in cog.get_commands():
            self.add_command(cog, command.func, command.name)
