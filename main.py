import urllib

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
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {secret.api_key}",
    }
    # url2 = urllib.parse.quote(url)
    response = requests.get(url, headers=headers)

    # print(response.text)

    v1 = json.loads(response.content)
    v2 = v1["results"][:4]

    keyboard = [
        [
            InlineKeyboardButton(
                f"{i}",
                callback_data=x["id"],
            )
        ]
        for i, x in enumerate(v2)
    ]

    message = [
        f'{i}: {x["title"]} [{x["release_date"]}] {x["overview"]}'
        for i, x in enumerate(v2)
    ]

    await update.message.reply_text(
        "\n\n\n".join(message),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# TODO limit max length of message
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
