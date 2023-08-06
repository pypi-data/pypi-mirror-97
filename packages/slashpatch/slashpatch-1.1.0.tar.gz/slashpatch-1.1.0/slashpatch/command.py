from asyncio import iscoroutinefunction as iscoro


class Command:
    def __init__(self, func, **kwargs):
        if not iscoro(func):
            raise TypeError("Command must be a coroutine.")

        self.name = kwargs.get("name", func.__name__)

        self.func = func


class Cog:
    def get_commands(self):
        for attr in dir(self):
            attr = getattr(self, attr)
            if isinstance(attr, Command):
                yield attr


def command(name=None, cls=None, **kwargs):
    cls = cls or Command

    def decorator(func):
        return cls(func, name=name, **kwargs)

    return decorator
