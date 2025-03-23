"""Runs backend server for report generation

The requests this server handles are in https://github.com/flyxiv/llm_report_generator/blob/main/doc/api.md
Receives target company and period for generating report, and uses RAG tools to make the LLM generate correct response.
"""
import yaml 
import logging
import os 

from flask import flask
from datetime import datetime
from ..data_retrieval import load_database

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = './config.yml'

try:
    with open(CONFIG_FILE_PATH, 'r') as f:
        CONFIGS = yaml.safe_load(f) 
except FileNotFoundError:
    raise FileNotFoundError("Cannot find file {CONFIG_FILE_PATH}")
    
@app.route("/api/v1/analysis_report")
def generate_analysis_report(company_id: int, start_year_month: str, end_year_month: str):
    start_datetime = datetime.strptime(start_year_month, '%Y%m')
    end_datetime = datetime.strptime(end_year_month, '%Y%m')
        
if __name__ == "__main__":
    os.makedirs(CONFIGS['persist_directory'], exist_ok=True)
    load_database(**CONFIGS)
    