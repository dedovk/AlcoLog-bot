import asyncio

from loguru import logger
from AlcoLog.utils.config import settings
from aiogram import Dispatcher, Bot
from aiogram.client.session.aiohttp import AiohttpSession
from AlcoLog.logs import setup_logger
from AlcoLog.handlers import router as main_router
from fluentogram import TranslatorHub, FluentTranslator
from fluent_compiler.bundle import FluentBundle
from AlcoLog.database.db import init_db, close_db
from AlcoLog.utils.middleware import TranslateMiddleware, UserMiddleware, ThrottlingMiddleware, DatabaseMiddleware


t_hub = TranslatorHub(
    {"ua": ("ua",), "ru": ("ru",), "en": ("en",)},
    translators=[
        FluentTranslator(locale="ua", translator=FluentBundle.from_files(
            "uk-UA", filenames=["AlcoLog/i18n/ua/text.ftl", "AlcoLog/i18n/ua/button.ftl"])),
        FluentTranslator(locale="ru", translator=FluentBundle.from_files(
            "ru-RU", filenames=["AlcoLog/i18n/ru/text.ftl", "AlcoLog/i18n/ru/button.ftl"])),
        FluentTranslator(locale="en", translator=FluentBundle.from_files(
            "en-US", filenames=["AlcoLog/i18n/eng/text.ftl", "AlcoLog/i18n/eng/button.ftl"])),
    ],
    root_locale="ua"
)


async def main():
    # Initialize database
    logger.info("Database initialized.")

    session = AiohttpSession()
    bot = Bot(token=settings.BOT_TOKEN, session=session)
    dp = Dispatcher(t_hub=t_hub)

    # Register middleware
    dp.message.middleware(TranslateMiddleware(t_hub))
    dp.message.middleware(UserMiddleware())
    dp.message.middleware(ThrottlingMiddleware(rate_limit=0.5))
    dp.message.middleware(DatabaseMiddleware())

    dp.callback_query.middleware(TranslateMiddleware(t_hub))
    dp.callback_query.middleware(UserMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware(rate_limit=1.0))
    dp.callback_query.middleware(DatabaseMiddleware())

    dp.include_router(main_router)

    setup_logger()

    logger.info("Bot is running.")

    try:
        await dp.start_polling(bot)
    except ValueError as e:
        logger.error(f"ValueError occurred: {e}")
    except KeyboardInterrupt as e:
        logger.error(f"Bot is stopped manually.")
    finally:
        await bot.session.close()
        await close_db()


if __name__ == '__main__':
    asyncio.run(main())
