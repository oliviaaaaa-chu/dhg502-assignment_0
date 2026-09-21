import io

from qhchina import load_stopwords
from qhchina.analytics import LDAGibbsSampler

with io.open("史記.txt", encoding="utf-8") as f:
    text = f.read()

stopwords = set(load_stopwords("zh_cl_tr"))
stopwords.update("　 \t\r\n")

# segment into 1000-character documents, removing stopwords/whitespace at char level
chars = [c for c in text if c not in stopwords]
documents = [chars[i:i + 1000] for i in range(0, len(chars) - 999, 1000)]
print(f"{len(documents)} segments")

lda = LDAGibbsSampler(n_topics=15, iterations=100, random_state=42,
                      min_word_count=2, stopwords=stopwords)
lda.fit(documents)

with io.open("史記_topics.txt", "w", encoding="utf-8") as f:
    f.write("Character-level LDA topic model\n")
    f.write("Corpus: 史記.txt (Records of the Grand Historian)\n")
    f.write(f"Segments: {len(documents)} documents of 1000 characters each\n")
    f.write("Topics: 15, Iterations: 100, random_state=42\n")
    f.write("Stopwords: qhchina zh_cl_tr (classical Chinese, traditional)\n\n")
    for t, words in enumerate(lda.get_topics(n_words=20)):
        f.write(f"Topic {t}:\n")
        for w, p in words:
            f.write(f"  {w}\t{p:.5f}\n")
        doc_probs = sorted(
            ((d, lda.get_document_topics(doc_id=d)[t][1]) for d in range(len(documents))),
            key=lambda x: x[1], reverse=True)
        f.write("  Top documents:\n")
        for doc_id, prob in doc_probs[:3]:
            f.write(f"    segment {doc_id}\t{prob:.5f}\n")
        f.write("\n")
print("done")
