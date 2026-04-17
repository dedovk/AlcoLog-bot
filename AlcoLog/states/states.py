from aiogram.fsm.state import StatesGroup, State


class AddRecordSG(StatesGroup):
    waiting_for_drink = State()
    waiting_for_amount = State()
    waiting_for_price = State()
    waiting_for_note = State()


class CalendarViewSG(StatesGroup):
    viewing_calendar = State()
