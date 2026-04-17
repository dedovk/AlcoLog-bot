from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, date

from states.states import AddRecordSG, CalendarViewSG
from keyboards import get_start_keyboard, get_month_calendar, get_day_details_keyboard
from database.models import User, DrinkRecord

router = Router()


@router.callback_query(F.data == "add_drink")
async def add_drink_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle Add Drink button"""
    await callback.answer()

    text = locale.get("add-drink-prompt")
    await callback.message.edit_text(text)
    await state.set_state(AddRecordSG.waiting_for_drink)


@router.callback_query(F.data == "view_history")
async def view_history_callback(callback: CallbackQuery, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Handle View History button"""
    await callback.answer()

    try:
        # Get user's drink records
        stmt = select(DrinkRecord).where(DrinkRecord.user_id == user.id)
        result = await session.execute(stmt)
        records = result.scalars().all()

        if not records:
            text = locale.get("history-empty")
        else:
            header = locale.get("history-header")
            text = header + "\n\n"

            for record in records:
                date_str = record.created_at.strftime(
                    "%d.%m.%Y %H:%M") if record.created_at else "N/A"
                text += f"🍷 {record.drink_name} - {record.amount} {record.amount_unit} ({date_str})\n"

        await callback.message.edit_text(text, reply_markup=get_start_keyboard())
    except Exception as e:
        error_text = locale.get("error-database")
        await callback.message.edit_text(error_text, reply_markup=get_start_keyboard())


