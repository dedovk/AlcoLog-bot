# English translations for AlcoLog bot

start-welcome = Hello, { $first_name }! 👋
    Welcome to AlcoLog - a bot for tracking your alcohol consumption calendar.

start-menu-text = What would you like to do?

help-text = 📖 Help:
    /start - Start working
    /add - Add a drink record
    /history - View history
    /stats - Statistics

add-drink-prompt = 📝 Drink name:
    Please enter the name of the drink (e.g., beer, wine, vodka, etc.).

add-amount-prompt = 📊 Amount:
    Enter the amount in ml or number of units.

add-price-prompt = 💰 Price:
    Enter the price (optional, can skip).

add-note-prompt = 📌 Note:
    Add a note or description (optional, can skip).

record-saved = ✅ Record saved!
    Drink: { $drink_name }
    Amount: { $amount } { $amount_unit }
    { $price_text }

cancel-confirmed = ❌ Operation cancelled.

history-empty = 📭 History is empty. Add your first record!

history-header = 📋 Your drink history:

error-invalid-input = ❌ Invalid input. Please try again.

error-database = ❌ Database error. Try again later.

stats-total = 📊 Total records: { $total }

stats-last-week = 📅 Last week: { $count }
