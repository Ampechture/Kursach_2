import pandas as pd
import bibtexparser
import matplotlib.pyplot as plt
import time
from collections import Counter
from itertools import combinations
import seaborn as sns
import networkx as nx
from article_parse import citation_count
#from article_parse_async import citation_count_async
def loading_data():
    with open(r'D:\visual_Studio_Projects\Kursach_3\downloads\combined_bibtex.bib', 'r', encoding="utf-8") as combined_bibtex_file:
        bib_database = bibtexparser.load(combined_bibtex_file)
        df = pd.DataFrame(bib_database.entries)

    citation_list = []
    for i in range(len(df)):
        pii = df["url"][i].split('/')[-1]
        print(i)
        citation_list.append(citation_count(pii))
    df["citation_count"] = citation_list
    df.to_csv("example.csv", index=False, sep='\t')
    print(df['citation_count'])



def most_common_keywords():
    sns.set(style="whitegrid")
    #разделяем ключевые слова и очищаем от пробелов
    keywords = [word.strip().lower() for sublist in df['keywords'].dropna().str.split(', ').tolist() for word in sublist]
    keywords_counter = Counter(keywords)
    most_common_keywords = keywords_counter.most_common(10)
    keywords, counts = zip(*most_common_keywords)

    # Создаем график
    plt.figure(figsize=(12, 6))
    bars = plt.bar(keywords, counts, color=sns.color_palette("coolwarm", len(keywords)))

    # Добавим подписи для столбцов
    plt.xlabel('Ключевые слова', fontsize=14)
    plt.ylabel('Количество', fontsize=14)
    plt.title('10 наиболее часто встречающихся ключевых слов', fontsize=16)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    # Добавим значения над столбцами
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + .5, yval, ha='center', va='bottom', fontsize=10)

    plt.tight_layout()

    # Сохраняем график в файл
    plt.savefig('most_common_keywords.png', dpi=300)
    plt.show()

def most_common_keywords_years():
    sns.set(style="whitegrid")

    # Загружаем данные
    # Пример: da = pd.read_csv('data.csv')

    # Предполагаем, что keywords разделены запятыми
    # Разделяем строку с ключевыми словами и создаем отдельные строки для каждого
    df_expanded = df.drop('keywords', axis=1).join(df['keywords'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('keyword'))

    # Удаляем пробелы в начале и конце ключевых слов
    df_expanded['keyword'] = df_expanded['keyword'].str.strip()
    # Приведение к нижнему регистру
    df_expanded['keyword'] = df_expanded['keyword'].str.lower()
    # Группируем по годам и ключевым словам, считаем количество
    keywords_by_year = df_expanded.groupby(['year', 'keyword']).size().reset_index(name='counts')

    # Находим 10 самых часто встречающихся ключевых слов
    top_keywords = keywords_by_year.groupby('keyword').sum().nlargest(10, 'counts').reset_index()

    # Фильтруем данные, чтобы оставить только топовые ключевые слова
    filtered_keywords_by_year = keywords_by_year[keywords_by_year['keyword'].isin(top_keywords['keyword'])]

    # Построение графика
    plt.figure(figsize=(12, 8))
    for key in filtered_keywords_by_year['keyword'].unique():
        plt.plot(filtered_keywords_by_year[filtered_keywords_by_year['keyword'] == key]['year'],
                filtered_keywords_by_year[filtered_keywords_by_year['keyword'] == key]['counts'],
                marker='o', label=key)

    plt.xlabel('Год', fontsize=14)
    plt.ylabel('Количество', fontsize=14)
    plt.title('10 самых часто встречающихся ключевых слов по годам', fontsize=16)
    plt.xticks(rotation=45)
    plt.legend(title='Ключевые слова')
    plt.tight_layout()
    plt.savefig('most_common_keywords_years.png', dpi=300)
    plt.show()

def most_valuable_author():
    df.dropna(subset=['author'], inplace=True)

    # Разделяем авторов в строках и создаем список всех авторов
    all_authors = df['author'].str.split(' and ').explode()


    author_counts = all_authors.value_counts().nlargest(10)


    sns.set_style('whitegrid')


    plt.figure(figsize=(12, 8))
    sns.barplot(x=author_counts.values, y=author_counts.index, palette='viridis')

    # Добавляем заголовки и метки
    plt.title('Авторы с наибольшим количеством работ', fontsize=16)
    plt.xlabel('Количество работ', fontsize=14)
    plt.ylabel('Автор', fontsize=14)


    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig('most_valuable_author.png', dpi=300)
    plt.show()

def graph_relationship():
        # Предполагаем, что df - это DataFrame Pandas с колонкой 'author', где авторы разделены ' and '
    df.dropna(subset=['author'], inplace=True)

    # Создаем список ребер, где каждая пара авторов, которые сотрудничали, создает ребро
    edges = []

    for authors in df['author'].str.split(' and '):
        edges.extend(combinations(authors, 2))


    most_common_pairs = Counter(edges).most_common(50)

    # Создаем граф на основе 100 самых частых пар
    G = nx.Graph()
    G.add_edges_from([pair for pair, count in most_common_pairs])

    # Вычисляем степень для каждого узла
    degrees = dict(G.degree())

    # Нормализуем степени для определения размера узла
    sizes = [degrees[node] * 200 for node in G.nodes()]

    # Выбираем цвет узла на основе его степени
    colors = [degrees[node] for node in G.nodes()]


    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, k=2)  # k регулирует расстояние между узлами
    nodes = nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color=colors, cmap=plt.cm.coolwarm)
    edges = nx.draw_networkx_edges(G, pos)
    labels = nx.draw_networkx_labels(G, pos, font_size=5, font_weight='bold')
    plt.colorbar(nodes, label='Количество связей')


    plt.title('Граф 50 самых часто взаимодействующих авторов')
    plt.axis('off')
    plt.savefig('most_relationships_graph.png', dpi=300)
    plt.show()
#most_common_keywords()
#most_common_keywords_years()
#most_valuable_author()
#graph_relationship()
def main():
    start_time = time.time()
    loading_data()
    end_time = time.time()
    runtime = end_time - start_time

    print(f"Функция выполнялась: {runtime} секунд(ы)")

dataframe = pd.read_csv(r"D:\visual_Studio_Projects\Kursach_3\example.csv",sep ='\t')
print(dataframe["citation_count"])