@router.callback_query(F.data == "view_stats")
async def view_stats_callback(callback: CallbackQuery, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Handle View Stats button"""
    await callback.answer()

    try:
        # Get total records count
        stmt = select(DrinkRecord).where(DrinkRecord.user_id == user.id)
        result = await session.execute(stmt)
        records = result.scalars().all()
        total = len(records)

        stats_text = locale.get("stats-total", total=total)
        stats_text += "\n\n📅 Переглянути по календарю →"

        # Build stats keyboard with calendar button
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        builder = InlineKeyboardBuilder()
        builder.button(text="📅 Календар", callback_data="show_calendar")
        builder.button(text="◀️ Назад", callback_data="back_to_menu")
        builder.adjust(5)

        await callback.message.edit_text(stats_text, reply_markup=builder.as_markup())
    except Exception:
        error_text = locale.get("error-database")
        await callback.message.edit_text(error_text, reply_markup=get_start_keyboard())


@router.callback_query(F.data == "show_help")
async def show_help_callback(callback: CallbackQuery, locale: TranslatorRunner):
    """Handle Help button"""
    await callback.answer()

    help_text = locale.get("help-text")
    try:
        await callback.message.edit_text(help_text, reply_markup=get_start_keyboard())
    except Exception:
        # If message content is same, just answer
        await callback.answer(help_text, show_alert=False)


@router.callback_query(F.data == "skip_field")
async def skip_field_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle Skip button in FSM flow"""
    await callback.answer()

    current_state = await state.get_state()

    # Get next state prompt based on current state
    data = await state.get_data()

    if current_state == AddRecordSG.waiting_for_drink:
        # Can't skip drink name
        error_text = locale.get("error-invalid-input")
        await callback.answer(error_text, show_alert=True)
        return

    elif current_state == AddRecordSG.waiting_for_amount:
        # Skip amount, go to price
        text = locale.get("add-price-prompt")
        await state.update_data(amount=0, amount_unit="ml")
        await callback.message.edit_text(text)
        await state.set_state(AddRecordSG.waiting_for_price)

    elif current_state == AddRecordSG.waiting_for_price:
        # Skip price, go to note
        text = locale.get("add-note-prompt")
        await state.update_data(price=None)
        await callback.message.edit_text(text)
        await state.set_state(AddRecordSG.waiting_for_note)

    elif current_state == AddRecordSG.waiting_for_note:
        # Skip note, confirm record (handled in message handler)
        pass


@router.callback_query(F.data == "confirm_record")
async def confirm_record_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle Confirm button"""
    await callback.answer()

    current_state = await state.get_state()
    data = await state.get_data()

    # Check if all required fields are filled
    if not data.get("drink_name"):
        error_text = locale.get("error-invalid-input")
        await callback.answer(error_text, show_alert=True)
        return

    confirm_text = f"✅ {locale.get('start-menu-text')}"
    try:
        await callback.message.edit_text(confirm_text, reply_markup=get_start_keyboard())
    except Exception:
        # If message content is same, don't edit
        pass
    await state.clear()


@router.callback_query(F.data == "cancel_add")
async def cancel_add_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle Cancel button"""
    await callback.answer()

    cancel_text = locale.get("cancel-confirmed")
    menu_text = locale.get("start-menu-text")

    try:
        await callback.message.edit_text(
            f"{cancel_text}\n\n{menu_text}",
            reply_markup=get_start_keyboard()
        )
    except Exception:
        # If message content is same, don't edit
        pass
    await state.clear()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle Back to Menu button"""
    await callback.answer()
    await state.clear()

    menu_text = locale.get("start-menu-text")
    try:
        await callback.message.edit_text(menu_text, reply_markup=get_start_keyboard())
    except Exception:
        # If message content is same, don't edit
        pass


@router.callback_query(F.data == "skip_field")
async def skip_field_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle Skip button in FSM flow"""
    await callback.answer()

    current_state = await state.get_state()

    # Get next state prompt based on current state
    data = await state.get_data()

    if current_state == AddRecordSG.waiting_for_drink:
        # Can't skip drink name
        error_text = locale.get("error-invalid-input")
        await callback.answer(error_text, show_alert=True)
        return

    elif current_state == AddRecordSG.waiting_for_amount:
        # Skip amount, go to price
        text = locale.get("add-price-prompt")
        await state.update_data(amount=0, amount_unit="ml")
        await callback.message.edit_text(text)
        await state.set_state(AddRecordSG.waiting_for_price)

    elif current_state == AddRecordSG.waiting_for_price:
        # Skip price, go to note
        text = locale.get("add-note-prompt")
        await state.update_data(price=None)
        await callback.message.edit_text(text)
        await state.set_state(AddRecordSG.waiting_for_note)

    elif current_state == AddRecordSG.waiting_for_note:
        # Skip note, confirm record (handled in message handler)
        pass


@router.callback_query(F.data == "confirm_record")
async def confirm_record_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle Confirm button"""
    await callback.answer()

    current_state = await state.get_state()
    data = await state.get_data()

    # Check if all required fields are filled
    if not data.get("drink_name"):
        error_text = locale.get("error-invalid-input")
        await callback.answer(error_text, show_alert=True)
        return

    confirm_text = f"✅ {locale.get('start-menu-text')}"
    try:
        await callback.message.edit_text(confirm_text, reply_markup=get_start_keyboard())
    except Exception:
        # If message content is same, don't edit
        pass
    await state.clear()


@router.callback_query(F.data == "cancel_add")
async def cancel_add_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle Cancel button"""
    await callback.answer()

    cancel_text = locale.get("cancel-confirmed")
    menu_text = locale.get("start-menu-text")

    try:
        await callback.message.edit_text(
            f"{cancel_text}\n\n{menu_text}",
            reply_markup=get_start_keyboard()
        )
    except Exception:
        # If message content is same, don't edit
        pass
    await state.clear()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle Back to Menu button"""
    await callback.answer()
    await state.clear()

    menu_text = locale.get("start-menu-text")
    try:
        await callback.message.edit_text(menu_text, reply_markup=get_start_keyboard())
    except Exception:
        # If message content is same, don't edit
        pass


# ============ CALENDAR HANDLERS ============

@router.callback_query(F.data == "show_calendar")
async def show_calendar_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Handle Show Calendar button"""
    await callback.answer()

    # Get current month
    today = datetime.now()
    year, month = today.year, today.month

    # Generate calendar
    keyboard, header = await get_month_calendar(year, month, user.id, session)

    try:
        await callback.message.edit_text(header, reply_markup=keyboard)
    except Exception:
        pass

    await state.set_state(CalendarViewSG.viewing_calendar)


@router.callback_query(F.data.startswith("cal_day_"))
async def calendar_day_callback(callback: CallbackQuery, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Handle click on specific day in calendar"""
    await callback.answer()

    # Parse callback data: cal_day_2025_01_15
    parts = callback.data.split("_")
    try:
        year, month, day = int(parts[2]), int(parts[3]), int(parts[4])
    except (IndexError, ValueError):
        await callback.answer("Помилка при розборі дати", show_alert=True)
        return

    from datetime import timedelta
    selected_date = date(year, month, day)

    # Query records for this day
    next_day = selected_date + timedelta(days=1)
    stmt = select(DrinkRecord).where(
        and_(
            DrinkRecord.user_id == user.id,
            DrinkRecord.created_at >= datetime.combine(
                selected_date, datetime.min.time()),
            DrinkRecord.created_at < datetime.combine(
                next_day, datetime.min.time())
        )
    ).order_by(DrinkRecord.created_at.desc())

    result = await session.execute(stmt)
    records = result.scalars().all()

    # Format day details
    date_str = selected_date.strftime("%d.%m.%Y")
    day_text = f"📊 {date_str}\n\n"

    if not records:
        day_text += "❌ Немає записів за цей день"
    else:
        day_text += f"🍷 Напитків: {len(records)}\n\n"

        total_amount = 0
        total_price = 0

        for i, record in enumerate(records, 1):
            day_text += f"{i}. {record.drink_name}"
            if record.amount:
                day_text += f" - {record.amount} {record.amount_unit}"
                total_amount += record.amount
            if record.price:
                day_text += f" ({record.price} грн)"
                total_price += record.price
            if record.note:
                day_text += f" | {record.note}"
            day_text += "\n"

        day_text += f"\n📈 Всього: {total_amount} мл" if total_amount > 0 else ""
        day_text += f"\n💰 Витрачено: {total_price} грн" if total_price > 0 else ""

    try:
        await callback.message.edit_text(day_text, reply_markup=get_day_details_keyboard())
    except Exception:
        pass


@router.callback_query(F.data.startswith("cal_prev_"))
async def calendar_prev_month_callback(callback: CallbackQuery, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Handle previous month button"""
    await callback.answer()

    # Parse current month
    parts = callback.data.split("_")
    try:
        year, month = int(parts[2]), int(parts[3])
    except (IndexError, ValueError):
        return

    # Go to previous month
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1

    # Generate calendar
    keyboard, header = await get_month_calendar(year, month, user.id, session)

    # Update callback_data for nav buttons
    keyboard.inline_keyboard[-2][0].callback_data = f"cal_prev_{year}_{month}"
    keyboard.inline_keyboard[-2][1].callback_data = f"cal_next_{year}_{month}"

    try:
        await callback.message.edit_text(header, reply_markup=keyboard)
    except Exception:
        pass


@router.callback_query(F.data.startswith("cal_next_"))
async def calendar_next_month_callback(callback: CallbackQuery, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Handle next month button"""
    await callback.answer()

    # Parse current month
    parts = callback.data.split("_")
    try:
        year, month = int(parts[2]), int(parts[3])
    except (IndexError, ValueError):
        return

    # Go to next month
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1

    # Generate calendar
    keyboard, header = await get_month_calendar(year, month, user.id, session)

    # Update callback_data for nav buttons
    keyboard.inline_keyboard[-2][0].callback_data = f"cal_prev_{year}_{month}"
    keyboard.inline_keyboard[-2][1].callback_data = f"cal_next_{year}_{month}"

    try:
        await callback.message.edit_text(header, reply_markup=keyboard)
    except Exception:
        pass


@router.callback_query(F.data == "cal_back_to_month")
async def calendar_back_to_month_callback(callback: CallbackQuery, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Handle back to calendar from day details"""
    await callback.answer()

    # Show current month calendar
    today = datetime.now()
    year, month = today.year, today.month

    keyboard, header = await get_month_calendar(year, month, user.id, session)

    try:
        await callback.message.edit_text(header, reply_markup=keyboard)
    except Exception:
        pass


@router.callback_query(F.data == "cal_back_to_menu")
async def calendar_back_to_menu_callback(callback: CallbackQuery, state: FSMContext, locale: TranslatorRunner):
    """Handle back to menu from calendar"""
    await callback.answer()
    await state.clear()

    menu_text = locale.get("start-menu-text")
    try:
        await callback.message.edit_text(menu_text, reply_markup=get_start_keyboard())
    except Exception:
        pass
