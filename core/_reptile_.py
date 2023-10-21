import selenium.webdriver
import chromedriver_autoinstaller
import time
import tqdm
import os
import string

class Reptile:

    def __init__(self, channel, folder):
        self.channel = channel
        self.folder = folder
        return

    def getDriver(self, display=True):
        _ = chromedriver_autoinstaller.install()
        option = selenium.webdriver.ChromeOptions()
        if(not display): option.add_argument("--headless")
        driver = selenium.webdriver.Chrome(options=option)
        return(driver)

    def getInventory(self, link):
        inventory = []
        if(self.channel=='youtube'):
            translation = str.maketrans('', '', string.punctuation)
            path = f'{self.folder}/{link.translate(translation)}.txt'
            here = os.path.exists(path)
            if(here):
                record = open(path, 'r')
                inventory = record.readlines()
                inventory = [_.replace("\n", "") for _ in inventory]
                record.close()
                return(inventory)
            driver = self.getDriver(display=False)
            driver.get(link)
            time.sleep(3)
            script = 'document.documentElement.scrollHeight'
            height = driver.execute_script(f"return {script}")
            while True:
                command = f"window.scrollTo(0, {script});"
                driver.execute_script(command)
                time.sleep(1)
                update = driver.execute_script(f"return {script}")
                if(height==update):break
                else: height=update
                continue
            iteration = driver.find_elements('id', "video-title")
            for item in tqdm.tqdm(iteration):
                content = item.get_attribute('href')
                identity = content.split('?v=')[-1].split('&')[0]
                if(content): inventory += [identity]
                continue
            driver.close()
            pass
        os.makedirs(os.path.dirname(path), exist_ok=True)
        record = open(f"{path}", 'w')
        for item in inventory: record.write(f"{item}\n")
        record.close()
        return(inventory)

    pass