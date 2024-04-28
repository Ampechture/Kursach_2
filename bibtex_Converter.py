from pybtex.database import parse_file
import os

os.chdir("downloads")
print(os.getcwd())
bib_data = parse_file("ScienceDirect_citations_1713843254831.bib")
for entry in bib_data.entries:
    print(bib_data.entries[entry])
    title = bib_data.entries[entry].fields["title"]
    try:
        abstract= bib_data.entries[entry].fields["abstract"]
    except Exception:
        abstract = "Error"
    year = bib_data.entries[entry].fields["year"]
    try:
        keywords = bib_data.entries[entry].fields["keywords"]
    except Exception:
        keywords = "Error"
    list_keywords = keywords.split(",")
    total_list_keywords = []
    for string in list_keywords:
      total_list_keywords.append(string.lstrip())
    url = bib_data.entries[entry].fields["url"]
    print(f"title: {title} \n keywords: {total_list_keywords}, \n year: {year}, \n url: {url}, \n abstract: {abstract}")

    for i in bib_data.entries[entry].persons["author"]:
        print(i)
        #print(f"names: {i.first_names }, middle_name: {i.middle_names }, last_name: {i.last_names}")
        test = i.first_names + i.middle_names + i.last_names
        authors = " ".join(test)
        print(authors)
#print(bib_data.entries["OTAY2024123874"].fields["title"])
