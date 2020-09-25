import spacy

PACKAGE_NAME = "en_core_web_sm"

if not spacy.util.is_package(PACKAGE_NAME):
    spacy.cli.download(PACKAGE_NAME)

nlp = spacy.load(PACKAGE_NAME)

remove = set(['PUNCT', 'NUM', 'SYM', '-PRON-'])

def lemmatizer(doc):

    doc = [token.lemma_ for token in doc if token.lemma_ != '-PRON-']

    doc = u' '.join(doc)

    return nlp.make_doc(doc)
    
def remove_stopwords(doc):

    parsed_doc = []

    for token in doc:
        if token.is_stop or token.is_punct or token.like_num:
            continue

        parsed_doc.append(token.text)
        

    return parsed_doc

nlp.add_pipe(lemmatizer, name='lemmatizer', after="ner")

nlp.add_pipe(remove_stopwords, name="stopwords", last=True)