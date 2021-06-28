from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cosine_similarity_compare(sentence_1, sentence_2):
    sentence = (sentence_1, sentence_2)
    
    # Tfidf Vectorizer 객체 생성
    vectorizer = TfidfVectorizer()

    # 문장 벡터화 진행
    matrix = vectorizer.fit_transform(sentence)

    # 각 단어
    text = vectorizer.get_feature_names()

    # 각 단어의 벡터 값
    idf = vectorizer.idf_

    cosine_similarity_value = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    cosine_similarity_value = float(cosine_similarity_value)

    return cosine_similarity_value