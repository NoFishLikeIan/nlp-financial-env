import spacy

from utils import read_pdf
from nlp import topic

TEST_FILE = "data/About-us_Voting-Policy-Proprietary-Investments_en.pdf"

if __name__ == '__main__':

    text = read_pdf.path_to_sentences(TEST_FILE)

    
    topic.get_topics(text)


    