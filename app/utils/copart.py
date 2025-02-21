from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from fastapi import status
from ..core.exceptions import HTTPException

async def get_car_location(lot_number: str = "89338945"):
    # Set up Firefox options
    options = Options()
    options.headless = True  # Run in headless mode (without opening a browser window)
    # Initialize the Firefox driver using GeckoDriverManager
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    try:
        url = f"https://www.copart.com/lot/{lot_number}"
        # Open the page
        driver.get(url)
        # Define the maximum wait time (in seconds)
        wait = WebDriverWait(driver, 200)
        # Wait for the element containing car details to be present
        sale_info_div = wait.until(
            EC.presence_of_element_located((By.ID, "sale-information-block"))
        )
        # Once the div is present, retrieve all its child elements
        child_elements = sale_info_div.find_elements(By.XPATH, ".//*")
        # Iterate over each child element and print its tag name and text content
        location = None
        for element in child_elements:
            if element.tag_name == "a" and element.get_attribute("data-uname") == "lotdetailSaleinformationlocationvalue":
                location = element.text
                break
        if location is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not extract location from Copart")
        return location
    finally:
        # Close the driver
        driver.quit()

