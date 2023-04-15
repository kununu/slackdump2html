import os
import re
from datetime import datetime

import emoji

from src.SlackDataCleaner import SlackDataCleaner
from src.SlackDumpReader import SlackData, SlackMessage, SlackThreadMessage


class HtmlPrinter:
    slack_data: SlackData
    channel_id: str
    standard_emojis: dict[str, str] = dict()
    used_custom_emojis: set[str] = set()
    data_cleaner = SlackDataCleaner()

    def __init__(self, slack_data: SlackData, channel_id: str):
        self.slack_data = slack_data
        self.channel_id = channel_id

    def print(self):
        html1 = "<!DOCTYPE html>\n"
        html1 += "    <head>\n"
        html1 += (
            f"        <title>{self.slack_data.get_title_text()} chat history</title>\n"
        )
        html1 += '        <meta charset="UTF-8">'
        html1 += self.read_css_file()
        html3 = "    </head>\n"
        html3 += "    <body>\n"
        html3 += f"        <h1>{self.slack_data.get_title_text()} chat history</h1>\n"
        html3 += self.print_messages(self.slack_data.messages)
        # Only print used emojis
        html2 = self.print_custom_emoji_definitions()
        html3 += "    </body>\n"
        html3 += "</html>\n"

        html = html1 + html2 + html3

        self.write_out_file(html)

    def read_css_file(self) -> str:
        html = '        <style type="text/css">\n'
        with open("src/style/style.css") as file:
            html += file.read()
        html += "        </style>\n"
        return html

    def print_messages(self, messages: list[SlackMessage]) -> str:
        html = ""

        last_date = None
        if len(messages) > 0:
            last_date = self.to_date(messages[0].date)
            html += self.print_date_block(last_date)

        for message in messages:
            date = self.to_date(message.date)
            if date != last_date:
                last_date = date
                html += self.print_date_block(date)

            html += self.print_message(message)
        return html

    def print_date_block(self, date: str) -> str:
        return f'        <div class="date-block"><span class="date-block-content">{date}</span></div>\n'

    def print_message(self, message: SlackMessage) -> str:
        html = '        <div class="message-container">\n'
        html += self.print_user_image(message.user)
        html += '            <p class="meta">\n'
        html += f'                <span class="author">{message.user}</span>\n'
        html += (
            f'                <span class="date">{self.to_time(message.date)}</span>\n'
        )
        html += "            </p>\n"
        html += (
            f'            <p class="message">{self.format_message(message.text)}</p>\n'
        )
        html += self.print_reactions(message.reactions)
        html += self.print_replies(message)
        html += "        </div>\n"
        return html

    def print_user_image(self, user: str) -> str:
        if " " in user:
            parts = user.split(" ")
            name = parts[0][0].upper() + parts[1][0].upper()
        else:
            name = user[0].upper()
        return f'            <div class="user-image color{self.calc_color_num(user)}">{name}</div>\n'

    def calc_color_num(self, user: str) -> int:
        letter_sum = 0
        for letter in user:
            letter_sum += ord(letter)
        return letter_sum % 15

    def format_message(self, text: str) -> str:
        text = text.replace("<!here>", '<span class="user-mention">here</span>')
        text = text.replace("<!channel>", '<span class="user-mention">channel</span>')
        text = re.sub(r"<(http.*?)\|(.*?)>", self.create_html_url_with_alias, text)
        text = re.sub(r"<(http.*?)>", self.create_html_url, text)
        text = re.sub(r"<(img .*?)>", self.create_html_img, text)
        text = re.sub(r"<@(.*?)>", self.create_at_tag, text)
        text = re.sub(r"<#.*\|(.*?)>", self.create_channel_tag_with_alias, text)
        text = re.sub(r"\*([^\"\n]+?)\*", self.make_bold, text)
        text = re.sub(
            r":([\w+-]+?)::skin-tone-(\d):", self.replace_emoji_with_skin_tone, text
        )
        text = re.sub(r":([\w+-]+?):", self.replace_emoji, text)
        text = re.sub(r"```(.*)```", self.make_code, text, flags=re.DOTALL)
        text = text.replace("\n", "<br>")
        text = emoji.emojize(text, language="alias")
        # TODO Emoji codes in links are translated to emojis which breaks these links
        return text

    def create_html_url_with_alias(self, match_obj):
        if match_obj.group(1) is not None and match_obj.group(2) is not None:
            return f'<a href="{match_obj.group(1)}">{match_obj.group(2)}</a>'

    def create_html_url(self, match_obj):
        if match_obj.group(1) is not None:
            return f'<a href="{match_obj.group(1)}">{match_obj.group(1)}</a>'

    def create_html_img(self, match_obj):
        if match_obj.group(1) is not None:
            return f"<{match_obj.group(1)}>"

    def create_at_tag(self, match_obj):
        if match_obj.group(1) is not None:
            user = match_obj.group(1)
            if user in self.data_cleaner.user_map:
                user = self.data_cleaner.user_map[user]
            return f'<span class="user-mention">{user}</span>'

    def create_channel_tag_with_alias(self, match_obj):
        if match_obj.group(1) is not None:
            return f'<span class="channel-mention">{match_obj.group(1)}</span>'

    def make_bold(self, match_obj):
        if match_obj.group(1) is not None:
            return f"<b>{match_obj.group(1)}</b>"

    def make_code(self, match_obj):
        if match_obj.group(1) is not None:
            code = match_obj.group(1)
            code = code.replace("<", "&lt;")
            code = code.replace(">", "&gt;")
            return f"<code>{code}</code>"

    def replace_emoji(self, match_obj):
        emoji_name = match_obj.group(1)
        if emoji_name is not None:
            return self.get_custom_emoji_html(emoji_name)

    def replace_emoji_with_skin_tone(self, match_obj):
        emoji_name = match_obj.group(1)
        skin_tone = match_obj.group(2)
        if emoji_name is not None and skin_tone is not None:
            cleaned_emoji_name = self.data_cleaner.replace_emoji_name_with_skin_tone(
                emoji_name, int(skin_tone)
            )
            return self.get_custom_emoji_html(cleaned_emoji_name)

    def print_reactions(self, reactions: dict[str, int]) -> str:
        html = ""
        if len(reactions) > 0:
            html += '            <ul class="reactions">\n'
            for reaction in reactions.items():
                emoji_name = self.get_custom_emoji_html(reaction[0])
                if emoji_name.startswith(":"):
                    print(f"Couldn't translate emoji {emoji_name}")
                html += f'                <li title="{reaction[0]}">{emoji_name} {reaction[1]}</li>\n'
            html += "            </ul>\n"
        return html

    def get_custom_emoji_html(self, emoji_name: str):
        if emoji_name in self.slack_data.emojis:
            self.used_custom_emojis.add(emoji_name)
            return f'<i class="emoji emoji-{emoji_name}"></i>'
        else:
            return emoji.emojize(
                f":{self.data_cleaner.replace_emoji_name(emoji_name)}:",
                language="alias",
            )

    def print_replies(self, message: SlackMessage) -> str:
        html = ""
        if len(message.replies) > 0:
            html += '		    <div class="thread">\n'
            html += f'               <p class="thread-meta">{len(message.replies)} answers </p>\n'
            for reply in message.replies:
                html += self.print_reply(reply)
            html += "		    </div>\n"
        return html

    def print_reply(self, reply: SlackThreadMessage) -> str:
        html = '		        <div class="reply">\n'
        html += self.print_user_image(reply.user)
        html += '		            <p class="meta">\n'
        html += f'		                <span class="author">{reply.user}</span>\n'
        html += f'		                <span class="date">{self.to_datetime(reply.date)}</span>\n'
        html += "		            </p>\n"
        html += (
            f'		            <p class="message">{self.format_message(reply.text)}</p>\n'
        )
        html += self.print_reactions(reply.reactions)
        html += "		        </div>\n"
        return html

    def print_custom_emoji_definitions(self) -> str:
        html = '      <style type="text/css">\n'
        for emoji_name in self.used_custom_emojis:
            html += f"        .emoji-{emoji_name} {{\n"
            html += f'          background-image: url("data:{self.slack_data.emojis[emoji_name]}");'
            html += "        }\n"
        html += "      </style>\n"
        return html

    @staticmethod
    def to_date(date: datetime) -> str:
        return date.strftime("%a, %d.%m.%Y")

    @staticmethod
    def to_time(date: datetime) -> str:
        return date.strftime("%H:%M:%S")

    @staticmethod
    def to_datetime(date: datetime) -> str:
        return date.strftime("%d.%m.%Y %H:%M:%S")

    def write_out_file(self, html: str):
        if not os.path.exists("out"):
            os.makedirs("out")
        file_name = f"out/{self.slack_data.channel_name}.html"
        html_file = open(file_name, "w", encoding="utf-8")
        html_file.write(html)
        html_file.close()
        print(f"{file_name} successfully written")
