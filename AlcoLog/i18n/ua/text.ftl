# Ukrainian translations for AlcoLog bot

start-welcome = Привіт, { $first_name }! 👋
    Ласкаво просимо до AlcoLog - бота для ведення календарю випивання алкоголю.

start-menu-text = Що ви бажаєте зробити?

help-text = 📖 Справка:
    /start - Почати роботу
    /add - Додати запис про напиток
    /history - Переглянути історію
    /stats - Статистика

add-drink-prompt = 📝 Назва напитку:
    Будь ласка, введіть назву напитку (наприклад: пиво, вино, водка, тощо).

add-amount-prompt = 📊 Обсяг:
    Введіть обсяг в мл або кількість одиниць.

add-price-prompt = 💰 Ціна:
    Введіть ціну (опціонально, можна пропустити).

add-note-prompt = 📌 Примітка:
    Додайте примітку або опис (опціонально, можна пропустити).

select-unit-prompt = Оберіть одиницю виміру:

record-saved = ✅ Запис збережено!
    Напиток: { $drink_name }
    Обсяг: { $amount } { $amount_unit }
    { $price_text }

cancel-confirmed = ❌ Операція скасована.

record-price = Ціна: { $price } грн.

record-note = Примітка: { $note }

record-info = ✅ Запис збережено!
    🍷 Напиток: { $drink_name }
    📊 Кількість: { $amount } { $amount_unit }{ $price_info }{ $note_info }

history-empty = 📭 Історія порожня. Додайте свій перший запис!

history-header = 📋 Ваша історія напитків:

error-invalid-input = ❌ Невірний ввід. Спробуйте ще раз.

error-database = ❌ Помилка бази даних. Спробуйте пізніше.

stats-total = 📊 Всього записів: { $total }

stats-last-week = 📅 За останній тиждень: { $count }

stats-calendar-prompt = 📅 Переглянути по календарю →

# Calendar translations
month-january = Січень
month-february = Лютий
month-march = Березень
month-april = Квітень
month-may = Май
month-june = Червень
month-july = Липень
month-august = Август
month-september = Вересень
month-october = Жовтень
month-november = Листопад
month-december = Грудень

calendar-header = 📅 { $month } { $year }
calendar-stat = 📊 { $days_count } днів • { $drinks_count } напитків

day-no-records = ❌ Немає записів за цей день
day-drinks-count = 🍷 Напитків: { $count }
day-total-amount = 📈 Всього: { $amount } мл
day-total-price = 💰 Витрачено: { $price } грн

error-date-parse = ❌ Помилка при розборі дати

# Delete record translations
delete-confirm-prompt = 🗑️ Ви впевнені, що бажаєте видалити ВСІ записи за цей день?
delete-single-confirm = 🗑️ Ви впевнені, що бажаєте видалити цей запис?
delete-success = ✅ Записи видалені успішно!
delete-cancelled = ❌ Видалення скасовано.