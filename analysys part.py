import pandas as pd
import bibtexparser
import matplotlib.pyplot as plt
import time
from collections import Counter
from itertools import combinations
from wordcloud import WordCloud
import seaborn as sns
import networkx as nx
import matplotlib.ticker as ticker
from article_parse import citation_count
import os

my_path = os.getcwd()
print(my_path)

class DataAnalysys():
    def __init__(self, query) -> None:
        self.query = query
        os.chdir("downloads")
    def loading_data(self, citation=False):
        current_dir = os.getcwd()
        print(current_dir)
        with open(current_dir + f'\\{self.query}\\combined {self.query}.bib', 'r', encoding="utf-8") as combined_bibtex_file:
            bib_database = bibtexparser.load(combined_bibtex_file)
            self.df = pd.DataFrame(bib_database.entries)
        if citation == True:
            citation_list = []
            for i in range(len(self.df)):
                pii = self.df["url"][i].split('/')[-1]
                print(i)
                citation_list.append(citation_count(pii))
            self.df["citation_count"] = citation_list
            #df.to_csv("example.csv", index=False, sep='\t')



    def most_common_keywords(self):
        file_to_save = 'most_common_keywords'
        df = self.df
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
        print(os.getcwd)
        os.chdir(f"{self.query}")
    
        os.chdir(f'analysys_images')
        plt.savefig( file_to_save, dpi=300)
        #plt.show()

    def most_common_keywords_years(self):
        df = self.df
        sns.set(style="whitegrid")
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
        #plt.show()

    def most_valuable_author(self):
        file_to_save = "most_valuable_author"
        df = self.df
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
        plt.savefig(file_to_save, dpi=300)
        #plt.show()

    def graph_relationship(self):
        file_to_save = "graph_relationship"
        df = self.df
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
        plt.savefig(file_to_save, dpi=300)
        plt.show()

    def wordcloud_wk(self):
        file_to_save = "wordcloud"
        df = self.df
        text = ' '.join(df['abstract'].dropna())

        # Создаем облако слов
        wordcloud = WordCloud(
            width=1920,
            height=1080,
            background_color='white',
            max_words=800,
            contour_width=4,
            contour_color='steelblue'
        )

        # Генерируем облако слов
        wordcloud.generate(text)

        # Отображаем облако слов
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(file_to_save, dpi=300)
        #plt.show()

    def most_cited_authors(self):
        file_to_save = "most_cited_authors"
        df = self.df
        df.dropna(subset=['author', 'citation_count'], inplace=True)

        # Преобразуем citation_count в числовой тип данных
        df['citation_count'] = pd.to_numeric(df['citation_count'], errors='coerce').fillna(0)

        # Разделяем авторов и дублируем значения citation_count для каждого автора
        authors_expanded = df['author'].str.split(' and ').explode()
        df_expanded = df.loc[df.index.repeat(df['author'].str.split(' and ').str.len())]
        df_expanded['author'] = authors_expanded

        # Группируем по авторам и рассчитываем суммарное и среднее количество цитирований
        author_citations = df_expanded.groupby('author')['citation_count'].agg(['sum', 'count', 'mean']).reset_index()
        author_citations.columns = ['author', 'total_citations', 'total_works', 'mean_citations']

        # Топ-10 авторов по суммарным цитированиям
        top_authors_by_citations = author_citations.nlargest(10, 'total_citations')

        sns.set_style('whitegrid')
        plt.figure(figsize=(12, 8))

        # График топ-10 авторов по суммарным цитированиям
        sns.barplot(x='total_citations', y='author', data=top_authors_by_citations, palette='viridis')
        plt.title('Топ-10 авторов по суммарным цитированиям', fontsize=16)
        plt.xlabel('Суммарное количество цитирований', fontsize=14)
        plt.ylabel('Автор', fontsize=14)
        plt.tight_layout()
        plt.savefig(file_to_save, dpi=300)
        plt.show()

        # График топ-10 авторов по среднему количеству цитирований на работу
        top_authors_by_mean_citations = author_citations.nlargest(10, 'mean_citations')
        plt.figure(figsize=(12, 8))
        sns.barplot(x='mean_citations', y='author', data=top_authors_by_mean_citations, palette='viridis')
        plt.title('Топ-10 авторов по среднему количеству цитирований на работу', fontsize=16)
        plt.xlabel('Среднее количество цитирований на работу', fontsize=14)
        plt.ylabel('Автор', fontsize=14)
        plt.tight_layout()
        plt.savefig('top_mean_citation.png', dpi=300)
        plt.show()

    def top_journals(self):
        file_to_save = "top_journals"
        df = self.df
        # График общего количества работ по годам
        plt.figure(figsize=(12, 6))
        df['year'].value_counts().sort_index().plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title('Общее количество работ по годам', fontsize=16)
        plt.xlabel('Год', fontsize=14)
        plt.ylabel('Количество работ', fontsize=14)
        plt.xticks(fontsize=12, rotation=45)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.savefig(file_to_save + '_1', dpi=300)
        plt.show()

        # Определение топ-10 журналов по количеству работ
        top_journals = df['journal'].value_counts().head(10)

        # Визуализация топ-10 журналов
        plt.figure(figsize=(12, 8))
        ax = top_journals.plot(kind='barh', color='lightgreen', edgecolor='black')
        plt.title('Топ-10 журналов по количеству работ', fontsize=16)
        plt.xlabel('Количество работ', fontsize=14)
        plt.ylabel('Журнал', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Force integer labels on x-axis
        plt.tight_layout()
        plt.savefig(file_to_save + '_2', dpi=300)
        plt.show()


    # Возвращение топ-10 журналов как DataFrame для дальнейшего использования
        return top_journals
#Костыльная загрузка


def main():
    start_time = time.time()
    test = DataAnalysys("smart grid")
    test.loading_data()
    test.most_common_keywords()
    test.most_common_keywords_years()
    test.most_valuable_author()
    test.graph_relationship()
    test.wordcloud_wk()
    test.top_journals()
    #most_cited_authors_long_term
    #test.most_cited_authors()
    end_time = time.time()
    runtime = end_time - start_time
    
    print(f"Функция выполнялась: {runtime} секунд(ы)")

main()
