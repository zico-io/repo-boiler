import json
from wget import download
from sys import exit
from re import compile
from time import sleep
from os import mkdir
from os.path import exists
from csv import writer, reader
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

with open('./data/config.json', 'r') as config:
    config = json.load(config)
    
class NotEnoughCPUs(Exception):
    def __init__(self, message):
        super().__init__(message)

class Scraper:
    def __init__(self):
        
        
        print('Initiating webdriver')
        options = {
            'request_storage': 'memory',
            'request_storage_max_size': 4
        }
        
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), seleniumwire_options=options)
        self.driver.implicitly_wait
        self.driver.scopes = [
            '.*akamaihd.*',
            '.*embed-fastly.*'
        ]
        
    def fetchVideoUrls(self) -> None:
        print('Logging in')
        self.login(self.driver)
        
        print('Loading course page.')
        self.driver.get(config["course_url"])
        
        container = BeautifulSoup(self.driver.page_source, "html.parser").find(class_='course-accordian')
        last_link = None

        illegal_char = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', '/', ' ', '$', '!', '\'', '\"', ':', '@', '+', '`', '|', '=']

        self.url_list = open('./data/urls.csv', 'w', newline='')
        self.write_to_list = writer(self.url_list)

        print('Navigating through pages.')
        for lesson in container.find_all("a", attrs={'href': compile("^https://")}):
            self.driver.get(lesson.get('href'))
            del self.driver.requests
            for iframe in BeautifulSoup(self.driver.page_source, 'html.parser').find_all('iframe', attrs={'src': compile("^https://")}):
                self.driver.get(iframe.get('src'))
                title = str(self.driver.title)
                for char in illegal_char:
                    if char in title:
                        title = title.replace(char, '')
                
                count = 0
                while True:
                    try:
                        WebDriverWait(self.driver, 30).until(lambda d: d.find_element(by = By.ID, value='wistia_video'))
                        self.driver.find_element(by = By.ID, value='wistia_video').click()
                        if self.driver.last_request.url.find('/seg'):
                            request = self.driver.last_request.url.split('/seg').pop(0)
                        else:
                            request = self.driver.last_request.url
                    except AttributeError:
                        sleep(2)
                    except IndexError:
                        sleep(2)
                    else:
                        if request != last_link:
                            break
                        else:
                            if count < 3:
                                count += 1
                                sleep(2)
                            else:
                                sleep(54)
                                count = 0
                                
                last_link = request
                url = [request, title]
                url[0] = url[0].replace('m3u8', 'mp4')
                self.write_to_list.writerow(url)
                    
        print('Links successfully fetched.')
        self.url_list.close()
        self.driver.quit()
            

    def login(self, driver) -> None:
        driver.get(config["login_url"])
        if "Login" in driver.title:
            email = driver.find_element(by=By.XPATH, value='//input[@name="email"]')
            password = driver.find_element(by=By.XPATH, value='//input[@name="password"]')
            submit = driver.find_element(by=By.CSS_SELECTOR, value='button')
            email.send_keys(config["user"])
            password.send_keys(config["pass"])
            return submit.click()        
        else:
            print(driver.title)

class Downloader:    
    
    save_dir = str
    
    def main(self) -> None:
        with open('./data/urls.csv', newline='') as csvfile:
            url_list = list(reader(csvfile))
            
        for count, line in enumerate(url_list):
            pass
        print(count + 1, 'links found.')
        
        self.save_dir = self.getSaveDirectory()
        with Pool(config["n_cpu"]) as pool:
            pool.starmap(self.downloadFile, enumerate(url_list, start=1))
        
    def downloadFile(self, idx, url, title):
        print(f'Downloading {title} from {url}', flush=True)
        download(url, out = self.save_dir + '\\' + title)
        
    
    def getSaveDirectory(self):
        while True:
            save_directory = input('Enter destination folder (ex. D:\\videos) ')
            try:
                mkdir(save_directory)
            except FileExistsError:
                while True:
                    ans = input('Destination folder already exists, continue anyway? y/n ')
                    if ans == 'y':
                        break
                    elif ans == 'n':
                        pass
                    else:
                        print('Destination folder already exists, continue anyway? y/n ')
                        return save_directory
            except FileNotFoundError:
                print('Specified directory is invalid, check the path entered.')
            else:
                print('Directory successfully created.')
                return save_directory  
    
def main() -> None:
    avail_cpu = cpu_count()
    if int(config["n_cpu"]) >= avail_cpu:
        raise NotEnoughCPUs(f'ERROR: Too many CPUs allocated. {avail_cpu} CPUs available, {config["n_cpu"]} were attempted to be used.')
    
    scraper = Scraper()
    
    if exists('./data/urls.csv'):
        while True:
            skip_fetch = input('urls.csv contains data. Would you like to skip fetching? y/n ')
            if skip_fetch == 'y':
                print('Skipping fetching new links.')
                break
            elif skip_fetch == 'n':
                while True:
                    overwrite = input('WARNING: Data inside urls.csv will be destroyed upon beginning a new fetch job. Continue? y/n ')
                    if overwrite == 'y':
                        print('Deleting data.')
                        with open('./data/urls.csv', 'w+'): pass
                        print('Fetching URLs.')
                        scraper.fetchVideoUrls()
                    elif overwrite == 'n':
                        break
                    else:
                        print('WARNING: Data inside urls.csv will be destroyed upon beginning a new fetch job. Continue? y/n ')
            else:
                print('urls.csv contains data. Data will be overwritten. Continue? y/n ')
    else:
        scraper.fetchVideoUrls()
                
    downloader = Downloader()
    downloader.main()
    print('\nAll operations completed successfully.')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Terminating')
        exit(0)
        