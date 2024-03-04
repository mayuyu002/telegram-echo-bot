from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater, MessageHandler, Filters
import random

# Dictionary to store user balances
user_balances = {}
# Dictionary to store referral links and their associated users
referral_links = {}

# Function to display the main menu
def display_main_menu(update, context):
    keyboard = [[InlineKeyboardButton("Earn", callback_data='earn')],
                [InlineKeyboardButton("Wallet", callback_data='wallet')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_chat.send_message('Welcome to the Captcha Earning bot! Click on the button to earn or check your wallet:', reply_markup=reply_markup)

# Callback handler for the 'Earn' button
def earn(update, context):
    user_data = context.user_data
    captcha = generate_captcha()
    user_data['captcha'] = captcha
    update.callback_query.answer()
    update.callback_query.edit_message_text(f"Please enter the following captcha: {captcha}")

# Message handler for processing captcha input
def process_captcha_input(update, context):
    user_data = context.user_data
    captcha = user_data.get('captcha')

    if captcha and update.message.text == captcha:
        user_id = update.effective_user.id
        user_balances[user_id] = user_balances.get(user_id, 0) + 0.04
        update.message.reply_text("Congratulations! You have earned 0.04 Pesos.")

        # Offer options to user
        display_main_menu(update, context)

    else:
        update.message.reply_text("Incorrect captcha. Please try again.")

# Callback handler for 'Earn More' and 'Wallet' buttons
def handle_earn_or_wallet(update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'earn':
        captcha = generate_captcha()
        context.user_data['captcha'] = captcha
        query.edit_message_text(f"Please enter the following captcha: {captcha}")
    elif query.data == 'wallet':
        wallet(update, context)  # Show wallet balance

# Callback handler for 'Back' button
def back(update, context):
    query = update.callback_query
    query.answer()
    display_main_menu(update, context)  # Redirect back to main menu

# Callback handler for 'Wallet' button
def wallet(update, context):
    user_id = update.effective_user.id
    balance = user_balances.get(user_id, 0)
    update.callback_query.answer()

    keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(f"Your current balance: {balance} Pesos.\nPress 'Back' to return.", reply_markup=reply_markup)

# Function to generate a random captcha
def generate_captcha():
    captcha = ''.join(random.choices('0123456789ABCDEF', k=6))
    return captcha

# Command handler for /start command with referral link
def start(update, context):
    if context.args and context.args[0] in referral_links:
        referral_user_id = referral_links[context.args[0]]
        referred_user_id = update.effective_user.id
        if referral_user_id != referred_user_id:  # Ensure user is not referring themselves
            user_balances[referral_user_id] = user_balances.get(referral_user_id, 0) + 5
            update.message.reply_text("You joined through a referral link. Your referrer has earned 5 Pesos!")
    display_main_menu(update, context)

# Function to handle referral link generation
def generate_referral_link(update, context):
    referral_code = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))
    referral_links[referral_code] = update.effective_user.id
    update.message.reply_text(f"Your referral link: https://t.me/Jshsjsjajsbot?start={referral_code}")

def main():
    # Replace "YOUR_BOT_TOKEN" with your actual bot token
    updater = Updater(token="7140712988:AAETwSbqijd3AUQMRL588afX7QPl6veOS8Y", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start, pass_args=True))
    dispatcher.add_handler(CommandHandler("referral", generate_referral_link))

    # Register callback query handlers
    dispatcher.add_handler(CallbackQueryHandler(earn, pattern='^earn$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_earn_or_wallet, pattern='^(earn|wallet)$'))
    dispatcher.add_handler(CallbackQueryHandler(back, pattern='^back$'))

    # Register message handler for captcha input
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_captcha_input))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
