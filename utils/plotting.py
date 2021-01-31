import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer

def plot_bigrams(sentences, ax, n = 10):
    bigram_tf_idf_vectorizer = TfidfVectorizer(ngram_range=(2,2), use_idf=True)
    bigram_tf_idf = bigram_tf_idf_vectorizer.fit_transform([" ".join(sent) for sent in sentences])
    
    words = bigram_tf_idf_vectorizer.get_feature_names()
    
    total_counts = np.zeros(len(words))
    for t in bigram_tf_idf:
        total_counts += t.toarray()[0]
        
    count_dict = (zip(words, total_counts))
    count_dict = sorted(count_dict, key=lambda x:x[1], reverse=True)[:n]
    words = [w[0] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words)) 
        
    sns.barplot(x_pos, counts, palette="Blues_r", ax = ax)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(words, rotation = 10)
    
    ax.set_xlabel("Bi-grams")
