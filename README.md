# tchan - Telegram Channel scraper

Python library and command-line interface to scrape Telegram public channels.
Since this scraper uses Telegram Channel Web preview, **it won't work** for:

- Public channels with "Restrict saving content" option enabled
- Private channels
- Public Groups
- Private Groups

It's also not possible to retrieve comments, since they're made on a group.

## Installing


```shell
pip install tchan  # Python library only
pip install tchan[cli]  # Library + CLI
```

## Using as a libray

```python
from tchan import ChannelScraper

scraper = ChannelScraper()
for message in scraper.messages("tchantest"):
    print(f"New message ({message.type}) from {message.channel}:")
    print(f"  id={message.id}")
    print(f"  created_at={message.created_at.isoformat()}")
    print(f"  text={message.text}")
    # TODO: add more parameters
```

## Using as a command-line tool

Scrape one or many channels and save all messages to `messages.csv`:

```shell
tchan messages.csv channel1 [channel2 ... channelN]
```

## Tests

To run all tests, execute:

```shell
make test  # or just `pytest`
```

Make sure to install development requirements.

Tests were made on a channel created for this task:
[tchantest](https://t.me/tchantest).
