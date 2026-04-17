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

record-saved = ✅ Запись сохранена!
    Напиток: { $drink_name }
    Объем: { $amount } { $amount_unit }
    { $price_text }

cancel-confirmed = ❌ Операция отменена.

history-empty = 📭 История пуста. Добавьте вашу первую запись!

history-header = 📋 Ваша история напитков:

error-invalid-input = ❌ Неверный ввод. Попробуйте еще раз.

error-database = ❌ Ошибка базы данных. Попробуйте позже.

stats-total = 📊 Всего записей: { $total }

stats-last-week = 📅 За последнюю неделю: { $count }
