
import sys
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

def duration_split(duration):
    hour = 0
    min = 0
    sec = 0
    list = duration.split(":")
    hour = int(list[0])
    min = int(list[1])
    sec = int(list[2])
    return hour*3600 + min*60 + sec

def start(url, dur, loop):
    if len(dur.split(":")) == 3:
        dur = duration_split(dur)
    else:
        print("Invalid duration format. Please use HH:MM:SS")
        return
    if loop.lower() == "inf":
        loop = 999999999
    else:
        try:
            loop = int(loop)
        except:
            print("Invalid loop count.")
            return

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    while loop > 0:
        driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
        driver.get(url)
        time.sleep(3)
        # The following line is commented out because it might not be necessary for shorts, 
        # and it was causing issues in the Firefox script.
        # plybtn = driver.find_element_by_class_name("ytp-play-button")
        # plybtn.click()                      
        time.sleep(dur)
        driver.close()
        loop -= 1

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python YouTubeBot_modified.py <url> <duration> <loop>")
        sys.exit(1)
    
    url = sys.argv[1]
    duration = sys.argv[2]
    loop_count = sys.argv[3]
    
    start(url, duration, loop_count)
