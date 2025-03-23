"""Loads needed documents and images at the start of the backend server.

1) Loads sales CSV file, parses it into meaningful text, and divides it into chunks.
2) Loads sales dashboard example.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

from logging import Logger 

import pandas as pd
import base64

def _convert_dataframe_to_document_chunks(sales_data: pd.DataFrame, chunk_size=1000, chunk_overlap=100):
    """Converts CSV data to readable text chunks
    
    Args:
        sales_data: Pandas DataFrame with following columns
            * InvoiceNo: Invoice ID, similar to transaction ID
            * StockCode: Stock ID
            * Description: Name of the product
            * Quantity: Number of product bought in the transaction
            * InvoiceDate: Date of the transaction
            * UnitPrice: Price for each unit of product

        chunk_size: maximum size of language chunks.
        chunk_overlap: number of chunks that can be stored together in consecutive chunks.
    """
    documents = []
    
    for row in sales_data.itertuples():
       content = f"Invoice: {row.InvoiceNo}\n" 
       content += f"StockCode: {row.StockCode}\n"
       content += f"Product Name: {row.Description}\n"
       content += f"Quantity: {row.Quantity}\n"
       content += f"Date: {row.InvoiceDate}\n"
       content += f"UnitPrice: {row.UnitPrice}"
       
       documents.append(content)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    chunks = text_splitter.create_documents(documents)

    return chunks


def store_chunks_to_vector_store(chunks, persist_directory="./chroma_db"):
    embeddings = OpenAIEmbeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    return vector_store

def add_sample_report_image(report_example_img_path: str):
    """Create sample report image document
    """

    try:
        with open(report_example_img_path, 'rb') as f:
            img_in_bytes = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("Cannot find find {report_example_img_path}")
        
    img_b64 = base64.b64encode(img_in_bytes).decode()

    doc = Document(
        page_content="Sales Report Example for Company A",
        metadata={
            "company": "A",
            "report_name": "Sales Report",
            "image_data": img_b64
        }
    )

    return [doc]


    
def load_database(sales_dataset: str, report_example_img_path: str, persist_directory: str):
    sales_data = pd.read_csv(sales_dataset)

    chunks = _convert_dataframe_to_document_chunks(sales_data)
    chunks.extend(add_sample_report_image(report_example_img_path))
    vector_store = store_chunks_to_vector_store(chunks)

   
