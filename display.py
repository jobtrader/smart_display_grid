from selenium import webdriver
from config import config


display_setting = config('webconfig.ini', 'Display')
options = webdriver.ChromeOptions()
# options.add_argument("--kiosk")
# options.add_experimental_option("detach", True)
url = "http://" + display_setting['ip'] + ":" + display_setting['port'] + "/showcredential?"
driver_path = r".\Chromedriver\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path, options=options)


def concat_argument(kwargs):
    ret_url = url
    for key in kwargs:
        ret_url += '{0}={1}&'.format(key, kwargs[key])
    return ret_url[:-1]


def show_credential(kwargs):
    global driver
    try:
        driver.get(concat_argument(kwargs))
    except:
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        driver.get(concat_argument(kwargs))
