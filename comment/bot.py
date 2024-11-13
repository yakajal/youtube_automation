import undetected_chromedriver as uc
import pickle
import time
import openpyxl
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor

def create_driver():
    options = uc.ChromeOptions()
    options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    return uc.Chrome(options=options)

def load_cookies(driver, cookie_file):
    driver.get("https://www.youtube.com")
    # time.sleep(2)  # Allow time for the page to load
    with open(cookie_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            if 'domain' in cookie and 'youtube.com' in cookie['domain']:
                driver.add_cookie(cookie)
    print(f"Cookies loaded from {cookie_file}")

def post_random_comments(driver, video_url, comments, total_comments=20):
    driver.get(video_url)
    time.sleep(5)

    # Scroll to the comments section
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(random.uniform(2,5))
    for _ in range(total_comments):
        # Get a random comment text
        comment_text = random.choice(comments)
        filter= ''.join(c for c in comment_text if ord(c) < 0x10000)

        # Locate the comment box and enter the comment
        comment_box_xpath ="/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[5]/ytd-comment-simplebox-renderer/div[3]/ytd-comment-dialog-renderer/ytd-commentbox/div[2]/div/div[2]/tp-yt-paper-input-container/div[2]/div/div[1]/ytd-emoji-input/yt-user-mention-autosuggest-input/yt-formatted-string/div"

           # Retry finding the comment box
        for attempt in range(2):  # Try 3 times
            try:
                comment_box = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, comment_box_xpath))
                )
                print("Comment box found!")
                break  # Exit the loop if successful
            except Exception as e:
                print(f"Attempt {attempt + 1}: Comment box not found, retrying... Error: {e}")
                time.sleep(2)  # Wait before retrying

        if 'comment_box' in locals():
            comment_box.click()
            time.sleep(1)
            comment_box.send_keys(filter)
        # Submit the comment
        submit_button_xpath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[5]/ytd-comment-simplebox-renderer/div[3]/ytd-comment-dialog-renderer/ytd-commentbox/div[2]/div/div[4]/div[5]/ytd-button-renderer[2]/yt-button-shape"

        submit_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, submit_button_xpath))
        )
        submit_button.click()
         # Wait before posting the next comment
        print(f"Posted comment: {comment_text}")
        time.sleep(2)
def load_comments_from_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    comments = [row[0] for row in sheet.iter_rows(values_only=True) if row[0]]
    return comments
def run_for_account(cookie_file, video_url, comments):
    driver = create_driver()
    try:
        load_cookies(driver, cookie_file)
        post_random_comments(driver, video_url, comments)
    finally:
        driver.quit()
# Main function to handle the auto-commenting
def main():
    accounts = [
    "cookies_account_1.pkl",
    "cookies_account_2.pkl",
    "cookies_account_4.pkl",
    "cookies_account_5.pkl",
    "cookies_account_6.pkl",
    "cookies_account_7.pkl",
    "cookies_account_9.pkl",
    "cookies_account_10.pkl",
    "cookies_account_11.pkl",
    "cookies_account_12.pkl",
    "cookies_account_13.pkl", 
    "cookies_account_15.pkl",
    "cookies_account_16.pkl",
    "cookies_account_17.pkl",
    "cookies_account_21.pkl",
    "cookies_account_22.pkl",
    "cookies_account_23.pkl",
    "cookies_account_24.pkl",
    "cookies_account_25.pkl",
    "cookies_account_26.pkl",
    "cookies_account_27.pkl",
    "cookies_account_29.pkl",
    "cookies_account_30.pkl",
    "cookies_account_31.pkl",
    "cookies_account_34.pkl",
    "cookies_account_35.pkl",
    "cookies_account_36.pkl",
    "cookies_account_37.pkl",
    "cookies_account_38.pkl",
    "cookies_account_39.pkl",
    "cookies_account_40.pkl",
    "cookies_account_41.pkl",
    "cookies_account_42.pkl",
    "cookies_account_43.pkl",
    "cookies_account_45.pkl",
    "cookies_account_46.pkl",
    "cookies_account_47.pkl",
    "cookies_account_48.pkl",
    "cookies_account_49.pkl",
    "cookies_account_53.pkl",  # Path to the 53rd account's cookie file
]
    
    video_url = "https://youtu.be/LZbGkTQ5UTA?si=2bYohE3f7L3Q6w1s"  # Video URL
    comments_file_path = "100.xlsx"  # Path to your comments Excel file

    comments = load_comments_from_excel(comments_file_path)

    
    total_iterations = 8000
     # Total iterations to run
    max_workers = 4
     # Number of parallel browser sessions

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(total_iterations):
            account = accounts[i % len(accounts)] # Randomly select an account
            executor.submit(run_for_account, account, video_url, comments)
if __name__ == "__main__":
    main()
