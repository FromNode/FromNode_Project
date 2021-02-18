# Pororo 미설치 가상환경인 경우, pip install pororo
from pororo import Pororo


def summary(target_text, language="ko"):
    if type(target_text) != str:
        raise Exception("can only summary str type as arguments")
    summ = Pororo(task="summarization", model="abstractive", lang=language)
    return summ(target_text)
