from aiogram import Router, types
from aiogram.types import Message

message_router = Router()


@message_router.message()
async def forward_with_text(message: Message):
    pass