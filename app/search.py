from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Загружаем только нужные пакеты
nltk.download('punkt')
nltk.download('stopwords')

# Индексируем документы (предположим, что это текст с сайтов)
def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join(p.get_text() for p in paragraphs)
    return text

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zа-я0-9]', ' ', text)  # Убираем все символы, кроме букв и цифр
    tokens = word_tokenize(text)  # Применяем токенизацию
    stop_words = set(stopwords.words('russian')) | set(stopwords.words('english'))  # Стоп-слова
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]  # Отбираем токены
    return tokens

# Пример документов
urls = {
    "site1": "https://moodle.astanait.edu.kz/",
    "site2": "https://example.org/en"
}

docs = {}
for name, url in urls.items():
    raw = get_text_from_url(url)
    tokens = preprocess_text(raw)
    docs[name] = tokens

# Индексация
def build_index(documents):
    index = defaultdict(set)
    for doc_id, tokens in documents.items():
        for token in tokens:
            index[token].add(doc_id)
    return index

# Индексируем
index = build_index(docs)

# Функция поиска
def search_documents(query):
    tokens = preprocess_text(query)
    results = [index[token] for token in tokens if token in index]
    
    if not results:
        return []
    
    # Пересекаем результаты, чтобы найти общий список документов
    return list(set.intersection(*results)) if results else []
