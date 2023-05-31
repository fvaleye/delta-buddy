from typing import List, Optional

from pydantic import BaseModel


class Answer(BaseModel):
    """
    Answer of the LLM model.
    """

    question: str
    answer: str

    @classmethod
    def to_html(cls, question: str, answer: str) -> "Answer":
        """
        Convert the answer to html.

        :param question: the question
        :param answer: the answer
        :return: the answer in html format
        """
        answer_html = f'<p><blockquote style="font-size:24">{question.capitalize()}</blockquote></p>'
        answer_html += (
            f'<p><blockquote style="font-size:18px">{answer.capitalize()}</blockquote></p>'
        )
        answer_html += "<p><hr/></p>"
        return cls(question=question, answer=answer_html)


class LLMInput(BaseModel):
    """
    Input of the LLM model using langchain.
    """

    prompt: str
    stop: Optional[List[str]]
