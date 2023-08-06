import re
import platform
import os

class Tools:
    
    isWindows = platform.system() == "Windows"

    def __init__(self):     
        pass

    def Checker(self, action):
        if action == "clear":
            if self.isWindows:
                os.system("cls")
            else:
                os.system("clear")
        elif action == "checker":
            if self.isWindows:
                return True
            else:
                return self.isWindows

    def PipInstall(self, *args):
        for pip in args:
            try:
                __import__(pip)
            except Exception as e:
                _module = re.search("'(.+)'", str(e)).group().replace("'", "").strip()
                if self.isWindows:
                    os.system(f"python -m pip install {_module}")
                else:
                    os.system(f"pip3 install {_module}")
                self.Checker("clear")
    
    PipInstall("requests")

    def Scraper(self, type_s):
        
        def Save(text):
            with open("proxies.txt", "wb") as file:
                file.write(text)
                file.close()

        import requests

        url_to_scrape = ["https://api.proxyscrape.com/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=no&anonymity=all&simplified=true", "https://api.proxyscrape.com/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all&simplified=true"]
        
        useHttp = url_to_scrape[0]
        useHttps = url_to_scrape[1]

        if type_s == "http":
            bodyHttp = requests.get(useHttp).content.strip()
            Save(bodyHttp)
        elif type_s == "https":
            bodyHttps = requests.get(useHttps).content.strip()
            Save(bodyHttps)