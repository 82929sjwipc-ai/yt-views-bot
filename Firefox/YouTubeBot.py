
import sys
from selenium import webdriver
import time

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

    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.add_argument("--headless")
    while loop > 0:
        driver = webdriver.Firefox(executable_path="./geckodriver", options=options)
        driver.get(url)
        plybtn = driver.find_element_by_class_name("ytp-play-button")
        time.sleep(3)
        # ---> If the video doesnt start playing within three seconds of opening, then disable this  <--- #
        plybtn.click()                      
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
