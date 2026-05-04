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

select-unit-prompt = Select amount unit:

record-saved = ✅ Record saved!
    Drink: { $drink_name }
    Amount: { $amount } { $amount_unit }
    { $price_text }

cancel-confirmed = ❌ Operation cancelled.

record-price = Price: { $price } UAH

record-note = Note: { $note }

record-info = ✅ Record saved!
    🍷 Drink: { $drink_name }
    📊 Amount: { $amount } { $amount_unit }{ $price_info }{ $note_info }

history-empty = 📭 History is empty. Add your first record!

history-header = 📋 Your drink history:

error-invalid-input = ❌ Invalid input. Please try again.

error-database = ❌ Database error. Try again later.

stats-total = 📊 Total records: { $total }

stats-last-week = 📅 Last week: { $count }

stats-calendar-prompt = 📅 View by calendar →

# Calendar translations
month-january = January
month-february = February
month-march = March
month-april = April
month-may = May
month-june = June
month-july = July
month-august = August
month-september = September
month-october = October
month-november = November
month-december = December

calendar-header = 📅 { $month } { $year }
calendar-stat = 📊 { $days_count } days • { $drinks_count } drinks

day-no-records = ❌ No records for this day
day-drinks-count = 🍷 Drinks: { $count }
day-total-amount = 📈 Total: { $amount } ml
day-total-price = 💰 Spent: { $price } UAH

error-date-parse = ❌ Error parsing date

# Delete record translations
delete-confirm-prompt = 🗑️ Are you sure you want to delete ALL records for this day?
delete-single-confirm = 🗑️ Are you sure you want to delete this record?
delete-success = ✅ Records deleted successfully!
delete-cancelled = ❌ Deletion cancelled.
