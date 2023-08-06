
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from easy_chrome_driver import proxy_driver as pc
pc().update_proxies()
driver = pc().get_chromedriver(use_proxy = True)    
driver.get('https://whatismyipaddress.com/')