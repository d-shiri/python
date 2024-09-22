import telebot
from telebot import types
import re
from get_videos import (get_video_ids, get_n_top_videos, get_n_days)
from langs import translations
from general import format_number, get_bot_info


bot_token = 'YOUR_TOKEN_HERE'
bot = telebot.TeleBot(bot_token)
bot_info_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
bot.set_webhook()

user_language = {}
def get_videos(days, n):
    days = get_n_days(days)
    video_ids = get_video_ids(n, days)
    videos = get_n_top_videos(video_ids)
    videos = sorted(videos, key=lambda x: x['views'], reverse=True)[:n]
    return videos

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    lang_code = message.from_user.language_code
    # Check if the language code is supported, otherwise default to 'en'
    if lang_code not in translations:
        lang_code = 'en'
    # Store the user's language preference
    user_language[user_id] = lang_code
    language_menu(message.chat.id)

def language_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("English 🇬🇧", callback_data='lang_en')
    item2 = types.InlineKeyboardButton("🇮🇷فارسی", callback_data='lang_fa')
    item3 = types.InlineKeyboardButton("Deutsch 🇩🇪", callback_data='lang_de')
    item4 = types.InlineKeyboardButton("española 🇪🇸", callback_data='lang_es')
    item5 = types.InlineKeyboardButton("भारतीय 🇮🇳", callback_data='lang_in')
    item6 = types.InlineKeyboardButton("française 🇫🇷", callback_data='lang_fr')
    # Add more languages here
    markup.add(item1, item3)
    markup.add(item2, item4)
    markup.add(item5, item6)
    bot.send_message(chat_id, "Please select your language:", reply_markup=markup)

def main_menu(chat_id):
    lang = user_language.get(chat_id, 'en')  # Default to English if not set
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(translations[lang]['day'], callback_data='day')
    item2 = types.InlineKeyboardButton(translations[lang]['week'], callback_data='week')
    item3 = types.InlineKeyboardButton(translations[lang]['month'], callback_data='month')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(chat_id, translations[lang]['choose'], reply_markup=markup)


def escape_markdown(text):
    # Escape characters that can interfere with Markdown formatting
    escape_chars = r"*_[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def get_videos_menu(chat_id, days, n, thumbnail=True):
    videos_info = get_videos(days, n)
    if thumbnail:
        for vid in videos_info:
            url = f"https://www.youtube.com/watch?v={vid['videoId']}"
            # Create the markup for the button
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                text="Watch Video",
                url=url
            ))
            # Format the video title and views text, escaping Markdown characters
            views = format_number(int(vid['views']))
            title = escape_markdown(vid['title'])
            vidLang = escape_markdown(vid['lang'] if vid['lang'] else '🤷🏻‍♂️')
            chName = escape_markdown(vid['channelTitle'])
            # Escape the URL in the caption to prevent parsing issues
            escaped_url = escape_markdown(url)
            caption = (
                f"{escaped_url}\n\n"
                f"*Channel:* {chName}\n"
                f"*Title:* {title}\n"
                f"*Views:* {views}\n"
                f"*Language:* {vidLang}"
            )

            # Send the thumbnail image with the caption and button
            bot.send_photo(chat_id, photo=vid['thumbnail'], caption=caption, parse_mode='Markdown', reply_markup=markup)

        # Get user's language and send a final watch message if needed
        lang = user_language.get(chat_id, 'en')
        watch_text = translations[lang]['watch']
        bot.send_message(chat_id, watch_text)

# def get_videos_menu(chat_id, days, n, thumbnail=True):
#     videos_info = get_videos(days, n)
#     if thumbnail:
#         for idx, vid in enumerate(videos_info):
#             markup = types.InlineKeyboardMarkup()
#             views = format_number(int(vid['views']))
#             title = vid['title']
#             title = title if len(title) > 30 else title + ' ' * 15
#             markup.add(types.InlineKeyboardButton(f"[{views} views] {title}", url=f"https://www.youtube.com/watch?v={vid['videoId']}"))
#             bot.send_photo(chat_id, vid['thumbnail'], reply_markup=markup)
#         lang = user_language.get(chat_id, 'en')
#         watch_text = translations[lang]['watch']
#         bot.send_message(chat_id, watch_text)
    # else:
    # for idx, vid in enumerate(videos_info):
    #     markup = types.InlineKeyboardMarkup()
    #     views = format_number(int(vid['views']))
    #     title = vid['title']
    #     title = title if len(title) > 30 else title + ' ' * 15
    #     url = f"https://www.youtube.com/watch?v={vid['videoId']}"
    #     markup.add(types.InlineKeyboardButton(f"{idx}. [{views} views] {title}", url=url))
    #     bot.send_message(chat_id, url, reply_markup=markup)
    # lang = user_language.get(chat_id, 'en')
    # watch_text = translations[lang]['watch']
    # bot.send_message(chat_id, watch_text,)


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    callback_data = call.data
    bot.answer_callback_query(call.id)
    # Handle language selection
    if callback_data.startswith('lang_'):
        lang_code = callback_data.split('_')[1]
        user_language[call.message.chat.id] = lang_code
        main_menu(call.message.chat.id)  # Show the main menu in the selected language
    # Handle time range selection
    elif callback_data == 'day':
        lang = user_language.get(call.message.chat.id, 'en')
        bot.send_message(call.message.chat.id, translations[lang]['day'])
        get_videos_menu(call.message.chat.id, 1, 5)
        main_menu(call.message.chat.id)  # Show the main menu in the selected language
    elif callback_data == 'week':
        lang = user_language.get(call.message.chat.id, 'en')
        bot.send_message(call.message.chat.id, translations[lang]['week'])
        get_videos_menu(call.message.chat.id, 7, 5)
        main_menu(call.message.chat.id)  # Show the main menu in the selected language
    elif callback_data == 'month':
        lang = user_language.get(call.message.chat.id, 'en')
        bot.send_message(call.message.chat.id, translations[lang]['month'])
        get_videos_menu(call.message.chat.id, 30, 5)
        main_menu(call.message.chat.id)  # Show the main menu in the selected language

if __name__ == '__main__':
    get_bot_info(bot_info_url)
    bot.polling()

