import argparse
from functools import wraps
import asyncio

from . import Funkwhale


def as_sync(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res
    return wrapper


async def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    api = Funkwhale("https://funkwhale-paftown.ddns.net")
    await api.login("wolfgang", "N@AM4-:W[2S~.B+5")

    async with api.session:
        response = await api.artists.list_libraries(1)
        print(response)


if __name__ == "__main__":
    as_sync(main)()
