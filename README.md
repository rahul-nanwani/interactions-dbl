<div align="center">
    <h1>interactions-dbl<h1>
    <img alt="PyPI" src="https://img.shields.io/pypi/v/interactions-dbl?color=4c7fbd&label=version&logoColor=33364b&style=flat-square">
    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/interactions-dbl?color=4c7fbd&logoColor=33364b&style=flat-square">
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/interactions-dbl?color=4c7fbd&logoColor=33364b&style=flat-square">
</div>

---

DBL (Discord Bot Lists) extension library for discord-py-interactions.

Find the supported bot listings [here](https://botblock.org/lists).

---

## Features

- Update server count on most of the bot listings.

---

## Installation

```Shell
pip install interactions-dbl
```

---

## Examples

### Using `bot.py`

```python
import interactions
from interactions.ext.dbl import DBLClient

from config import BOT_TOKEN, TOPGG_TOKEN, DBL_TOKEN

if __name__ == '__main__':
    bot = interactions.Client(
        token=BOT_TOKEN,
        intents=interactions.Intents.DEFAULT
    )


    @bot.event
    async def on_ready():
        auth = {
            "top.gg": TOPGG_TOKEN,
            "discordbotlist.com": DBL_TOKEN
        }
        DBLClient(bot=bot, auth=auth)


    bot.start()
```

### Using cogs

```python
import interactions
from interactions.ext.dbl import DBLClient

from config import TOPGG_TOKEN, DBL_TOKEN


class UpdateCount(interactions.Extension):
    def __init__(self, bot):
        self.bot: interactions.Extension = bot

        auth = {
            "top.gg": TOPGG_TOKEN,
            "discordbotlist.com": DBL_TOKEN
        }
        DBLClient(bot=self.bot, auth=auth)


def setup(client):
    UpdateCount(client)
```
