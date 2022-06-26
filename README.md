# Telegram Message Animation

Create an animation in Telegram with text & emojis by editing a message.

# Disclaimer
This project uses [python-telegram](https://github.com/alexander-akhmetov/python-telegram) module. It supports only Linux. 

# Installation
1. Build [TDLib](https://github.com/tdlib/td#building)
2. Install modules by running `pip install -r requirements.txt`
3. [Register](http://my.telegram.org/apps/) a new Telegram app
4. Create .txt files for frames of your animation
   1. You can view it by running `python animation_viewer.py -f /path/to/frames`
5. Run the script by executing `python main.py -l /path/to/login.json -id chat_id -cmd CommandToStartAnimation -f /path/to/frames`