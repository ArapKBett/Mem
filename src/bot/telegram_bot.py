from telegram.ext import Updater, CommandHandler
from telegram.error import TelegramError
import logging

class TelegramBot:
    def __init__(self, token, channel_id):
        self.updater = Updater(token, use_context=True)
        self.channel_id = channel_id
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler("topgainers", self.top_gainers))
        self.dispatcher.add_error_handler(self.error_handler)

    def error_handler(self, update, context):
        logging.error(f"Telegram error: {context.error}")

    def send_message(self, message, image_path=None):
        """Send a message and optional image to the Telegram channel."""
        try:
            self.updater.bot.send_message(chat_id=self.channel_id, text=message, parse_mode="Markdown")
            if image_path:
                self.updater.bot.send_photo(chat_id=self.channel_id, photo=open(image_path, "rb"))
        except TelegramError as e:
            logging.error(f"Error sending Telegram message: {e}")

    def top_gainers(self, update, context):
        """Handle /topgainers command (for testing)."""
        update.message.reply_text("Fetching top gainers... Check the channel for updates!")

    def start(self):
        """Start the Telegram bot."""
        self.updater.start_polling()
        logging.info("Telegram bot started")

    def stop(self):
        """Stop the Telegram bot."""
        self.updater.stop()
