import Parser_selenium
import couple_bib_files

def data_fetcher(query):
    query = str(query)
    Parser = Parser_selenium.ParserMain(query)
    try:
        Parser.login_logic()
    except Exception: 
        couple_bib_files(query)
