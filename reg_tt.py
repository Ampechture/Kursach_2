import bibtexparser
import pandas as pd
import os
import bibtexparser

# Задайте путь к директории с файлами BibTeX
bibtex_dir = r'D:\visual_Studio_Projects\Kursach_3\downloads'

# Получите список всех файлов BibTeX в директории

bibtex_files = [f for f in os.listdir(bibtex_dir) if f.endswith('.bib')]

# Создайте пустой объект BibDatabase для хранения объединенных записей
combined_bib_db = bibtexparser.bibdatabase.BibDatabase()

# Проход по всем файлам BibTeX и добавление их содержимого в combined_bib_db
for bibtex_file in bibtex_files:
    file_path = os.path.join(bibtex_dir, bibtex_file)
    with open(file_path, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        combined_bib_db.entries.extend(bib_database.entries)

# Сохраните объединенную базу BibTeX в новый файл
path_t = os.getcwd()
with open(r'D:\visual_Studio_Projects\Kursach_3\downloads\combined_bibtex.bib', 'w', encoding="utf-8") as combined_bibtex_file:
    bibtexparser.dump(combined_bib_db, combined_bibtex_file)
df = pd.DataFrame(combined_bib_db.entries)
print(df["title"])
