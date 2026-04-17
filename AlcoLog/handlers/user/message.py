from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from states.states import AddRecordSG
from keyboards import get_start_keyboard, get_skip_confirm_keyboard, get_amount_units_keyboard
from database.db import AsyncSessionLocal
from database.models import DrinkRecord, User
from sqlalchemy import select

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, locale: TranslatorRunner):
    """Handle /start command"""
    first_name = message.from_user.first_name or "User"

    text = locale.get("start-welcome", first_name=first_name)
    menu_text = locale.get("start-menu-text")

    await message.answer(
        f"{text}\n\n{menu_text}",
        reply_markup=get_start_keyboard()
    )


@router.message(Command("add"))
async def add_record_start(message: Message, state: FSMContext, locale: TranslatorRunner):
    """Start the AddRecord FSM flow"""
    text = locale.get("add-drink-prompt")

    await message.answer(text, reply_markup=get_skip_confirm_keyboard())
    await state.set_state(AddRecordSG.waiting_for_drink)


@router.message(AddRecordSG.waiting_for_drink, StateFilter(AddRecordSG.waiting_for_drink))
async def process_drink_name(message: Message, state: FSMContext, locale: TranslatorRunner):
    """Process drink name input"""
    drink_name = message.text.strip()

    if not drink_name or len(drink_name) > 255:
        error_text = locale.get("error-invalid-input")
        await message.answer(error_text)
        return

    await state.update_data(drink_name=drink_name)

    text = locale.get("add-amount-prompt")
    await message.answer(text, reply_markup=get_skip_confirm_keyboard())
    await state.set_state(AddRecordSG.waiting_for_amount)


@router.message(AddRecordSG.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext, locale: TranslatorRunner):
    """Process amount input"""
    amount_text = message.text.strip()

    # Try to parse as float
    try:
        amount = float(amount_text)
        if amount < 0:
            raise ValueError("Amount must be positive")
    except ValueError:
        error_text = locale.get("error-invalid-input")
        await message.answer(error_text)
        return

    await state.update_data(amount=amount, amount_unit="ml")

    text = locale.get("add-price-prompt")
    await message.answer(text, reply_markup=get_skip_confirm_keyboard())
    await state.set_state(AddRecordSG.waiting_for_price)


@router.message(AddRecordSG.waiting_for_price)
async def process_price(message: Message, state: FSMContext, locale: TranslatorRunner):
    """Process price input (optional)"""
    price_text = message.text.strip()
    price = None

    if price_text and price_text.lower() != "skip":
        try:
            price = float(price_text)
            if price < 0:
                raise ValueError("Price must be positive")
        except ValueError:
            error_text = locale.get("error-invalid-input")
            await message.answer(error_text)
            return

    await state.update_data(price=price)

    text = locale.get("add-note-prompt")
    await message.answer(text, reply_markup=get_skip_confirm_keyboard())
    await state.set_state(AddRecordSG.waiting_for_note)


@router.message(AddRecordSG.waiting_for_note)
async def process_note(message: Message, state: FSMContext, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Process note and save the record"""
    note = message.text.strip() if message.text else None

    if note and len(note) > 500:
        error_text = locale.get("error-invalid-input")
        await message.answer(error_text)
        return

    # Get data from state
    data = await state.get_data()

    try:
        # Create and save drink record
        record = DrinkRecord(
            user_id=user.id,
            drink_name=data.get("drink_name"),
            amount=data.get("amount"),
            amount_unit=data.get("amount_unit", "ml"),
            price=data.get("price"),
            note=note
        )

        session.add(record)
        await session.commit()

        # Prepare success message
        price_text = f"Ціна: {data.get('price')} грн." if data.get(
            'price') else ""
        success_text = locale.get(
            "record-saved",
            drink_name=data.get("drink_name"),
            amount=data.get("amount"),
            amount_unit=data.get("amount_unit"),
            price_text=price_text
        )

        await message.answer(success_text)

    except Exception as e:
        error_text = locale.get("error-database")
        await message.answer(error_text)
        return

    # Clear state and return to menu
    await state.clear()
    menu_text = locale.get("start-menu-text")
    await message.answer(menu_text, reply_markup=get_start_keyboard())


@router.message(Command("help"))
async def help_handler(message: Message, locale: TranslatorRunner):
    """Handle /help command"""
    text = locale.get("help-text")
    await message.answer(text, reply_markup=get_start_keyboard())


@router.message(Command("history"))
async def history_handler(message: Message, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Handle /history command"""
    try:
        # Get user's drink records
        stmt = select(DrinkRecord).where(DrinkRecord.user_id == user.id)
        result = await session.execute(stmt)
        records = result.scalars().all()

        if not records:
            text = locale.get("history-empty")
            await message.answer(text, reply_markup=get_start_keyboard())
            return

        header = locale.get("history-header")
        text = header + "\n\n"

        for record in records:
            date_str = record.created_at.strftime(
                "%d.%m.%Y %H:%M") if record.created_at else "N/A"
            text += f"🍷 {record.drink_name} - {record.amount} {record.amount_unit} ({date_str})\n"

        await message.answer(text, reply_markup=get_start_keyboard())

    except Exception as e:
        error_text = locale.get("error-database")
        await message.answer(error_text)


@router.message(Command("stats"))
async def stats_handler(message: Message, locale: TranslatorRunner, user: User, session: AsyncSession):
    """Handle /stats command"""
    try:
        # Get total records count
        stmt = select(DrinkRecord).where(DrinkRecord.user_id == user.id)
        result = await session.execute(stmt)
        records = result.scalars().all()
        total = len(records)

        stats_text = locale.get("stats-total", total=total)
        await message.answer(stats_text, reply_markup=get_start_keyboard())

    except Exception as e:
        error_text = locale.get("error-database")
        await message.answer(error_text)
