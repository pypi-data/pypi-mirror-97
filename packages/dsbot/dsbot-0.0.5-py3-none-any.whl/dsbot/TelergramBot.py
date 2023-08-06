from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler ,Filters, CallbackQueryHandler, CallbackContext
import logging

from .utils import BotConfig
from .commands.base.speech import Speech


class TelegramBot:

    def __init__(self, **kwargs):

        telegram_token = '1481896100:AAFUsMu2jSsTOGeFeEqx2uZ7T4vTg3BVWWY'
        if 'telegram_token' in kwargs:
            telegram_token = kwargs['telegram_token']

        self.config = BotConfig(kwargs)
        self.speech_manager = Speech(self.config)

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        self.updater = Updater(token=telegram_token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        hi_handler = CommandHandler('hi', self.hi)
        reset_handler = CommandHandler('reset', self.reset)
        photo_handler = CommandHandler('test', self.test)

        # commands
        self.dispatcher.add_handler(hi_handler)
        self.dispatcher.add_handler(photo_handler)
        self.dispatcher.add_handler(reset_handler)

        self.dispatcher.add_handler(CallbackQueryHandler(self.inline_keyboard_callback))

        # messages
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo))
        self.updater.start_polling()

    # Commands
    def hi(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm alive")

    def test(self, update, context):
        keyboard = [
            [
                InlineKeyboardButton("Option 1", callback_data="Option 1"),
            ],
            [
                InlineKeyboardButton("Option 2", callback_data="Option 2"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    # Receive User input
    def echo(self, update, context):
        """Echo the user message."""
        text = update.message.text
        self.process_text(text, update, context)

    # Inline Keyboard
    def inline_keyboard_callback(self, update, context):
        query = update.callback_query
        query.answer()
        data = query.data
        self.process_text(data, update, context)

    # Process Text
    def process_text(self, text, update, context):
        # case of empty text
        if not text:
            print("Bot: Nao entendi. Pode tentar novamente.")
            update.message.reply_text("Nao entendi")
        else:
            response = self.speech_manager.next(text)

            tag = response["tag"]
            message = response["message"]

            if "plot_result" in response["context"]:
                image = response["context"]["plot_result"]
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=image,
                    caption=message
                )
                del response["context"]
            elif "options" in response["context"]:
                options = response["context"]["options"]
                keyboard = [
                    [InlineKeyboardButton(option, callback_data=option) for option in options],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(update.effective_chat.id, 'Escolha uma opcao:', reply_markup=reply_markup)
                del response["context"]
            else:
                context.bot.send_message(update.effective_chat.id, message)