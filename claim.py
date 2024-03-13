import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

print("Initialising the HOT Wallet Auto-claim Python Script - Good Luck!")
session_path = "./selenium2"
os.makedirs(session_path, exist_ok=True)
screenshots_path = "./screenshots"
os.makedirs(screenshots_path, exist_ok=True)

# Correct the path to your ChromeDriver here
chromedriver_path = "/usr/local/bin/chromedriver"

# Create a Service object
service = Service(chromedriver_path)

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={session_path}")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")  # Set log level to suppress INFO and WARNING messages
chrome_options.add_argument("--disable-bluetooth")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize WebDriver, passing the service object
driver = webdriver.Chrome(service=service, options=chrome_options)

url = 'https://tgapp.herewallet.app/auth/import#tgWebAppData=user%3D%257B%2522id%2522%253A831612161%252C%2522first_name%2522%253A%2522John%2522%252C%2522last_name%2522%253A%2522Doe%2522%252C%2522username%2522%253A%2522j_doe%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D&chat_instance%3D-1658397054350349435&chat_type%3Dsender&auth_date%3D1710122886&hash%3Da8ed62de9dc49dad96f3a46d8297046a51ad4587a625bcefcf611d06be2bf499&tgWebAppVersion=7.0&tgWebAppPlatform=web&tgWebAppBotInline=1&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22button_color%22%3A%22%233390ec%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%23707579%22%2C%22link_color%22%3A%22%2300488f%22%2C%22secondary_bg_color%22%3A%22%23f4f4f5%22%2C%22text_color%22%3A%22%23000000%22%2C%22header_bg_color%22%3A%22%23ffffff%22%2C%22accent_text_color%22%3A%22%233390ec%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22section_header_text_color%22%3A%22%233390ec%22%2C%22subtitle_text_color%22%3A%22%23707579%22%2C%22destructive_text_color%22%3A%22%23df3f40%22%7D'

time.sleep(1)
wait = WebDriverWait(driver, 10)

def Login(iseed, iseed_index, total_seeds):
    err = 0
    while True:
        try:
            print('Login attempt {} out of 2 on seed number {} of {}.'.format(err+1, iseed_index, total_seeds))
            driver.get(url)

            # Use WebDriverWait to wait for elements up to 60 seconds
            wait = WebDriverWait(driver, 60)
            try:
              print("Attempting to find the seed input area...")
              seed_area = '/html/body/div[1]/div/div[1]/label/textarea'
              seed_input = wait.until(EC.element_to_be_clickable((By.XPATH, seed_area)))
              driver.save_screenshot(os.path.join(screenshots_path, "01_recovery_using_seed_phrase.png"))
              print("Seed input area found. Attempting to enter the seed phrase...")
              seed_input.click()
              seed_input.send_keys(iseed)
              driver.save_screenshot(os.path.join(screenshots_path, "02_enter_seed_phrase.png"))
              print("Seed phrase entered successfully.")

              print("Looking for the 'Continue' button to proceed with seed phrase submission...")
              enter_seed_xpath = '//*[@id="root"]/div/div[2]/button'
              enter_seed_button = wait.until(EC.element_to_be_clickable((By.XPATH, enter_seed_xpath)))
              driver.save_screenshot(os.path.join(screenshots_path, "03_before_click_continue.png"))
              enter_seed_button.click()
              driver.save_screenshot(os.path.join(screenshots_path, "04_importing_account.png"))
              print("Seed phrase submission attempted. Waiting for account import confirmation...")
            except TimeoutException as e:
              print("Failed to perform an action due to timeout: {}".format(e))
            except Exception as e:
              print("An error occurred during seed phrase entry or submission: {}".format(e))

            try:
              print("Attempting to select the account...")
              # Wait for the account selection button to be clickable
              account_selection_button_xpath = '//*[@id="root"]/div/button'
              account_selection_button = wait.until(EC.element_to_be_clickable((By.XPATH, account_selection_button_xpath)))
              driver.save_screenshot(os.path.join(screenshots_path, "05_select_account_byID.png"))
              account_selection_button.click()
              print("Account selection attempted. Waiting for the account to log in...")
              driver.save_screenshot(os.path.join(screenshots_path, "06_initial_logged_in_screen.png"))
              print("Account successfully logged in. Proceeding with the next steps.")
            except TimeoutException as e:
              print("Timeout waiting for the account selection button: {}".format(e))
              # Handle the timeout scenario, perhaps by retrying or logging the failure
            except Exception as e:
              print("An error occurred during account selection or login confirmation: {}".format(e))

            try:
              # Replace 'xpath1' and 'xpath2' with your actual XPaths
              success = try_interact_with_elements(driver, '//*[@id="root"]/div/div/div/div[4]/div[1]', '//*[@id="root"]/div/button', screenshot_base="06")
              if success:
                print("Successfully interacted with the elements.")
            except TimeoutException as e:
                print(e)
            
            # Again, wait for the next clickable element
            # enter_seed_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div[4]/div[2]/div')))
            enter_seed_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div[4]/div[1]')))
            enter_seed_button.click()
            driver.save_screenshot(os.path.join(screenshots_path, "07_move_to_claim_page.png"))

            wait_time = claim(iseed, total_seeds, iseed_index)
            return wait_time

        except TimeoutException as e:
            print("Timeout waiting for an element: {}".format(e))
            err += 1
            if err > 2:
                return 60  # Example default wait time in minutes
        except Exception as e:
            print("An error occurred, most possibly trying to proceed to the next step too early OR VPN error: {}".format(e))
            err += 1
            if err > 2:
                return 60  # Leave it an hour, there seems to be some rate throttling if too many requests

