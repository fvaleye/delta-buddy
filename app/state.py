import logging

from app.chatbot import ChatBot
from app.config import ExecutionContext, config


def prepare_chatbot() -> ChatBot:
    """
    Prepare the chatbot based on the execution context.

    :return: the chatbot prepared.
    """
    if config.EXECUTION_CONTEXT == ExecutionContext.LOCAL:
        logging.info("Loading with the LOCAL execution context.")
        return ChatBot(execution_context=ExecutionContext.LOCAL)
    elif config.EXECUTION_CONTEXT == ExecutionContext.DATABRICKS:
        logging.info("Loading with the DATABRICKS execution context.")
    return ChatBot(execution_context=ExecutionContext.DATABRICKS)


chat_bot: ChatBot = prepare_chatbot()
