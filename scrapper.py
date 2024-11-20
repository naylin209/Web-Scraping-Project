""" NSSA 220 Final Group: Nay Lin Aung & Ayesha Khan"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://www.rit.edu/dubai/directory"

# Load the webpage
def load_webpage():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    driver.maximize_window()
    return driver

# Manually scroll to the bottom of the page to load more data
def scroll_to_load(driver):
    # Scroll down in increments and wait for content to load
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for the page to load
        
        # Calculate the new scroll height and compare it with the last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # No more content is loaded
        last_height = new_height
        print("Scrolling...")

def load_more(driver):
    try:
        accept_button = driver.find_element(By.ID, "consent-accept")
        accept_button.click()
        print('Cookies button clicked successfully')
    except Exception as e:
        print("Consent button not found or already accepted:", e)
    #Clicking 'load more' 5 times
    for i in range(5):
        try:
            load_more_button = driver.find_element(By.CLASS_NAME, "see-more")
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            time.sleep(1)
            
            load_more_button.click()
            print(f"'Load More' clicked {i + 1} times")
            
            time.sleep(3)
                
        except Exception as e:
            print(f"Error clicking 'Load More' button on iteration {i + 1}: {e}")
            break
    print("Finshed Clicking 'Load More'")
   
# Extract the data from the page
def extract_data(driver):
    LOAD_MORE_BUTTON_SELECTOR = ".see-more"  # Button to load more content
    ARTICLE_SELECTOR = ".views-row article.card.person-directory"  # Selector for each person's card
    NAME_SELECTOR = ".person--info a"  # Selector for name
    TITLE_SELECTOR = ".person--info .directory-text-small"  # Selector for title
    EMAIL_SELECTOR = ".person--extra-text a"  # Selector for email
    # Parse the page source with BeautifulSoup
    
    instructors = []
    time.sleep(3)  # Ensure all dynamically loaded content is fully rendered
    articles = driver.find_elements(By.CSS_SELECTOR, ARTICLE_SELECTOR)
    print(f"Total articles found: {len(articles)}")
 
    for article in articles:
        try:
            # Extract name
            name = article.find_element(By.CSS_SELECTOR, NAME_SELECTOR).text.strip()
 
            # Extract title (set to "null" if missing)
            try:
                title_elements = article.find_elements(By.CSS_SELECTOR, TITLE_SELECTOR)
                if len(title_elements) > 0:
                    title = title_elements[0].text.strip()  # Pick the first `.directory-text-small`
                else:
                    title = " "
            except Exception:
                title = " "
 
            # Extract email
            try:
                email_element = article.find_element(By.CSS_SELECTOR, EMAIL_SELECTOR)
                email = email_element.get_attribute("href").replace("mailto:", "").strip()
            except Exception:
                email = "N/A"
 
            # Append the extracted data
            instructors.append({
                "Name": name,
                "Title": title,
                "Email": email
            })
        except Exception as e:
            print(f"Error scraping an article: {e}")
 
    return instructors

# Save the data to a CSV file
def load_data(instructors):
    df = pd.DataFrame(instructors)
    try:
        df.to_csv("directory.csv", index=False)
        print("File saved successfully!")
    except Exception as e:
        print(f"Error: {e}")

def main():
    driver = load_webpage()

    # Scroll to load more content
 
    #scroll_to_load(driver)  # Scroll until all content is loaded
    load_more(driver)

    # Extract the data after content is fully loaded
    data = extract_data(driver)
    load_data(data)  # Save data to a CSV file
    driver.quit()

if __name__ == "__main__":
    main()
