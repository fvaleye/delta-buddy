import glob
import logging
import os
from multiprocessing import Pool
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    NotebookLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from tqdm import tqdm

from app.config import CHROMA_SETTINGS, config

chunk_size = 500
chunk_overlap = 0

# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".mdx": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    ".ipynb": (NotebookLoader, {})
    # Add more mappings for other file extensions and loaders as needed
}


def load_single_document(file_path: str) -> List[Document]:
    extension = f'.{file_path.rsplit(".", 1)[-1]}'
    if extension in LOADER_MAPPING and file_path:
        loader_class, loader_args = LOADER_MAPPING[extension]
        loader = loader_class(file_path, **loader_args)
        return loader.load()

    raise ValueError(f"Unsupported file extension for the document['{file_path}]'")


def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files
    """
    all_files = []
    for extension in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{extension}"), recursive=True)
        )
    filtered_files = [
        file_path for file_path in all_files if file_path not in ignored_files
    ]

    results = list()
    with Pool(processes=os.cpu_count()) as pool:
        with tqdm(
            total=len(filtered_files), desc="Loading new documents", ncols=80
        ) as pbar:
            for i, docs in enumerate(
                pool.imap_unordered(load_single_document, filtered_files)
            ):
                results.extend(docs)
                pbar.update()
        return results


async def process_documents(
    source_directory: str, ignored_files: List[str] = []
) -> List[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files.
    Splits the documents into chunks of text and returns a list of all chunks.

    :param source_directory:
    :param ignored_files:
    :return:
    """
    logging.info(f"Loading documents from {source_directory}")
    documents = load_documents(source_directory, ignored_files)
    if not documents:
        logging.info("No new documents to load")
        return list()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    logging.info(f"Loaded {len(documents)} new documents from {source_directory}")
    texts = text_splitter.split_documents(documents)
    logging.info(
        f"Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)"
    )
    return texts


def does_vectorstore_exist(persist_directory: str) -> bool:
    if os.path.exists(os.path.join(persist_directory, "index")):
        if os.path.exists(
            os.path.join(persist_directory, "chroma-collections.parquet")
        ) and os.path.exists(
            os.path.join(persist_directory, "chroma-embeddings.parquet")
        ):
            list_index_files = glob.glob(os.path.join(persist_directory, "index/*.bin"))
            list_index_files += glob.glob(
                os.path.join(persist_directory, "index/*.pkl")
            )
            # At least 3 documents are needed in a working vectorstore
            if len(list_index_files) > 3:
                return True
    return False


async def ingest_documents_in_database(
    persist_directory: str, model_name: str
) -> List[Document]:
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    if does_vectorstore_exist(persist_directory=persist_directory):
        logging.info(f"Appending to existing vectorstore at {persist_directory}")
        db = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            client_settings=CHROMA_SETTINGS,
        )
        collection = db.get()
        texts = await process_documents(
            source_directory=config.SOURCE_DOCUMENTS_DIRECTORY,
            ignored_files=[metadata["source"] for metadata in collection["metadatas"]],
        )
        logging.info("Creating embeddings. May take some minutes...")
        if texts:
            db.add_documents(texts)
    else:
        # Create and store locally vectorstore
        logging.info("Creating new vectorstore")
        texts = await process_documents(source_directory=config.SOURCE_DOCUMENTS_DIRECTORY)
        logging.info("Creating embeddings. May take some minutes...")
        db = Chroma.from_documents(
            texts,
            embeddings,
            persist_directory=persist_directory,
            client_settings=CHROMA_SETTINGS,
        )
        # Force flush
        db.similarity_search("dummy")
    db.persist()
    db = None

    logging.info("Ingestion complete!")
