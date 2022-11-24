from dataclasses import dataclass
from datetime import datetime


@dataclass
class SlackThreadMessage:
    user: str
    text: str
    date: datetime
    reactions: dict[str, int]


@dataclass
class SlackMessage:
    user: str
    text: str
    date: datetime
    reactions: dict[str, int]
    replies: list[SlackThreadMessage]


@dataclass
class SlackData:
    channel_name: str
    messages: list[SlackMessage]
    emojis: dict[str, str]