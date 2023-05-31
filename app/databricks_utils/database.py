from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.config import DATABRICKS_TEXT_TO_SQL_MODEL


class TextToSQL:
    """
    Text to SQL model for translating English text to SQL requests.
    """

    def __init__(self) -> None:
        self.model_name = DATABRICKS_TEXT_TO_SQL_MODEL
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def get_sql(self, query) -> str:
        """
        Translate English text to SQL.
        :param query: to translate
        :return: the SQL query
        """
        input_text = """Translate English to SQL: %s </s>""" % query
        features = self.tokenizer([input_text], return_tensors="pt")

        output = self.model.generate(
            input_ids=features["input_ids"],
            attention_mask=features["attention_mask"],
        )

        return self.tokenizer.decode(output[0], skip_special_tokens=True)
