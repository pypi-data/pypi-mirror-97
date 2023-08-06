from datetime import datetime
from dateutil import parser
from typing import Optional, List


class OptionType:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8


class SlashPatchObject:
    type: int
    name: int


class String(SlashPatchObject):
    """A slash commands string option."""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.type = OptionType.STRING


class Integer(SlashPatchObject):
    """A slash commands integer option."""

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        self.type = OptionType.INTEGER


class Boolean(SlashPatchObject):
    """A slash commands boolean option."""

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        self.type = OptionType.BOOLEAN


class User(SlashPatchObject):
    """A slash commands user option."""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.type = OptionType.USER


class Channel(SlashPatchObject):
    """A slash commands user option."""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.type = OptionType.CHANNEL


class Role(SlashPatchObject):
    """A slash commands user option."""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.type = OptionType.ROLE


class SubCommand(SlashPatchObject):
    """A slash commands subcommand option."""

    def __init__(self, name: str, options: list):
        self.name = name
        self.type = OptionType.SUB_COMMAND

        self.options = []

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
            else:
                raise TypeError(f"Invalid option received! <Type={type}>")

            self.options.append(c(option["name"], option["value"]))


class SubCommandGroup(SlashPatchObject):
    """A slash commands subcommand group option."""

    def __init__(self, name: str, options: list):
        self.name = name
        self.type = OptionType.SUB_COMMAND

        self.options = []

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
                self.options.append(SubCommand(option["name"], option.get("options", [])))
                continue
            else:
                raise TypeError(f"Invalid option received! <Type={type}>")

            self.options.append(c(option["name"], option["value"]))


class ResolvedObject:
    def __init__(self, id: int):
        self.id = id


class ResolvedUser(ResolvedObject):
    def __init__(self, data: dict):
        super().__init__(int(data["id"]))

        self.username: str = data["username"]
        self.discriminator: int = int(data["discriminator"])
        self.public_flags: int = data["public_flags"]
        self.avatar: Optional[str] = data["avatar"]


class ResolvedMember(ResolvedObject):
    def __init__(self, user: ResolvedUser, data: dict):
        super().__init__(user.id)

        self.user: ResolvedUser = user
        self.is_pending: bool = data["is_pending"]
        self.pending: bool = data["pending"]
        self.nick: Optional[str] = data["nick"]
        self.joined_at: datetime = parser.isoparse(data["joined_at"])
        self.role_ids: List[int] = [int(role) for role in data["roles"]]
        self.premium_since: Optional[datetime] = None

        if ps := data["premium_since"]:
            self.premium_since = parser.isoparse(ps)


class ResolvedChannel(ResolvedObject):
    def __init__(self, data: dict):
        super().__init__(int(data["id"]))

        self.name: str = data["name"]
        self.permissions: int = int(data["permissions"])
        self.type: int = data["type"]


class ResolvedRole(ResolvedObject):
    def __init__(self, data: dict):
        super().__init__(int(data["id"]))

        self.name: str = data["name"]
        self.color: int = data["color"]
        self.hoist: bool = data["hoist"]
        self.managed: bool = data["managed"]
        self.mentionable: bool = data["mentionable"]
        self.permissions: int = int(data["permissions"])
        self.position: int = data["position"]
        self.tags: Optional[dict] = data.get("tags", {})
