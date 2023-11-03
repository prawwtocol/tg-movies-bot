import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
)

import secret
import json


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    movie_name = update.message.text
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {secret.api_key}",
    }

    response = requests.get(url, headers=headers)

    # print(response.text)

    v1 = json.loads(response.content)
    v2 = v1["results"]

    keyboard = [
        [
            InlineKeyboardButton(
                "1",
                callback_data=v2[0]["id"],
            )
        ],
        [
            InlineKeyboardButton(
                "2",
                callback_data=v2[1]["id"],
            )
        ],
        [
            InlineKeyboardButton(
                "3",
                callback_data=v2[2]["id"],
            )
        ],
        [
            InlineKeyboardButton(
                "4",
                callback_data=v2[3]["id"],
            )
        ],
    ]
    await update.message.reply_text(
        f"""
1: {v2[0]["title"]}[{v2[0]["release_date"]}]{v2[0]["overview"]}

2: {v2[1]["title"]}[{v2[1]["release_date"]}]{v2[1]["overview"]}

3: {v2[2]["title"]}[{v2[2]["release_date"]}]{v2[2]["overview"]}

4:{v2[3]["title"]}[{v2[3]["release_date"]}]{v2[3]["overview"]}""",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    # query contains 1,2,3,4 now

    v2 = query.data  # contains selected movie id
    url = "https://api.themoviedb.org/3/account/20661070/watchlist"

    payload = {"media_type": "movie", "media_id": v2, "watchlist": True}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret.api_key}",
    }

    response = requests.post(url, json=payload, headers=headers)
    # TODO if response 2xx
    await query.edit_message_text(f"Added movie with id {query.data} to watchlist")
    pass


def main():
    """
    Main program function
    """
    application = Application.builder().token(secret.bot_token).build()
    application.add_handler(MessageHandler((~filters.COMMAND), start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    pass


if __name__ == "__main__":
    main()
