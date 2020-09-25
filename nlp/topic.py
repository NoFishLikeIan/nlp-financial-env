import gensim

from gensim.models.ldamodel import LdaModel

def get_topics(sentences, **kwargs):
    words = gensim.corpora.Dictionary(sentences)

    corpus = [words.doc2bow(doc) for doc in sentences]



    lda_model = LdaModel(corpus=corpus, id2word=words, alpha='auto', **kwargs)

    return lda_model, corpus, sentences
