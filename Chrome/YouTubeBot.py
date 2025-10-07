import sys
import threading
from selenium import webdriver
import time
from datetime import datetime
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

def worker(url, dur, loop_count, thread_id):
    views_generated = 0
    while loop_count > 0:
        try:
            driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
            driver.get(url)
            time.sleep(3)
            # The following line is commented out because it might not be necessary for shorts,
            # and it was causing issues in the Firefox script.
            # plybtn = driver.find_element_by_class_name("ytp-play-button")
            # plybtn.click()
            time.sleep(dur)
            driver.close()
            loop_count -= 1
            views_generated += 1
            print(f"[Thread {thread_id}] View {views_generated} generated at {datetime.now()}")
        except Exception as e:
            print(f"[Thread {thread_id}] Error: {e}")
            # Optional: add a delay before retrying
            time.sleep(10)


def start(url, dur, loop, num_browsers):
    if len(dur.split(":")) == 3:
        dur = duration_split(dur)
    else:
        print("Invalid duration format. Please use HH:MM:SS")
        return

    try:
        num_browsers = int(num_browsers)
    except:
        print("Invalid number of browsers.")
        return

    global options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if loop.lower() == "inf":
        loop_per_browser = float('inf')
    else:
        try:
            total_loop_count = int(loop)
            loop_per_browser = total_loop_count // num_browsers
        except:
            print("Invalid loop count.")
            return

    threads = []
    for i in range(num_browsers):
        # The last thread gets the remainder of the loops
        if i == num_browsers - 1:
            if loop.lower() != "inf":
                loop_per_browser += total_loop_count % num_browsers
        
        thread = threading.Thread(target=worker, args=(url, dur, loop_per_browser, i + 1))
        threads.append(thread)
        thread.start()
        print(f"Started thread {i+1}")

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python YouTubeBot.py <url> <duration> <loop> <num_browsers>")
        sys.exit(1)

    url = sys.argv[1]
    duration = sys.argv[2]
    loop_count = sys.argv[3]
    num_browsers = sys.argv[4]

    start(url, duration, loop_count, num_browsers)