import PyPDF2
import string
import requests
import re
import io
import os

from .parser_model import nlp


def is_url(to_validate):

    url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(url_regex, to_validate) is not None

def extract_statements(text):

  lines = []
  prev = ""
  for line in text.split('\n'):

    if line.startswith(' ') or not prev.endswith('.'):
        prev = prev + ' ' + line
    else:
        lines.append(prev)
        prev = line
        
  lines.append(prev)

  sentences = []
  for line in lines:
    
      line = re.sub(r'^\s?\d+(.*)$', r'\1', line)
      line = line.strip()
      line = re.sub('\s?-\s?', '-', line)
      line = re.sub(r'\s?([,:;\.])', r'\1', line)
      line = re.sub(r'\d{5,}', r' ', line)
      line = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', r' ', line)
      line = re.sub('\s+', ' ', line)


      sentences.append(nlp(line))

  return sentences


def pdf_to_text(pdf):
    text = ""
    n_pages = pdf.getNumPages()

    for i in range(n_pages):
        page = pdf.getPage(i)

        page_text = page.extractText()

        text += f"{page_text}\n"

    return text


def path_to_sentences(filepath: str) -> str:

    text = ""

    if os.path.isfile(filepath):
        with open(filepath, "rb") as file:
            pdf = PyPDF2.PdfFileReader(file)
            text = pdf_to_text(pdf)

    else:
        response = requests.get(filepath)

        with io.BytesIO(response.content) as file:
            pdf = PyPDF2.PdfFileReader(file)
            text = pdf_to_text(pdf)

    return extract_statements(text)