import PyPDF2
import string

import re

from .parser_model import nlp

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

def path_to_sentences(filepath: str) -> str:

    text = ""

    with open(filepath, "rb") as file:
        pdf = PyPDF2.PdfFileReader(file)

        n_pages = pdf.getNumPages()

        for i in range(n_pages):
            page = pdf.getPage(i)

            page_text = page.extractText()

            text += f"{page_text}\n"

    return extract_statements(text)