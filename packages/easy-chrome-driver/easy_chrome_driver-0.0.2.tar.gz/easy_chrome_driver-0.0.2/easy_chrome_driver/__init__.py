# -*- coding: utf-8 -*-
"""
Created on Mon Mar 08 15:29:32 2021

@author: Vaibhav
"""

# Dependencies 
import random
import time
import zipfile
import json
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# Global variables

software_names = [SoftwareName.CHROME.value,SoftwareName.CHROMIUM.value, SoftwareName.FIREFOX.value, SoftwareName.ICEWEASEL.value, SoftwareName.INTERNET_EXPLORER.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.CHROMEOS.value, OperatingSystem.MACOS.value, OperatingSystem.MAC.value, OperatingSystem.MAC_OS_X.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
file_path = os.path.join(os.getcwd(),'proxy_driver')

# Folder for proxy_driver files

if not os.path.exists('proxy_driver'):
    os.makedirs('proxy_driver')
    sys.stdout.write('proxy_driver folder is created')
    os.makedirs(os.path.join(file_path,'user_data'))
    sys.stdout.write('user_data folder is created inside the proxy driver')

# Module

class proxy_driver():
    def __init__(self,PROXY_USER='',PROXY_PASS='',user_path = os.path.join(file_path,'user_data')):
        '''
        proxy_driver(PROXY_USER='',PROXY_PASS='',user_path = None)
            Create a driver class with the above parameters
        
        Parameters:
        
            PROXY_USER : string, default ''
                User name for the Proxies in proxies.json file in proxy_driver folder.
            PROXY_PASS : string, default - ''
                Password for the Proxies in proxies.json file in proxy_driver folder.
            user_path : string, default './proxy_driver/user_data'
                Path to store user data generated during scrapping.
        
        See also
            proxy_driver.get_chromedriver(), proxy_driver.update_proxies()

        '''
        self.PROXY_HOST = '' #1.53.137.164
        self.PROXY_PORT = '' #4145
        self.PROXY_TYPE = '' #socks4
        self.PROXY_USER = PROXY_USER #abc
        self.PROXY_PASS = PROXY_PASS #*@x
        self.user_path = user_path #/home/user/user_data
        self.session_url = None
        self.session_id = None      
        
    def __get_extension(self):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """
        
        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "%s",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };
        
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (self.PROXY_TYPE,self.PROXY_HOST, self.PROXY_PORT, self.PROXY_USER, self.PROXY_PASS)
        return (manifest_json,background_js)


    def get_chromedriver(self,use_proxy = False,save_user_data = True, user_agent = True,headless = False,download_path = file_path, driver_path = None):
        '''
        get_chromedriver(self,use_proxy = False,save_user_data = True, user_agent = True,headless = False,download_path = file_path, driver_path = None)
            Create chrome driver instance with the following parameters.
        
        Parameters:

            use_proxy : bool, default False
                Use a random proxy selected from 'proxies.json' file in proxy_driver folder with username and password passed into proxy_driver class.
                To update the 'proxies.json' run proxy_driver().update_proxies()
                or Manually add the proxy as 'proxy:port':type in the json file. Eg. '172.67.182.48:80':http

            save_user_data : boo;, default True
                Saves the user data generated while using web driver in the user_data folder.
            user_agent : bool, default True
                Changes user agent every time the web driver is called.
            headless : bool, default False
                Run the driver without opening it. i.e. in the background
            download_path : bool, default './proxy_driver'
                To change the default download path of the chrome driver
            driver_path : bool, default None
                To change the default driver path of the chrome_driver. For default path refer chromedriver documentation.
                https://chromedriver.chromium.org/getting-started
        '''
#        path = os.path.dirname(os.path.abspath(__file__))
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            proxies = json.load(open(os.path.join(file_path,'proxies.json')))
            self.PROXY_HOST, self.PROXY_PORT = random.choice(list(proxies.keys())).split(':')
            self.PROXY_TYPE = proxies['%s:%s' %(self.PROXY_HOST,self.PROXY_PORT) ]
            manifest_json,background_js = self.__get_extension()
            pluginfile = 'proxy_auth_plugin.zip'
    
            with zipfile.ZipFile(os.path.join(file_path,pluginfile), 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(os.path.join(file_path,pluginfile))
        else:
            self.PROXY_HOST,self.PROXY_TYPE,self.PROXY_PORT = ['']*3
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % user_agent_rotator.get_random_user_agent())
        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('window-size=1420,1080')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-infobars')
#            chrome_options.add_argument("ignore-certificate-errors")
        if save_user_data:
            chrome_options.add_argument("--user-data-dir="+self.user_path)
            chrome_options.add_argument("--enable-file-cookies")
        if download_path:
            prefs = {"download.default_directory": download_path}#,"download.prompt_for_download": False,"download.directory_upgrade": True}
            chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("ignore-certificate-errors")
        if driver_path:
            driver = webdriver.Chrome(driver_path,chrome_options=chrome_options,desired_capabilities=DesiredCapabilities.CHROME)
        else:
            driver = webdriver.Chrome(chrome_options=chrome_options,desired_capabilities=DesiredCapabilities.CHROME)
        self.session_url = driver.command_executor._url
        self.session_id = driver.session_id
        with open(os.path.join(file_path,'log.txt'),'a') as f:
            f.write('-'*20+'\n')
            f.write('Session_url :'+self.session_url+'\n')
            f.write('Session__id :'+self.session_id+'\n')
            f.write('Session_proxy :'+self.PROXY_HOST+'\n')
            f.write('Session_port :'+self.PROXY_PORT+'\n')
            f.write('Session_type :'+self.PROXY_TYPE+'\n')
        return driver
    def update_proxies(self,no_of_pages = 3,driver_path = None):
        '''
        update_proxies(self,no_of_pages = 3,driver_path = None)
            Update the 'proxies.json' file in the proxy_driver folder with fresh free ips.
            
        Parameters:

        no_of_pages : int, default 3
            To get large number of proxies increase the number of pages.
        driver_path : str, default None
            If the executable file of driver is at different location than default. For default location refer chromedriver documentation.
            https://chromedriver.chromium.org/getting-started
        '''
        if driver_path:
            driver = self.get_chromedriver(use_proxy=False,headless = True, driver_path = driver_path)
        else:
            driver = self.get_chromedriver(use_proxy=False,headless = True)
        proxy_site = 'https://hidemy.name/en/proxy-list/'
        driver.get(proxy_site)
        wait = WebDriverWait(driver,10)
        def get_row_element_text(r,c):
            return driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[%s]/td[%s]'%(str(r),str(c))).text
        d={}
        for i in range(no_of_pages):
            driver.get(proxy_site+'?start='+str(i*64)+'#list')
            for k in range(1,65):
                element = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[%s]/td[4]/div/div'%(str(k)))))
                if element.get_attribute("style").split(':')[-1][:-1].strip()=='rgb(121, 188, 0)':
                    d[get_row_element_text(k,1)+':'+get_row_element_text(k,2)] = get_row_element_text(k,5).lower().split(',')[0]
#                if wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr["%s"]/td[4]/div/div'(str(k))))).getAttribute("style")[-6:]=='79bc00':
#                    d[driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[%s]/td[1]'(str(k))).text+':'+driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[%s]/td[2]'(str(k))).text] = driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[%s]/td[5]'(str(k))).text
#        for i in range(no_of_pages):
#            driver.get(proxy_site+'?start='+str(len(d))+'#list')
#            element = wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div[4]/div/div[4]/table")))
#            t = element.text    
#            t = t[t.find('\n')+1:].split('\n')
#            for i in range(0,len(t),3):
#                d[':'.join(t[i].split()[:2])] = t[i+2].split()[0].lower()
        driver.quit()
        with open(os.path.join(file_path,'proxies.json'),'w') as f:
            json.dump(d,f,indent = 4)

# Testing

if __name__=="__main__":
    p = proxy_driver()
    p.update_proxies()
    driver = p.get_chromedriver(use_proxy = True)    
    driver.get('https://whatismyipaddress.com/')
