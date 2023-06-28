# Delta-Buddy 
<!-- Add logo.png -->

![Delta-Buddy](logo.png?raw=true)

[![licence](https://img.shields.io/badge/license-Apache--2.0-green)](https://github.com/fvaleye/delta-buddy/blob/main/LICENSE.txt)

Introducing Delta-Buddy: Your ultimate Delta Lake companion! 🐍
Streamline your data journey with an AI-powered chatbot. Ask Delta-Buddy anything about your Delta Lake.

## Demo
https://github.com/fvaleye/delta-buddy/assets/19929573/20e5b9c7-4cd5-4de5-a804-27feb3297188

## ⚡️Features
- A chatbot to ask questions to [Dolly](https://github.com/databrickslabs/dolly) based on your documents and datasets.
- Ingest documents in a [Chroma](https://github.com/chroma-core/chroma) database locally or from a Databricks notebook.
- Provide a web UI based on [Chainlit](https://github.com/Chainlit/chainlit) to ask questions and receive answers.
- Provide a API based on [FastAPI](https://fastapi.tiangolo.com/) to receive and questions from everywhere.
- Run locally or on Databricks while keeping your data safe.

## 📚 Documentation
The documentation for Delta-Buddy is in construction.

## 📦 Installation

### Locally

- Configure the `env.sample` file in the root and and rename it to `.env` with your configuration (use `local` for the execution context).
- Install the virtual environment and the dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- You could also install the development dependencies if you want to contribute to Delta-Buddy
```bash
pip install -r requirements-dev.txt
```

- Run the following example data_preparation.prepare_delta_buddy.py to start the data preparation using the following command:

```bash
make prepare-data
```

- Delta-Buddy is ready, launch the UI with the following command:
```bash
make launch-ui
```
- When everything is running well, you are ready to use the UI to ask questions to Delta-Buddy. 

***Disclaimer**: for the first run, it could take some time to download the LLM model.*

### On Databricks

- Add the delta-buddy repo to Databricks (under Repos click Add Repo, enter https://github.com/fvaleye/delta-buddy.git, then click Create Repo). More information [here](https://docs.databricks.com/repos/index.html).
Start a 13.0 LTS ML (includes Apache Spark 3.4.0, GPU, Scala 2.12) single-node cluster with node type having 8 A100 GPUs (e.g. Standard_ND96asr_v4 or p4d.24xlarge). Note that these instance types may not be available in all regions, or may be difficult to provision. In Databricks, note that you must select the GPU runtime first, and unselect "Use Photon", for these instance types to appear (where supported).  
- Configure the `env.sample` file in the root and rename it to `.env` with your configuration and use `databricks` for the execution context for your databricks configuration.
- Configure the `env.sample` file in the `notebooks` folder and rename it to `.env` for your notebook configuration.
- Open the notebooks folder inside the Repo (which are `delta_buddy_preparation.py` first and then `delta_buddy_run.py`), attach to your GPU cluster, and run all cell.
- Open the notebooks folder and launch the notebook `delta_buddy_preparation.py` to prepare the Chroma database on your Databricks cluster.
- Open the notebooks folder and launch the notebook `delta_buddy_run.py` to test the chatbot on your Databricks cluster.
- You have different serving mode for `delta_buddy_run.py`: local, by notebook api or llm connection (see the environment variables to choose the best serving mode). 
- When everything is running well, you are ready to ask questions to Delta-Buddy.

- Launch the UI connected to Databricks depending on the serving mode with the following command:

```bash
make launch-ui
```

***Disclaimer**: for the first run, it could take some time to download the LLM model.*

## 🔎 Usage

In construction. 

## 🔒Privacy & Security

Delta-Buddy is designed to run locally or on Databricks with Dolly to not share your data with anyone.

## ⚙️ Environment Variables

The environment variables can be set from an environment file `.env`.

| **Parameter**                    | **Description**                                                                                                                      |
|----------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------|
| **EXECUTION_CONTEXT**            | The execution context for running Delta-Buddy: local or databricks (look the DATABRICKS_SERVING_MODE to specify the serving access). |
| **PREPARATION_MODEL_NAME**       | The model used for preparation and execution for the sentence transformer.                                                           |
| **EMBEDDINGS_MODEL_NAME**        | The model used for preparation and execution for the sentence transformer.                                                           |
| **SOURCE_DOCUMENTS_DIRECTORY**   | The directory to store on disk the documents to be ingested in the Chromadb database.                                                |
| **PERSIST_DIRECTORY**            | The directory to persist the Chromadb database.                                                                                      |
| **SOURCE_DOCUMENTS_MAX_COUNT**   | The number of sources to use when prompting the question to Dolly.                                                                   |
| **DATABRICKS_MODEL_NAME**        | The name of the Databricks Dolly model.                                                                                              |
| **DATABRICKS_CLUSTER_ID**        | The identifier of the Databricks cluster to use for llm or notebook run.                                                             |
| **DATABRICKS_NOTEBOOK_PATH**     | The path of `delta_buddy_run.py` notebook in the dbfs of Databricks.                                                                 |
| **DATABRICKS_SERVER_HOSTNAME**   | The server hostname to use to access your Databricks account.                                                                        |
| **DATABRICKS_TEXT_TO_SQL_MODEL** | The model to use for Text to SQL translations.                                                                                       |
| **DATABRICKS_HTTP_PATH**         | The HTTp path of the Databricks Warehouse to use for fetching metadata.                                                              |
| **DATABRICKS_TOKEN**             | The Token of your Databricks account to access clusters or metadata.                                                                 |
| **DATABRICKS_LLM_PORT**          | The port to use for accessing the model's API on the `delta_buddy_run.py` notebook.                                                  |
| **DATABRICKS_SERVING_MODE**      | The serving mode for accessing the model: `local`, `notebook_hosted_api`, `notebook_api`.                                            |

## 🛡️ License

Delta-Buddy is licensed under the Apache License 2.0. See the LICENSE file for more details.

## ✨Contributing

Contributions are welcome! Please check out the todos below, and feel free to open a pull request.
For more information, please see the [contributing guidelines](CONTRIBUTING.md).

After installing the virtual environment, please remember to install `pre-commit` to be compliant with our standards:

### 🗺️ Todo

- [ ] Ask questions on Delta Lake tables with Text to SQL capabilities.
- [ ] Add a chat history
- [ ] Improve the CI and the tests
- [ ] Integrate MLFlow for serving the model
- [ ] Improve the FastAPI features and documentation

## Disclaimer
This is a early-stage project to validate the feasibility of a fully private solution for question answering 
using Dolly and Vector embeddings. It's not production ready yet.