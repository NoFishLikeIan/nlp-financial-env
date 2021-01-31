import spacy

from PyPDF2.utils import PdfReadError

from utils import read_pdf, parser_model, url
from nlp import topic

URLS = "data/urls-st.txt"

if __name__ == '__main__':

    with open(URLS, "r") as file:
        urls = file.read().split("\n")

    names = [url.get_name(u) for u in urls]

    urls = dict(zip(names, urls))

    text = []

    for entry, url in urls.items():
        try:
            sentences = read_pdf.path_to_sentences(url)
            text.append(sentences)
        except PdfReadError:
            text.append([])
    