# -*- coding: utf-8 -*-
"""
analyze.py
Проект №8 — N-граммы
Загрузка текста, предобработка (токенизация + стоп-слова),
подсчёт частот униграмм/биграмм/триграмм, визуализация топ-20.
"""

import re
import os
import matplotlib.pyplot as plt
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Скачиваем стоп-слова (один раз)
nltk.download("stopwords", quiet=True)

# Настройка русского шрифта
plt.rcParams['font.family'] = 'DejaVu Sans'

# Русские стоп-слова
RUSSIAN_STOPWORDS = set(stopwords.words("russian"))
# Добавляем свои
EXTRA_STOPWORDS = {"это", "все", "так", "вот", "даже", "уже", "еще", "очень", "быть", "сказать"}
STOPWORDS = RUSSIAN_STOPWORDS | EXTRA_STOPWORDS


def load_text(filepath):
    """Загружает текст из файла"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def preprocess(text):
    """
    Предобработка текста:
    1. Нижний регистр + замена ё на е
    2. Удаление пунктуации и цифр
    3. Токенизация
    4. Удаление стоп-слов и коротких слов (менее 2 букв)
    """
    text = text.lower()
    text = text.replace('ё', 'е')
    text = re.sub(r'[^а-яa-z\s]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return words


def get_ngrams(tokens, n):
    """Создаёт n-граммы из списка токенов"""
    if len(tokens) < n:
        return []
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [' '.join(ngram) for ngram in ngrams]


def plot_top20(counter, title, filename, top_n=20):
    """Строит горизонтальный bar chart топ-N n-грамм"""
    top_items = counter.most_common(top_n)
    if not top_items:
        print(f"  Предупреждение: нет данных для {title}")
        return
    
    items = [item[0] for item in top_items[::-1]]
    counts = [item[1] for item in top_items[::-1]]
    
    plt.figure(figsize=(12, 8))
    plt.barh(items, counts, color='steelblue')
    plt.xlabel('Частота', fontsize=12)
    plt.title(title, fontsize=14)
    plt.tight_layout()
    
    os.makedirs('../images', exist_ok=True)
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"  График сохранён: {filename}")


def analyze_author(filepath, author_name):
    """Полный анализ одного автора"""
    print(f"\n{'='*50}")
    print(f"📖 АНАЛИЗ: {author_name}")
    print(f"{'='*50}")
    
    text = load_text(filepath)
    print(f"  Исходный объём: {len(text)} символов")
    
    tokens = preprocess(text)
    print(f"  Слов после обработки: {len(tokens)}")
    print(f"  Уникальных слов: {len(set(tokens))}")
    
    unigrams = Counter(tokens)
    bigrams = Counter(get_ngrams(tokens, 2))
    trigrams = Counter(get_ngrams(tokens, 3))
    
    print(f"\n  Топ-10 слов:")
    for i, (word, count) in enumerate(unigrams.most_common(10), 1):
        print(f"    {i}. '{word}' — {count} раз")
    
    print(f"\n  Топ-10 биграмм:")
    for i, (bg, count) in enumerate(bigrams.most_common(10), 1):
        print(f"    {i}. '{bg}' — {count} раз")
    
    print(f"\n  Топ-10 триграмм:")
    for i, (tg, count) in enumerate(trigrams.most_common(10), 1):
        print(f"    {i}. '{tg}' — {count} раз")
    
    plot_top20(unigrams, f'{author_name}: Топ-20 слов', f'../images/{author_name}_unigrams.png')
    plot_top20(bigrams, f'{author_name}: Топ-20 биграмм', f'../images/{author_name}_bigrams.png')
    plot_top20(trigrams, f'{author_name}: Топ-20 триграмм', f'../images/{author_name}_trigrams.png')
    
    return {
        'name': author_name,
        'tokens': len(tokens),
        'unigrams': unigrams,
        'bigrams': bigrams,
        'trigrams': trigrams
    }


def main():
    print("="*60)
    print("ПРОЕКТ №8 — N-ГРАММЫ")
    print("Достоевский vs Чехов vs Гончаров")
    print("="*60)
    
    authors = [
        ('../texts/dostoevsky.txt', 'Достоевский'),
        ('../texts/chekhov.txt', 'Чехов'),
        ('../texts/goncharov.txt', 'Гончаров')
    ]
    
    for filepath, name in authors:
        analyze_author(filepath, name)
    
    print("\n" + "="*60)
    print("✅ Анализ завершён. Графики в папке 'images/'")
    print("="*60)


if __name__ == '__main__':
    main()