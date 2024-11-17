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

# Extract the data from the page
def extract_data(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    employee_blocks = soup.find_all("div", class_="pb-2")

    print(f"Number of employee blocks found: {len(employee_blocks)}")

    name_data = []
    title_data = []
    email_data = []

    # Loop through the employee blocks and extract relevant information
    for i in range(0, len(employee_blocks), 4):
        try:
            name_div = employee_blocks[i].find("a")
            title_div = employee_blocks[i + 1]
            email_div = employee_blocks[i + 3].find("a", href=True)

            if name_div and title_div and email_div:
                name = name_div.text.strip()
                title = title_div.text.strip() if title_div else "No Title"
                email = email_div.text.strip() if email_div else "No Email"

                name_data.append(name)
                title_data.append(title)
                email_data.append(email)
            else:
                print(f"Skipping incomplete block at index {i}")
        except IndexError:
            print(f"Error processing block {i}")

    return name_data, title_data, email_data

# Save the data to a CSV file
def load_data(name_data, title_data, email_data):
    df = pd.DataFrame({
        "Name": name_data,
        "Title": title_data,
        "Email": email_data
    })
    try:
        df.to_csv("First_Directory.csv", index=False)
        print("File saved successfully!")
    except Exception as e:
        print(f"Error: {e}")

def main():
    driver = load_webpage()

    # Scroll to load more content
    scroll_to_load(driver)  # Scroll until all content is loaded

    # Extract the data after content is fully loaded
    name_data, title_data, email_data = extract_data(driver)
    load_data(name_data, title_data, email_data)  # Save data to a CSV file

if __name__ == "__main__":
    main()
