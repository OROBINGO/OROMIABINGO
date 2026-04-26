import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Game state
numbers = list(range(1, 76))
called_numbers = []
game_active = False

# Start bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Welcome to Bingo Bot!\n\n"
        "/newgame - Start new game\n"
        "/call - Call next number\n"
        "/numbers - Show called numbers\n"
        "/reset - Reset game"
    )

# New game
async def newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global numbers, called_numbers, game_active
    numbers = list(range(1, 76))
    called_numbers = []
    game_active = True
    await update.message.reply_text("🆕 New Bingo Game Started! Numbers 1–75 ready.")

# Call number
async def call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global numbers, called_numbers, game_active

    if not game_active:
        await update.message.reply_text("⚠️ Start game first using /newgame")
        return

    if not numbers:
        await update.message.reply_text("🏁 All numbers finished!")
        return

    num = random.choice(numbers)
    numbers.remove(num)
    called_numbers.append(num)

    # Bingo letter
    if num <= 15:
        letter = "B"
    elif num <= 30:
        letter = "I"
    elif num <= 45:
        letter = "N"
    elif num <= 60:
        letter = "G"
    else:
        letter = "O"

    await update.message.reply_text(f"🎯 Number: {letter}-{num}")

# Show called numbers
async def show_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not called_numbers:
        await update.message.reply_text("No numbers called yet.")
    else:
        nums = ", ".join(map(str, sorted(called_numbers)))
        await update.message.reply_text(f"📋 Called Numbers:\n{nums}")

# Reset game
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global numbers, called_numbers, game_active
    numbers = list(range(1, 76))
    called_numbers = []
    game_active = False
    await update.message.reply_text("🔄 Game reset. Use /newgame to start again.")

# Run bot
if __name__ == "__main__":
    TOKEN = "8790858201:AAFazDtzz9wWUvlSo_fHxjNrydgO8P0PRBM
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newgame", newgame))
    app.add_handler(CommandHandler("call", call))
    app.add_handler(CommandHandler("numbers", show_numbers))
    app.add_handler(CommandHandler("reset", reset))

    print("Bot is running...")
    app.run_polling()