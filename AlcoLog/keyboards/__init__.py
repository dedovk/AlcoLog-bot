from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import calendar

from database.models import DrinkRecord


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard for /start"""
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Add Drink", callback_data="add_drink")
    builder.button(text="📋 History", callback_data="view_history")
    builder.button(text="📊 Stats", callback_data="view_stats")
    builder.button(text="📖 Help", callback_data="show_help")
    builder.adjust(2, 2)  # 2 buttons per row
    return builder.as_markup()


def get_skip_confirm_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with Skip and Confirm buttons"""
    builder = InlineKeyboardBuilder()
    builder.button(text="⏭️ Skip", callback_data="skip_field")
    builder.button(text="✅ Confirm", callback_data="confirm_record")
    builder.button(text="❌ Cancel", callback_data="cancel_add")
    builder.adjust(2, 1)  # 2 buttons in first row, 1 in second
    return builder.as_markup()


def get_amount_units_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting amount units"""
    builder = InlineKeyboardBuilder()
    builder.button(text="мл (ml)", callback_data="unit_ml")
    builder.button(text="одиниці (units)", callback_data="unit_units")
    builder.button(text="грами (g)", callback_data="unit_grams")
    builder.adjust(2, 1)
    return builder.as_markup()


def get_confirm_cancel_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with Confirm and Cancel buttons"""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Confirm", callback_data="confirm_record")
    builder.button(text="❌ Cancel", callback_data="cancel_add")
    builder.adjust(2)
    return builder.as_markup()


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with Back button"""
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Back to Menu", callback_data="back_to_menu")
    return builder.as_markup()


async def get_month_calendar(year: int, month: int, user_id: int, session: AsyncSession) -> tuple[InlineKeyboardMarkup, str]:
    """
    Generate calendar keyboard for the given month with marked days
    Returns: (keyboard, header_text)
    """
    # Get month name in Ukrainian
    month_names_ua = [
        "Січень", "Лютий", "Березень", "Квітень", "Май", "Червень",
        "Липень", "Август", "Вересень", "Жовтень", "Листопад", "Грудень"
    ]
    month_name = month_names_ua[month - 1]

    # Query ALL records for this user (no month filter in SQL - we'll filter in Python)
    stmt = select(DrinkRecord).where(DrinkRecord.user_id == user_id)
    result = await session.execute(stmt)
    all_records = result.scalars().all()

    # Filter by month in Python
    marked_days = {}
    for record in all_records:
        record_date = record.created_at.date()
        if record_date.year == year and record_date.month == month:
            day = record_date.day
            if day not in marked_days:
                marked_days[day] = {"count": 0, "amount": 0}
            marked_days[day]["count"] += 1
            if record.amount:
                marked_days[day]["amount"] += record.amount

    total_days_with_records = len(marked_days)
    total_drinks = sum(1 for r in all_records if r.created_at.date().year == year and r.created_at.date().month == month)

    # Create header
    header = f"📅 {month_name} {year}\n"
    header += f"📊 {total_days_with_records} днів • {total_drinks} напитків"

    # Build calendar grid
    cal = calendar.monthcalendar(year, month)
    builder = InlineKeyboardBuilder()

    # Add day names (Пн, Вт, etc)
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    # Note: We can't make row of text, so we'll add numbers directly

    # Add calendar days
    for week in cal:
        for day in week:
            if day == 0:
                # Empty cell before month starts or after month ends
                builder.button(text=" ", callback_data="dummy")
            elif day in marked_days:
                # Day with records - mark with green circle
                builder.button(text=f"🟢{day}", callback_data=f"cal_day_{year}_{month}_{day}")
            else:
                # Regular day
                builder.button(text=str(day), callback_data=f"cal_day_{year}_{month}_{day}")
        builder.adjust(7)  # 7 columns for days

    # Navigation buttons
    builder.button(text="◀️ Попередній", callback_data=f"cal_prev_{year}_{month}")
    builder.button(text="▶️ Наступний", callback_data=f"cal_next_{year}_{month}")
    builder.adjust(2)

    # Back button
    builder.button(text="◀️ В меню", callback_data="cal_back_to_menu")

    return builder.as_markup(), header


def get_day_details_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for day details view"""
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад до календаря", callback_data="cal_back_to_month")
    builder.button(text="➕ Додати запис", callback_data="add_drink")
    builder.button(text="🏠 В меню", callback_data="back_to_menu")
    builder.adjust(1, 2)
    return builder.as_markup()

