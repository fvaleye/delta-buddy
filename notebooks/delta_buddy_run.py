# Databricks notebook source
# MAGIC %md
# MAGIC #Databricks run notebook

# COMMAND ----------

# MAGIC %pip install -r ../requirements.txt
# MAGIC dbutils.library.restartPython()
# MAGIC print("Python dependencies are installed ✅")

# COMMAND ----------

dbutils.widgets.text(
    "question",
    "What is Delta Lake?",
)
dbutils.widgets.dropdown(
    "serving_mode",
    "notebook_hosted_api",
    ["local", "notebook_hosted_api", "notebook_api"],
    "How to serve the ChatBot",
)

# COMMAND ----------

from app.databricks_utils.manager import DatabricksManager
from app.main import app
from app.state import chat_bot

if dbutils.widgets.get("serving_mode") == "notebook_hosted_api":
    await DatabricksManager.launch_llm_fast_api_from_notebook(app=app)
else:
    question = dbutils.widgets.get("question")
    answer = chat_bot.chat(
        question,
        from_databricks_notebook=dbutils.widgets.get("serving_mode") == "local",
    )
    displayHTML(answer.answer)

# COMMAND ----------

dbutils.library.restartPython()
dbutils.notebook.exit(answer.answer.capitalize())
