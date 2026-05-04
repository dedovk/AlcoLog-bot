# Russian translations for AlcoLog bot

start-welcome = Привет, { $first_name }! 👋
    Добро пожаловать в AlcoLog - бот для ведения календаря употребления алкоголя.

start-menu-text = Что вы хотите сделать?

help-text = 📖 Справка:
    /start - Начать работу
    /add - Добавить запись о напитке
    /history - Просмотреть историю
    /stats - Статистика

add-drink-prompt = 📝 Название напитка:
    Пожалуйста, введите название напитка (например: пиво, вино, водка и т.д.).

add-amount-prompt = 📊 Объем:
    Введите объем в мл или количество единиц.

add-price-prompt = 💰 Цена:
    Введите цену (необязательно, можно пропустить).

add-note-prompt = 📌 Примечание:
    Добавьте примечание или описание (необязательно, можно пропустить).

select-unit-prompt = Выберите единицу измерения:

record-saved = ✅ Запись сохранена!
    Напиток: { $drink_name }
    Объем: { $amount } { $amount_unit }
    { $price_text }

cancel-confirmed = ❌ Операция отменена.

record-price = Цена: { $price } грн.

record-note = Примечание: { $note }

record-info = ✅ Запись сохранена!
    🍷 Напиток: { $drink_name }
    📊 Объем: { $amount } { $amount_unit }{ $price_info }{ $note_info }

history-empty = 📭 История пуста. Добавьте вашу первую запись!

history-header = 📋 Ваша история напитков:

error-invalid-input = ❌ Неверный ввод. Попробуйте еще раз.

error-database = ❌ Ошибка базы данных. Попробуйте позже.

stats-total = 📊 Всего записей: { $total }

stats-last-week = 📅 За последнюю неделю: { $count }
stats-days = 📅 Дней с записями: { $days }
stats-unique-drinks = 🍸 Разных напитков: { $count }
stats-total-spent = 💰 Потрачено всего: { $amount } грн
stats-average-price = 🔎 Средняя цена за запись: { $price } грн
stats-most-popular-drink = ⭐ Самый популярный напиток: { $drink }

stats-calendar-prompt = 📅 Просмотреть по календарю →

# Calendar translations
month-january = Январь
month-february = Февраль
month-march = Март
month-april = Апрель
month-may = Май
month-june = Июнь
month-july = Июль
month-august = Август
month-september = Сентябрь
month-october = Октябрь
month-november = Ноябрь
month-december = Декабрь

calendar-header = 📅 { $month } { $year }
calendar-stat = 📊 { $days_count } дней • { $drinks_count } напитков

day-no-records = ❌ Нет записей за этот день
day-drinks-count = 🍷 Напитки: { $count }
day-total-amount = 📈 Всего: { $amount } мл
day-total-price = 💰 Потрачено: { $price } грн

error-date-parse = ❌ Ошибка при разборе даты

# Delete record translations
delete-confirm-prompt = 🗑️ Вы уверены, что хотите удалить ВСЕ записи за этот день?
delete-single-confirm = 🗑️ Вы уверены, что хотите удалить эту запись?
delete-success = ✅ Записи успешно удалены!
delete-cancelled = ❌ Удаление отменено.
