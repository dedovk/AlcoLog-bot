import loguru
import time
import asyncio

from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from cachetools import TTLCache
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.db import AsyncSessionLocal
from database.models import User

caches = {"default": TTLCache(maxsize=10_000, ttl=0.1)}


class TranslateMiddleware(BaseMiddleware):
    """Middleware that injects translator into handler context"""

    def __init__(self, t_hub: TranslatorHub):
        self.t_hub = t_hub

    async def __call__(self, handler, event, data):
        # Get user language code
        user = event.from_user if hasattr(event, 'from_user') else None
        language = (user.language_code or "ua") if user else "ua"

        # Normalize language code (e.g., uk -> ua, en-US -> en)
        if language:
            language = language.split('-')[0].lower()
            if language == 'uk':
                language = 'ua'
        else:
            language = 'ua'

        # Get translator for user's language
        translator = self.t_hub.get_translator_by_locale(language)
        data["locale"] = translator

        return await handler(event, data)


class UserMiddleware(BaseMiddleware):
    """Middleware that fetches/creates user and injects into context"""

    async def __call__(self, handler, event, data):
        # Get user from Telegram
        telegram_user = event.from_user if hasattr(
            event, 'from_user') else None

        if telegram_user:
            async with AsyncSessionLocal() as session:
                # Try to find user in database
                stmt = select(User).where(User.id == telegram_user.id)
                result = await session.execute(stmt)
                user = result.scalars().first()

                if not user:
                    # Create new user
                    user = User(
                        id=telegram_user.id,
                        is_bot=telegram_user.is_bot,
                        first_name=telegram_user.first_name,
                        last_name=telegram_user.last_name,
                        username=telegram_user.username,
                        language_code=telegram_user.language_code,
                        is_premium=telegram_user.is_premium,
                        can_join_groups=telegram_user.can_join_groups,
                        can_read_all_groups_messages=telegram_user.can_read_all_group_messages,
                        supports_inline_queries=telegram_user.supports_inline_queries,
                    )
                    session.add(user)
                    await session.commit()
                else:
                    # Update user info
                    user.first_name = telegram_user.first_name
                    user.last_name = telegram_user.last_name
                    user.username = telegram_user.username
                    user.language_code = telegram_user.language_code
                    user.is_premium = telegram_user.is_premium
                    await session.commit()

                data["user"] = user

        return await handler(event, data)


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware for rate limiting users"""

    def __init__(self, rate_limit: float = 0.5):  # seconds between messages
        self.rate_limit = rate_limit
        self.caches = {"default": TTLCache(maxsize=10_000, ttl=rate_limit)}

    async def __call__(self, handler, event, data):
        # Get user id
        user_id = event.from_user.id if hasattr(event, 'from_user') else None

        if not user_id:
            return await handler(event, data)

        # Check if user is throttled
        cache = self.caches["default"]
        if user_id in cache:
            # User is throttled, skip handler
            loguru.logger.debug(f"User {user_id} is throttled")
            return

        # Record this request
        cache[user_id] = True

        return await handler(event, data)


class DatabaseMiddleware(BaseMiddleware):
    """Middleware that injects database session into context"""

    async def __call__(self, handler, event, data):
        async with AsyncSessionLocal() as session:
            data["session"] = session
            return await handler(event, data)
