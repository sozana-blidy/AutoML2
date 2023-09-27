from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver

from selenium.webdriver.firefox.webdriver import WebDriver



def get_page_content_after_submit(stnnumber):

    browser = WebDriver()

    # ... rest of your code ...

    # ... rest of your script ...



    # Navigate to the page
    browser.get('http://2023.moed.gov.sy/sec-ch1/12th/index.php')

    # Locate the input field (this is a placeholder, you need to replace with the correct ID or name)
    input_field = browser.find_element_by_id('YOUR_INPUT_FIELD_ID_OR_NAME')

    # Enter the stnnumber
    input_field.send_keys(stnnumber)

    # Submit the form (this assumes there's only one form on the page)
    input_field.send_keys(Keys.RETURN)

    # Wait for the page to load (you can also use more advanced wait methods)
    time.sleep(5)

    # Get the page content
    page_content = browser.page_source

    # Close the browser
    browser.quit()

    return page_content


start_stnnumber = 12000
end_stnnumber = 15000

all_pages = []

for stnnumber in range(start_stnnumber, end_stnnumber + 1):
    page_content = get_page_content_after_submit(stnnumber)
    all_pages.append(page_content)

# Example: Print the content of the first page
print(all_pages[0])
