from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cosine_similarity(sentence_1, sentence_2):
    sentence = (sentence_1, sentence_2)
    
    # Tfidf Vectorizer 객체 생성
    vectorizer = TfidfVectorizer()

    # 문장의 벡터화
    matrix = vectorizer.fit_transform(sentence)

    # Cosine Similarity 도출
    cosine_similarity_value = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

    return cosine_similarity_value