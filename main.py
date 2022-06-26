import os
import time
import json
import logging
from argparse import ArgumentParser
from telegram.client import Telegram

ENTER_API_ID = "Enter your api_id (can be found on https://my.telegram.org/apps): "
ENTER_API_HASH = "Enter your api_hash (can be found on https://my.telegram.org/apps): "
ENTER_PHONE = "Enter your phone (can be found on https://my.telegram.org/apps): "
ENTER_DB_KEY = "Enter your database encryption key (can be found on https://my.telegram.org/apps): "

logging.basicConfig(level=logging.INFO)

parser = ArgumentParser()
parser.add_argument(
    "-l", "--login", help="Path to .json file with credentials.", required=True
)
parser.add_argument(
    "-id", "--chat_id", help="Chat ID (can be found by @userinfobot).", required=True
)
parser.add_argument(
    "-cmd", "--command", help="Command to start the script.", required=True
)
parser.add_argument(
    "-f", "--frames", help="Path to a directory with frames.", required=True
)
parser.add_argument(
    "-d", "--delay", help="A delay between frames (seconds).", default=0.25, type=float
)
args = parser.parse_args()

with open(args.login, "r", encoding="utf-8") as login_json:
    login_data = json.load(login_json)

ifChanged = False
if "api_id" not in login_data:
    api_id = input(ENTER_API_ID)
    login_data["api_id"] = api_id
    ifChanged = True
if "api_hash" not in login_data:
    api_hash = input(ENTER_API_HASH)
    login_data["api_hash"] = api_hash
    ifChanged = True
if "phone" not in login_data:
    phone = input(ENTER_PHONE)
    login_data["phone"] = phone
    ifChanged = True
if "database_encryption_key" not in login_data:
    database_encryption_key = input(ENTER_DB_KEY)
    login_data["database_encryption_key"] = database_encryption_key
    ifChanged = True

if ifChanged:
    with open(args.login, "w", encoding="utf-8") as login_json:
        json.dump(login_data, login_json, ensure_ascii=False, indent=4)

assert os.path.exists(args.frames), "The path to frames folder does not exist."

tg = Telegram(
    api_id=login_data["api_id"],
    api_hash=login_data["api_hash"],
    phone=login_data["phone"],
    database_encryption_key=login_data["database_encryption_key"],
)
tg.login()
response = tg.get_chats()
response.wait()

receive = True
message_id = 0
countErrors = 0
while receive:
    try:
        response = tg.get_chat_history(args.chat_id, 1, 0)
        response.wait()
        data = response.update
        if (
            "text" in data["messages"][0]["content"]
            and data["messages"][0]["content"]["text"]["text"] == args.command
        ):
            message_id = data["messages"][0]["id"]
            receive = False
    except TypeError:
        countErrors += 1

    if countErrors > 5:
        raise Exception("[ERROR] Unknown TypeError while waiting for the command.")

    time.sleep(0.25)

frames_filenames = os.listdir(args.frames)
frames_filenames = list(
    filter(lambda x: x.endswith(".txt") and x.split(".")[0].isdigit(), frames_filenames)
)
frames_filenames = sorted(frames_filenames, key=lambda x: int(x.split(".")[0]))

MAX_LENGTH = 128
MAX_WIDTH = 64

if len(frames_filenames) > MAX_LENGTH:
    print(
        f"[WARN] The length of the animation exceeds the max length of {MAX_LENGTH}. It will be cut to first {MAX_LENGTH} frames."
    )

frames = []

for f in frames_filenames:
    with open(os.path.join(args.frames, f), "r", encoding="utf-8") as fp:
        frames.append(fp.read())

    for i in range(len(frames[-1])):
        if len(frames[-1][i]) > MAX_WIDTH:
            print(
                f"[WARN] The length of the line of the frame exceeds the max length if {MAX_WIDTH}. It will be cut to last {MAX_WIDTH} symbols."
            )
            frames[-1][i] = frames[-1][i][-MAX_WIDTH:]


for frame in frames:
    response = tg.call_method(
        "editMessageText",
        params={
            "chat_id": args.chat_id,
            "message_id": message_id,
            "input_message_content": {
                "@type": "inputMessageText",
                "text": {"@type": "formattedText", "text": frame},
            },
        },
    )
    response.wait()
    if response.update is None:
        print("[ERROR] Could not edit the message. Is it sent by you?")
    time.sleep(args.delay)

tg.stop()
