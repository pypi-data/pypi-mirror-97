easy-chrome-driver: Abstraction for chrome driver for easy modifications
========================================================================

**easy-chrome-driver** is a Python package that provides fast and
flexible modifications in chrome driver by overcoming frequent errors.It
supports proxy implementation and updation along with generating session
id and session url which is useful to reuse the existing webdriver
window.

Main Features
-------------

Here are the things that easy\_chrome\_driver does well without much
effort:

-  Setting up proxy using chrome web extension created by
   ``easy_chrome_driver`` module.
-  Using username and password for the proxies
-  Updating the proxy list automatically along with manual addition
-  Saving user data and session metadata for the reuse of chrome driver
   session.
-  Running chrome driver headless without any errors
-  Using any driver path for the chrome driver

Source Code
-----------

The source code is currently hosted on GitHub at:
https://github.com/vaibhavkpatel1/easy\_chrome\_driver

Dependencies
------------

-  `selenium - Automate web browser interaction from
   Python. <https://pypi.org/project/selenium/>`__
-  `random-user-agent - Provides list of user agents, from a collection
   of more than 326,000+ user agents, based on
   filters. <https://pypi.org/project/random-user-agent/>`__

Installation
------------

easy-chrome-driver can be installed from PyPI:

.. code:: sh

    pip3 install easy-chrome-driver

License
-------

`MIT <LICENSE>`__

Documentation
-------------

**Create instance for proxy\_driver, update proxies and get driver**

.. code:: sh

    from easy_chrome_driver import proxy_driver as pc
    pc().update_proxies()
    driver = pc('user_name','password').get_chromedriver(use_proxy=True)


::

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

::

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

**Update proxies**

This code must be run before the first time use of proxy, else create the json file manually in the proxy_driver folder. Eg. Eg. '172.67.182.48:80':http

.. code:: sh

    pc().update_proxies()

::

    update_proxies(self,no_of_pages = 3,driver_path = None)
        Update the 'proxies.json' file in the proxy_driver folder with fresh free ips.
        
    Parameters:

    no_of_pages : int, default 3
        To get large number of proxies increase the number of pages.
    driver_path : str, default None
        If the executable file of driver is at different location than default. For default location refer chromedriver documentation.
        https://chromedriver.chromium.org/getting-started

**Following folders will be created in your current directory**

::

    proxy_driver\
        user_data\
        proxy_auth_plugin.zip
        proxies.json
        log.txt
        
