from typing import Final

import telegram
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup)
import olimp
import re
import newsmaker
from telegram.ext import (CallbackContext)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.ext import CallbackQueryHandler

import db_handler as db
import json
from telegram.ext import CallbackQueryHandler

TOKEN: Final = '6512036614:AAHAT909IhiSwHO8FdVS3UoY2eH5rJeNTlE'
BOT_USERNAME: Final = '@olymp_aibot'
USER_STATES_FILE = "user_states.json"
USER_STATE = {}
new_account = 'new account'
collecting_password = 'collecting_password'
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler

# Define your custom keyboard
custom_keyboard = [['/start', '/login'],
                   ['/news', '/affiliate']]

reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    print(f'{update.effective_chat.id} trying to Login')
    if db.get_user_data(user_id)['verified']:
        login_text = "What do you want to Update ?"

        buttons = [
            InlineKeyboardButton("Change Mail", callback_data=new_account),
            InlineKeyboardButton("Change Password", callback_data=collecting_password)]
        login_keyboard = InlineKeyboardMarkup([buttons])  # Wrap the buttons list in another list

        # Send a message with the inline keyboard
        await update.message.reply_text(login_text, reply_markup=login_keyboard)

    else:
        if db.get_user_data(user_id)['stage'][0] == collecting_password:
            await update.message.reply_text("Enter your password", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Enter your mail address", reply_markup=reply_markup)
            db.update(user_id, stage=[new_account, 0])


async def starter_pack(update, context):
    if not db.check_user_existence(update.effective_chat.id):
        db.update(update.effective_chat.id)
        print(f'{update.effective_chat.id} Signed-in')
    # send custom message to 6117341471
    await update.message.reply_text("👋 Welcome its Olymp AI", reply_markup=reply_markup)
    await update.message.reply_text("~A Trader without emotions 😎")
    await context.bot.sendDocument(update.effective_chat.id, document=open('Olymp AI Guide.pdf', 'rb'),
                                   caption="Help-book for Olymp AI 📈")


async def news(update: Update, content: ContextTypes.DEFAULT_TYPE):
    news = newsmaker.top_news()
    await update.message.reply_text(news[0])
    await update.message.reply_text(news[1])


async def affiliate(update: Update, content: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    print(f'{user_id} trying to enter Affiliate')
    buttons = [
        InlineKeyboardButton("Enter Promo-code", callback_data='promo'),
        InlineKeyboardButton("Affiliate Dashbord", callback_data='af_portal')]
    af_keyboard = InlineKeyboardMarkup([buttons])  # Wrap the buttons list in another list
    await update.message.reply_text('What do you like to have', reply_markup=af_keyboard)


def handel_response(text: str):
    processed: str = text.lower()
    if 'trade' in text:
        return "Your trade will be executed soon"


async def handel_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').split()
            response: str = handel_response(new_text)
        else:
            return
    else:
        response: str = handel_response(text)

    await update.message.reply_text(response)


async def login_btn_function(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.message.chat.id
    callback_data = query.data  # Get the callback data

    if callback_data == new_account:
        await query.message.edit_text("Enter your mail address")

    elif callback_data == collecting_password:
        await query.message.edit_text("Enter your password")

    db.update(user_id, stage=[callback_data, 0], verified=0)


async def affilate_btn_function(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.message.chat.id
    callback_data = query.data  # Get the callback data

    if callback_data == 'promo':
        await query.message.edit_text("Enter Your Promo-code")
        db.update(user_id, stage=['promo', 0])

    elif callback_data == 'af_portal':
        await query.message.edit_text(f'Affiliate code: {user_id}\n'
                                      f'Affiliates: {0}\n'
                                      f'Earnings: 0$')


async def handle_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE, ):
    user_id = update.message.chat.id

    if db.get_user_data(user_id)['stage'][0] == new_account:
        mail = update.message.text
        print(f'Pasword: "{mail}" tried by {user_id} ')
        # Validate the mail using a regular expression
        if re.match(r"[^@]+@[^@]+\.[^@]+", mail):
            await update.message.reply_text("Enter your Password")
            db.update(user_id, mail=mail, stage=[collecting_password, 0])
        else:
            if db.get_user_data(user_id)['stage'][1] > 1:
                await update.message.reply_text(rf"Limit Crossed try to /login again.")
                db.update(user_id, stage=[None, 0])
            else:
                await update.message.reply_text(
                    f"[{db.get_user_data(user_id)['stage'][1] + 2}] Wrong Mail ID try again")
                db.update(user_id, stage=[new_account, db.get_user_data(user_id)['stage'][1] + 1])

    elif db.get_user_data(user_id)['stage'][0] == collecting_password:
        password = update.message.text
        print(f'Pasword: "{password}" tried by {user_id}  with {password}')
        await update.message.reply_text("Wait while verifying the credentials...")
        # Validate the mail using a regular expression
        if olimp.cred_check(user_id, mail=db.get_user_data(user_id)['mail'], password=password):
            db.update(user_id, password=password, stage=[None, 0], verified=1)
            await update.message.reply_text(
                f'✅ Verified Successfully ', reply_markup=reply_markup)
            db.update(user_id, stage=[None, 0])
        else:

            if db.get_user_data(user_id)['stage'][1] > 1:
                await update.message.reply_text(
                    rf"[{db.get_user_data(user_id)['stage'][1] + 2}] Limit Crossed try to /login again.")
                db.update(user_id, stage=[None, 0])
            else:
                await update.message.reply_text(
                    f'Mail ID:     \t{db.get_user_data(user_id)["mail"]}\nPassword: \t{password}\n\n Wrong Credentials Provided ')
                db.update(user_id, stage=[collecting_password, db.get_user_data(user_id)['stage'][1] + 1])

    elif db.get_user_data(user_id)['stage'][0] == 'promo':
        promo = update.message.text
        print(promo)
        if db.check_user_existence(int(promo)):
            await update.message.reply_text('Your affiliate is added it may take 24hrs.')
            db.update(user_id, stage=[None, 0], affiliate=promo)
            await app.send_message(6117341471, text=fr'{promo} affiliated with {user_id}')
        else:
            await update.message.reply_text("Affiliate doesn't Exist")
            db.update(user_id, stage=[None, 0], affiliate=None)


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', starter_pack))
    app.add_handler(CommandHandler('login', login))
    app.add_handler(CommandHandler('affiliate', affiliate))
    app.add_handler(CommandHandler('news', news))

    app.add_handler(MessageHandler(filters.TEXT, handle_credentials))

    app.add_handler(CallbackQueryHandler(login_btn_function, pattern='^new account$'))
    app.add_handler(CallbackQueryHandler(login_btn_function, pattern='^collecting_password$'))
    app.add_handler(CallbackQueryHandler(affilate_btn_function, pattern='^promo$'))
    app.add_handler(CallbackQueryHandler(affilate_btn_function, pattern='^af_portal'))

    # Add the conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', starter_pack)],
        states={"CONVERSATION": [MessageHandler(filters.TEXT & ~filters.COMMAND, starter_pack)]},
        fallbacks=[],
    )
    app.add_handler(conversation_handler)

    print('Polling...')
    app.run_polling(poll_interval=1)
