from selenium import webdriver
from config import config


display_setting = config('webconfig.ini', 'Display')
options = webdriver.ChromeOptions()
# options.add_argument("--kiosk")
# options.add_experimental_option("detach", True)
url = "http://" + display_setting['ip'] + ":" + display_setting['port'] + "/showcredential?"
driver_path = r".\Chromedriver\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path, options=options)


def concat_argument(args):
    ret_url = url
    for arg in args:
        ret_url += 'image={0}&'.format(arg)
    return ret_url[:-1]


def show_credential(image_paths):
    global driver
    try:
        driver.get(concat_argument(image_paths))
    except:
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        driver.get(concat_argument(image_paths))
