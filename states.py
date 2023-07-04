from aiogram.fsm.state import State, StatesGroup


class Gen(StatesGroup):
    text_prompt = State()
    img_prompt = State()


class Edit(StatesGroup):
    orig_img = State()
    mask_img = State()
    edit_prompt = State()
