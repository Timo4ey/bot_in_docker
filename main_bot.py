# pylint: disable=no-name-in-module
import logging
from asyncpg import UndefinedParameterError
from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup,InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, CallbackQueryHandler, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
from config import tg_access_token
from memes_sender import send_memes_runner

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the bot"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )


async def button(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()
    
    if query.data != '0':
        await send_memes_runner(chat_id=update.effective_chat.id, hours = int(query.data)) 
    else:
        await query.edit_message_text(text = "Ok, if you want don't know how it's working just use /help")

async def send_memes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send memes"""
    await send_memes_runner(chat_id=update.effective_chat.id, hours = int(update.message.text))


async def agreement_buttons(update:Update, context:ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton('Yes', callback_data = update.message.text),
            InlineKeyboardButton('No', callback_data = '0')   


        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Do you want to get meme(s) for {update.message.text} hour(s)?', reply_markup=reply_markup)



async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """send caution if a user send unknown command"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Sorry, I didn't understand that command.")


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! \n I'm MemesBot, I've made for send memes \n If you want to get memes, just send me a number from 1 to 66 (1 == 1 hour) \n :3 \n ")    



if __name__ == '__main__':
    application = ApplicationBuilder().token(tg_access_token).build()
    

    start_handler = CommandHandler('start', start)
    helper_handler = CommandHandler('help', helper)
    memes_handler = MessageHandler(filters.Regex('^([0-66])'), agreement_buttons)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    
    application.add_handler(start_handler)
    application.add_handler(helper_handler)
    application.add_handler(memes_handler)
    application.add_handler(unknown_handler)
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()