def claim(iseed, total_seeds, iseed_index):
    print("Log in successful. Starting Claim Logic!")
    driver.save_screenshot(os.path.join(screenshots_path, "08_confirm_still_same_page.png"))  # Take screenshot
    
    try:
        waktu_xpath = '//*[@id="root"]/div/div[2]/div/div[3]/div/div[2]/div[1]/p[2]'
        waktu_element = driver.find_element(By.XPATH, waktu_xpath)
        waktu_text = waktu_element.text
        forceClaim = False
        
        # Let's see if this wallet is Full or if making a claim is forced on for testing!
        if waktu_text == "Filled" or forceClaim:
            # Attempt to click "Check NEWS" button
            try:
                print("Let's wait 25 seconds for the page to catch up and see if there is any news to read.\n")
                time.sleep(25)
                driver.save_screenshot(os.path.join(screenshots_path, "09_preparing_to_check_news.png"))
                check_news_button_xpath = '//*[@id="root"]/div/div[2]/div/div[3]/div/div[2]/div[2]/button[contains(@class, "sc-ktwOSD eZybGy") and contains(@style, "background: rgb(253, 132, 227)") and contains(text(), "Check NEWS")]'
                check_news_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, check_news_button_xpath)))
                check_news_button.click()
                print("Found and clicked 'Check NEWS' button.\n")
                driver.save_screenshot(os.path.join(screenshots_path, "10_after_checking_news.png"))
            except TimeoutException:
                print("'Check NEWS' button not found or not clickable.")
            
            # Regardless of NEWS button status, attempt to click "Claim HOT" button
            try:
                print("Let's wait 25 seconds for the page to catch up, before finally clicking the claim button!\n")
                time.sleep(25)
                claim_button_xpath = '//*[@id="root"]/div/div[2]/div/div[3]/div/div[2]/div[2]//button[contains(@class, "sc-ktwOSD eZybGy") and contains(text(), "Claim HOT")]'
                claim_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, claim_button_xpath)))
                claim_button.click()
                print("Attempting to submit a claim now! Another 75 second timer.\n")
                driver.save_screenshot(os.path.join(screenshots_path, "11_preparing_to_claim.png"))
                time.sleep(75)
                driver.save_screenshot(os.path.join(screenshots_path, "12_after_the_claim.png"))
                print("Claim attempt finished. Screenshot 12 will show if the pot has reset or not.\n")
                return 5
            except TimeoutException:
                print("Claim HOT' button was not clickable within the expected time. This might be due to it being claimed too recently, or they changed the system again.")
                return 5
        else:
            # If not forcing a claim and not "Filled", process the waiting time
            matches = re.findall(r'(\d+)([hm])', waktu_text)
            if matches:
                total_time = (sum(int(value) * (60 if unit == 'h' else 1) for value, unit in matches))
                print("Not Time to Claim seed [{}] yet. Wait for {} Minutes.".format(iseed_index, total_time))
                return total_time
            else:
                print("No time data found. Check the page or xpath.")
                return None
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))
        return 60  # Let's give them an hour in case of too many errors and potential rate throttling. 
        
