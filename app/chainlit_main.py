import logging

import chainlit as cl
from chainlit import on_chat_start
from consts import PRESENTATION
from models import Answer
from state import chat_bot


@on_chat_start
async def chat_start():
    logging.info("Loading Delta-Buddy...")
    await cl.Message(content=PRESENTATION).send()


@cl.on_message
async def on_message(question: str):
    logging.info(f'Question received from user: "{question}"')
    answer: Answer = chat_bot.chat(question=question)
    await cl.Message(content=answer.answer).send()
