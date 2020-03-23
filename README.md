# house_finder

## Set up

```
> git clone https://github.com/sqrg/house_finder.git
> cd house_finder/
> touch credentials.py
> touch database.db
> pip install requirements.txt
```

#### Edit credentials.py
```
BOT_TOKEN = 'foo'
CHAT_ID = '-bar' # The - has to be there
```

For help creating your own Telegram bot, go [here](https://core.telegram.org/bots)

To get your `CHAT_ID`, you can visit https://web.telegram.org/, select your desired chat and copy the ID from the URL (the ID is the code after the `g`, e.g. in `p=g359930xxx` the ID is `359930xxx`)

#### Edit request_payload.json

You can modify values like limit price, or how many rooms

#### Run the script

Run the script with `python main.py` and you are set.