# Define your base path for screenshots
screenshot_base = os.path.join(screenshots_path, "screenshot")

# Your function using the screenshot_base with the path included
def try_interact_with_elements(driver, xpath1, xpath2, max_wait=30, interval=10, screenshot_base=screenshot_base):
    wait = WebDriverWait(driver, max_wait)
    cycle_count = 0
    success = False

    while cycle_count < 5 and not success:
        cycle_count += 1
        try:
            # Try interacting with the first element
            first_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath1)))
            first_element.click()
            print("Successfully interacted with the first element.")
            success = True
        except TimeoutException:
            print("Cycle {}: Failed to interact with the first element, trying the second one.".format(cycle_count))
            driver.save_screenshot(f"{screenshot_base}_cycle_{cycle_count}_1.png")

            try:
                second_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath2)))
                second_element.click()
                print("Successfully interacted with the second element, retrying the first one.")
                driver.save_screenshot(f"{screenshot_base}_cycle_{cycle_count}_2.png")
                
                time.sleep(interval)
                first_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath1)))
                first_element.click()
                print("Successfully retried and interacted with the first element after the second.")
                success = True
            except TimeoutException:
                print("Cycle {}: Failed to interact with both elements.".format(cycle_count))
                driver.save_screenshot(f"{screenshot_base}_cycle_{cycle_count}_retry.png")

        if not success:
            time.sleep(interval)  # Wait before retrying in the next cycle

    if not success:
        raise TimeoutException("Failed to interact with the elements within the given cycles.")

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux(here, os.name is 'posix')
    else:
        os.system('clear')

def load_seeds_from_file(seed_file_path):
    """Load seed phrases from a file."""
    try:
        with open(seed_file_path, "r") as file:
            seeds = [line.strip() for line in file if line.strip()]
            if seeds:
                return seeds
            else:
                print("The seeds.txt file is empty.")
                return None
    except FileNotFoundError:
        print("The seeds.txt file does not exist.")
        return None

def validate_and_collect_seeds():
    """Collect and validate seed phrases from user input."""
    seeds = []
    print("Please enter your 12-word seed phrases. Press enter on a blank line when done.")
    while True:
        seed_input = input("Enter seed phrase or press enter to finish: ").strip()
        if not seed_input:
            break
        words = seed_input.split()
        if len(words) == 12 and all(word.isalpha() for word in words):
            seeds.append(seed_input)
        else:
            print("Invalid seed phrase. Each phrase must consist of exactly 12 alphabetical words. Please try again.")
    return seeds

def get_seeds(seed_file_path="seed.txt"):
    """Main function to load or collect seeds."""
    seeds = load_seeds_from_file(seed_file_path)
    if not seeds:
        clear_screen()
        seeds = validate_and_collect_seeds()
        while not seeds:
            print("No seed phrases entered. Please enter at least one seed phrase.")
            seeds = validate_and_collect_seeds()
    return seeds

# Main script execution
seed_file_path = "seed.txt"
seeds = get_seeds(seed_file_path)


# Function to cycle through seeds and perform actions
def cycle_seeds(seeds):
    iseed_index = 0
    wait_times = []

    while True:
        if iseed_index < len(seeds):
            try:
                iseed = seeds[iseed_index]
                print("Starting login attempts on seed {} of {}. Max 2 attempts per seed.".format(iseed_index + 1, len(seeds)))
                wait_time = Login(iseed, iseed_index + 1, len(seeds))
                wait_times.append(wait_time)
            except Exception as e:
                print("Error with seed {}: {}".format(iseed, e))
            finally:
                iseed_index += 1
        else:
            # Handle wait times after processing all seeds or if an exception occurred on the last seed
            min_wait = min([time for time in wait_times if time is not None]) if wait_times else 1
            while min_wait > 0:
                this_wait = min(min_wait, 15)
                print("Waiting for {} more minutes before refreshing timer out of {} minutes...".format(this_wait, min_wait))
                time.sleep(this_wait * 60)
                min_wait -= this_wait
                if min_wait > 0:
                    print("Waiting for another {} minutes.".format(min_wait))
            iseed_index = 0
            wait_times.clear()

cycle_seeds(seeds)  # Ensure seeds is defined and populated with your seed values
