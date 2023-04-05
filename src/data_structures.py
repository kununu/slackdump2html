from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


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


class ChannelType(StrEnum):
    Channel = "#"
    Conversation = "@"
    Private = "🔒"
    Unknown = "?"


@dataclass
class SlackData:
    channel_type: ChannelType
    channel_name: str
    messages: list[SlackMessage]
    emojis: dict[str, str]

    def get_title_text(self) -> str:
        return self.channel_type.value + self.channel_name
