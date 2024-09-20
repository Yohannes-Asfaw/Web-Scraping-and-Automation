from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup the WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open Google Maps
driver.get('https://www.google.com/maps')

# Explicit wait for the page to load
wait = WebDriverWait(driver, 15)

# Locate the search box and input the query for hotels in Addis Ababa
search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
search_box.send_keys('Hotels in Addis Ababa')
search_box.send_keys(Keys.ENTER)

# Wait for a few seconds to allow results to load
time.sleep(5)

# Using the `role` attribute to locate the results container
try:
    results_container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='feed']")))
    print("Found the results container using role='feed'.")
except Exception as e:
    print(f"Error waiting for results container: {e}")
    driver.quit()

# Initialize a list to store the hotel information
hotel_data = []

# Scroll and scrape hotels until no new hotels are loaded
while True:
    time.sleep(3)  # Wait for hotel elements to load
    
    # Find all hotel elements within the results container
    hotels = results_container.find_elements(By.CLASS_NAME, "m6QErb")

    # If no hotels found, break the loop
    if not hotels:
        print("No hotels found.")
        break

    # Loop through each hotel entry
    for hotel in hotels:
        try:
            name = hotel.find_element(By.CLASS_NAME, "qBF1Pd").text
            rating = hotel.find_element(By.CLASS_NAME, "MW4etd").text
            num_reviews = hotel.find_element(By.CLASS_NAME, "UY7F9").text

            hotel_data.append({
                'Name': name,
                'Rating': rating,
                'Number of Reviews': num_reviews
            })
        except Exception as e:
            print(f"Error processing hotel: {e}")
            continue

    # Scroll down to load more hotels
    driver.execute_script("arguments[0].scrollBy(0, 1000);", results_container)

# Convert the data into a Pandas DataFrame
df = pd.DataFrame(hotel_data)
print(df)

# Save the data to a CSV file if any results are found
if not df.empty:
    df.to_csv('hotels_in_addis_ababa.csv', index=False)
else:
    print("No hotel data found.")

# Close the WebDriver
driver.quit()
