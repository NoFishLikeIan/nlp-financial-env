import os
import json 

from math import log
from itertools import chain, islice

from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary

from PyPDF2.utils import PdfReadError

from utils import read_pdf, url_parse, plotting
from nlp import topic


REPORTS = "data/reports/" 
VERBOSE = False # TODO: move to env

def read_reports(reportpath):
    for filename in os.listdir(REPORTS):

        filepath = os.path.join(REPORTS, filename)
        report = read_pdf.path_to_sentences(filepath)

        yield report, filename

def saliency_index(lda: LdaModel, corpus, words: Dictionary):

    full_corpus = list(chain(*corpus))

    N = len(words)
    total = sum(words.cfs[i] for i in range(N))
    frequencies = [words.cfs[i] / total for i in range(N)]

    topics = lda.print_topics() 

    relative_likelihood = [0. for _ in range(N)]

    for topic_id, topic_prob in lda.get_document_topics(full_corpus, minimum_probability=0.):
        for term, cond_prob in lda.get_topic_terms(topic_id, topn = None):

            relative_likelihood[term] += cond_prob * log(cond_prob / topic_prob)


    saliencies = [f * l for f, l in zip(frequencies, relative_likelihood)]

    return { words[i]: s for i, s in enumerate(saliencies) }


if __name__ == '__main__':

    companies = {}

    for report, filename in read_reports(REPORTS):
        company = filename.replace(".pdf", "")
        print(f"Report {company}...")

        try:

            lda, corpus, words = topic.get_topics(report)

            saliencies = saliency_index(lda, corpus, words) 

            companies[company] = saliencies

        except:
            print("...failed to read pdf!")
            

    with open("data/saliency.json", "w") as outfile:

        json.dump(companies, outfile)