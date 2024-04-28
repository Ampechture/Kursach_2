from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

from selenium.webdriver.chrome.options import Options



login = "s.odoevtsev@g.nsu.ru"
password = "VE32seaok"
def get_all_pages(driver, query):
    query.replace(" ", "%20")
    for i in range(100):
        query_t = f'https://www.sciencedirect.com/search?qs={query}&show=100&offset={i * 100}'
        driver.get(query_t)
        #select_all
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="srp-toolbar"]/div[1]/div[1]/div/label/span[1]').click()
        #export button
        driver.find_element("xpath", '//*[@id="srp-toolbar"]/div[1]/div[3]/div/div/button').click()
        #export to bibtex
        driver.find_element("xpath", '/html/body/div[5]/div/div/div/p/div/div/button[3]').click()

def login_logic(login, password):
    #where to save
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        os.chdir("downloads")
        current_folder = os.getcwd()
    else:
        os.chdir("downloads")
        current_folder = os.getcwd()

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": current_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}]
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://id.elsevier.com/as/authorization.oauth2?platSite=SD%2Fscience&scope=openid%20email%20profile%20els_auth_info%20els_idp_info%20els_idp_analytics_attrs%20els_sa_discover%20urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&response_type=code&redirect_uri=https%3A%2F%2Fwww.sciencedirect.com%2Fuser%2Fidentity%2Flanding&authType=SINGLE_SIGN_IN&prompt=login&client_id=SDFE-v4&state=retryCounter%3D0%26csrfToken%3D1c723de8-4999-4d50-947a-c5579b7c9dbf%26idpPolicy%3Durn%253Acom%253Aelsevier%253Aidp%253Apolicy%253Aproduct%253Aindv_identity%26returnUrl%3D%252Fsearch%253Fqs%253Dsmart%252520city%2526show%253D100%2526offset%253D100%26prompt%3Dlogin%26cid%3Datp-90d6a815-3edf-4dce-afec-b8c092eaa658&els_policy=idp_policy_indv_identity_plus")
    driver.find_element("xpath", '//*[@id="bdd-email"]').send_keys(login)
    driver.find_element("xpath", '//*[@id="bdd-elsPrimaryBtn"]').click()
    #aceept cookies //*[@id="onetrust-accept-btn-handler"]
    time.sleep(2)
    driver.find_element("xpath", '//*[@id="onetrust-accept-btn-handler"]').click()
    driver.find_element("xpath", '//*[@id="bdd-password"]').send_keys(password)
    driver.find_element("xpath", '//*[@id="bdd-elsPrimaryBtn"]').click()
    time.sleep(2)
    try:
        get_all_pages(driver, "smart city")
    except Exception:
        print("aboba")
        driver.quit()

    time.sleep(120)
