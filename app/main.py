import logging

from fastapi import FastAPI

from app.models import LLMInput
from app.state import chat_bot

app = FastAPI()


@app.post("/")
async def llm(llm_input: LLMInput):
    logging.info(f"Received input: {llm_input})")
    answer = chat_bot.chat(question=llm_input.prompt)
    logging.info(f"Answering with the answer: {answer}")
    return answer.answer
