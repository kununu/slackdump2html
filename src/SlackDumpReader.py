import base64
import json
import os
from datetime import datetime

from src.data_structures import SlackData, SlackMessage, SlackThreadMessage


class SlackDumpReader:
    def read(self, file_path: str) -> SlackData:
        dump_file = open(file_path, encoding="utf-8")
        dump_data = json.load(dump_file)

        messages: list[SlackMessage] = list()

        for message in dump_data["messages"]:
            if (
                message["type"] == "message"
                and "subtype" not in message
                and "text" in message
            ):
                replies = self.read_replies(message)
                messages.append(
                    SlackMessage(
                        user=self.get_user(message),
                        text=self.get_message_content(message),
                        date=self.to_datetime(message["ts"]),
                        reactions=self.read_reactions(message),
                        replies=replies,
                    )
                )

        slack_data = SlackData(
            channel_name=dump_data["name"],
            messages=messages,
            emojis=self.read_emojis(),
        )

        return slack_data

    def get_user(self, message: dict) -> str:
        if "user" in message:
            return message["user"]
        else:
            return "Unknown user"

    def get_message_content(self, message: dict) -> str:
        if self.is_gif(message):
            return (
                '<img src="'
                + message["blocks"][0]["image_url"]
                + '" alt="'
                + message["text"]
                + '">'
            )
        else:
            return message["text"]

    def is_gif(self, message: dict) -> bool:
        return (
            message["blocks"] is not None
            and message["blocks"][0]["type"] == "image"
            and str(message["blocks"][0]["image_url"]).__contains__("giphy.com")
        )

    def read_replies(self, message: dict) -> list[SlackThreadMessage]:
        replies: list[[SlackThreadMessage]] = list()
        if "slackdump_thread_replies" in message:
            for reply in message["slackdump_thread_replies"]:
                if (
                    reply["type"] == "message"
                    and "subtype" not in reply
                    and "text" in reply
                ):
                    replies.append(
                        SlackThreadMessage(
                            user=reply["user"],
                            text=self.get_message_content(reply),
                            date=self.to_datetime(reply["ts"]),
                            reactions=self.read_reactions(reply),
                        )
                    )
        return replies

    def read_reactions(self, message: dict) -> dict[str, int]:
        reactions: dict[str, int] = dict()
        if "reactions" in message:
            for reaction in message["reactions"]:
                reactions[reaction["name"]] = reaction["count"]
        return reactions

    def read_emojis(self) -> dict[str, str]:
        emoji_file = open("data/emojis/index.json", encoding="utf-8")
        emoji_data = json.load(emoji_file)

        emojis: dict[str, str] = dict()
        for emoji in emoji_data.items():
            if not emoji[1].startswith("alias:"):
                with open(self.get_emoji_file_name(emoji[0]), "rb") as image:
                    image_data = image.read()
                    image_type = self.get_image_type(image_data)
                    base64_data = (
                        base64.encodebytes(image_data).decode("utf-8").replace("\n", "")
                    )
                    emojis[emoji[0]] = image_type + ";base64," + base64_data

        for emoji in emoji_data.items():
            if emoji[1].startswith("alias:") and emoji[1][6:] in emojis:
                emojis[emoji[0]] = emojis[emoji[1][6:]]

        return emojis

    def get_emoji_file_name(self, emoji_name: str) -> str:
        if os.path.exists("data/emojis/emojis/" + emoji_name + ".gif"):
            return "data/emojis/emojis/" + emoji_name + ".gif"
        elif os.path.exists("data/emojis/emojis/" + emoji_name + ".jpeg"):
            return "data/emojis/emojis/" + emoji_name + ".jpeg"
        elif os.path.exists("data/emojis/emojis/" + emoji_name + ".jpg"):
            return "data/emojis/emojis/" + emoji_name + ".jpg"
        elif os.path.exists("data/emojis/emojis/" + emoji_name + ".png"):
            return "data/emojis/emojis/" + emoji_name + ".png"
        else:
            return "<none>" + emoji_name

    def get_image_type(self, image_data: bytes) -> str:
        if image_data.startswith(bytes("GIF", "utf-8")):
            return "image/gif"
        else:
            # TODO support other image types. Not urgent - it works like that, but is technically wrong
            return "image/png"

    @staticmethod
    def to_datetime(timestamp: str) -> datetime:
        return datetime.fromtimestamp(float(timestamp))
