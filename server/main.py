from langchain.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from flask import Flask, request, jsonify
from flask_cors import CORS

os.environ["OPENAI_API_KEY"] = "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"
api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)
CORS(app)

CHROMA_DB_DIRECTORY = "chroma_db/docs"


def handle_exception(e):
    return jsonify({"status": "fail", "message": str(e)}, 500)


def get_database():
    try:
        embeddings = OpenAIEmbeddings()
        db = Chroma(
            collection_name="Docs",
            embedding_function=embeddings,
            persist_directory=CHROMA_DB_DIRECTORY,
        )
        return db
    except Exception as e:
        print(e)


def traverse_folder(folder_path, file_list):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                file_list.append(file_path)

        for dir in dirs:
            new_folder_path = os.path.join(root, dir)
            traverse_folder(new_folder_path, file_list)


def build_database_md():
    try:
        folder_path = "./docs/md/"

        loaders = []

        traverse_folder(folder_path, loaders)
        loaders = [UnstructuredMarkdownLoader(file_path) for file_path in loaders]
        loader = DirectoryLoader(
            folder_path, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader
        )
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splitted_documents = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()

        print("ingesting data...")
        db = Chroma.from_documents(
            splitted_documents,
            embeddings,
            collection_name="Docs",
            persist_directory=CHROMA_DB_DIRECTORY,
        )
        db.persist()
        db = None
        print("Ingested")
    except Exception as e:
        print(e)


def build_database():
    try:
        folder_path = "./docs/"
        loader = DirectoryLoader(folder_path, glob="./*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splitted_documents = text_splitter.split_documents(documents)
        print(documents[0])
        embeddings = OpenAIEmbeddings()

        print("ingesting data...")
        db = Chroma.from_documents(
            splitted_documents,
            embeddings,
            collection_name="Docs",
            persist_directory=CHROMA_DB_DIRECTORY,
        )
        db.persist()
        db = None
        print("Ingested")
    except Exception as e:
        print(e)


def delete_database():
    try:
        db = get_database()
        db.delete_collection()
        db.persist()
    except Exception as e:
        print(e)


def answer_query(query):
    embeddings = OpenAIEmbeddings()
    db = Chroma(
        collection_name="Docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_DIRECTORY,
    )

    chat = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    chain = RetrievalQA.from_chain_type(
        llm=chat,
        chain_type="stuff",
        retriever=db.as_retriever(),
        return_source_documents=True,
    )

    llm_response = chain(query)
    result = {
        "result": llm_response["result"],
        "sources": [
            source.metadata["source"] for source in llm_response["source_documents"]
        ],
    }
    return result


@app.route("/api/build_database", methods=["GET"])
def route_build_database():
    try:
        build_database_md()
        return jsonify({"status": "success"})
    except Exception as e:
        return handle_exception(e)


@app.route("/api/delete_database", methods=["GET"])
def route_delete_database():
    try:
        delete_database()
        return jsonify({"status": "success"})
    except Exception as e:
        return handle_exception(e)


@app.route("/api/answer_query", methods=["POST"])
def route_answer_query():
    try:
        query = request.json["query"]
        response = answer_query(query)
        return jsonify(response)
    except Exception as e:
        return handle_exception(e)


if __name__ == "__main__":
    app.run(debug=True)
