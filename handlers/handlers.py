from aiogram import F, Router, flags, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import kb
import text
import utils
from main import Bot
from states import Edit, Gen

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(
        text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu
    )


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "generate_text")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text(text.gen_text)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)


@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    res = await utils.generate_text(prompt)
    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.edit_text(res[0], disable_web_page_preview=True)


@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_prompt)
    await clbck.message.edit_text(text.gen_image)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)


@router.message(Gen.img_prompt)
@flags.chat_action("upload_photo")
async def generate_image(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    img_res = await utils.generate_image(prompt)
    if len(img_res) == 0:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.delete()
    await mesg.answer_photo(photo=img_res[0])


@router.callback_query(F.data == "edit_image")
async def input_orig_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Edit.orig_img)
    await clbck.message.edit_text(text.orig_img)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)


file_ids = []


@router.message(Edit.orig_img)
async def get_orig(message: types.Message, state: FSMContext, bot: Bot):
    file_id = message.photo[-1].file_id
    destination = f"/Users/zhansen/Pictures/{file_id}.png"
    file_ids.append(file_id)
    await bot.download(message.photo[-1], destination)
    await message.answer("Now send an image with a mask")
    await state.set_state(Edit.mask_img)


@router.message(Edit.mask_img)
async def get_mask(message: types.Message, state: FSMContext, bot: Bot):
    file_id = message.photo[-1].file_id
    destination = f"/Users/zhansen/Pictures/{file_id}.png"
    file_ids.append(file_id)
    await bot.download(message.photo[-1], destination)
    await message.answer("Now write a text prompt")
    await state.set_state(Edit.edit_prompt)


@router.message(Edit.edit_prompt, F.text)
async def send_edited_img(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    img_res = await utils.edit_image(file_ids[0], file_ids[1], prompt)
    if len(img_res) == 0:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.delete()
    await mesg.answer_photo(photo=img_res[0])
