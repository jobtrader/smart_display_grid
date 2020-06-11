from selenium import webdriver
from config import config


display_setting = config('webconfig.ini', 'Display')
options = webdriver.ChromeOptions()
# options.add_argument("--kiosk")
# options.add_experimental_option("detach", True)
url = "http://" + display_setting['ip'] + ":" + display_setting['port'] + "/showcredential?"
driver = webdriver.Chrome(options=options)


def concat_argument(ids):
    ret_url = url
    for id in ids:
        ret_url += 'image={0}&'.format(id)
    return ret_url[:-1]


def show_credential(ids):
    global driver
    try:
        driver.get(concat_argument(ids))
    except:
        driver = webdriver.Chrome(options=options)
        driver.get(concat_argument(ids))
