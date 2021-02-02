import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from PyPDF2.utils import PdfReadError

from utils import read_pdf, url_parse, plotting
from nlp import topic


if __name__ == '__main__':

    with open("data/urls-st.txt", "r") as file:
        urls = file.read().split("\n")

    urls = {
        url_parse.get_name(u): u for u in urls 
        if read_pdf.is_url(u)
    }

    sentences = {}

    for company, url in urls.items():
        try: 
            s = read_pdf.path_to_sentences(url)
            sentences[company] = s
            
        except PdfReadError:
            print(f"PdfReadError at {company}")

    company = "apg"

    fig, ax = plt.subplots(figsize=(20, 12))

    plotting.plot_bigrams(sentences[company], ax = ax)

    fig.savefig(f"plots/{company}_bigram.png")

    lda, corpus, words = topic.get_topics(sentences[company])
