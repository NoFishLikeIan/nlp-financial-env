import os
import json
from dotenv import load_dotenv, find_dotenv

from utils import read_pdf


def read_reports(reportpath):
    for filename in os.listdir(reportpath):
        try:
            filepath = os.path.join(reportpath, filename)
            report = read_pdf.path_to_sentences(filepath)

            yield report, filename

        except PdfReadError as err:
            print(f"{filename}: {err}")
            return [], filename

def read_sentences(sentencepath):
    for filename in os.listdir(sentencepath):
        filepath = os.path.join(sentencepath, filename)

        with open(filepath) as f:
            sentences = json.load(f)

        yield sentences["sentences"], filename

if __name__ == '__main__':

    load_dotenv(find_dotenv())
    REPORTS = os.environ.get("REPORTS")

    if not REPORTS:
        raise ValueError("Could not find REPORTS path. Make sure you create a .env with REPORTS")
    
    for report, filename in read_reports(REPORTS):
        
        company = filename.replace(".pdf", "")

        with open(f"data/outreports/{company}.json", "w") as f:
            json.dump({"sentences": report}, f)