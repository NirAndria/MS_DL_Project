import os
import requests
import imghdr
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to initialize Selenium WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to fetch image URLs from the Google Image Search page
def fetch_image_urls(search_url):
    driver = init_driver()
    driver.get(search_url)

    try:
        # Wait for the cookie consent popup and click "Tout refuser"
        consent_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "W0wltc"))
        )
        consent_button.click()
        print("✅ Clicked 'Tout refuser' on cookie consent.")
    except:
        print("⚠️ No cookie consent popup found. Continuing...")
    
    # Scroll to the bottom of the page to load more images
    last_height = driver.execute_script("return document.body.scrollHeight")
    image_urls = set()
    scroll_attempts = 0
    max_scroll_attempts = 30  # Prevent infinite loops


    while (len(image_urls) < 150) and (scroll_attempts < max_scroll_attempts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            # Wait until at least one new image is loaded (max wait: 5 sec)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
        except:
            print("No new images loaded.")
            break  # Stop if no more images are loading

        # Extract image URLs
        img_tags = driver.find_elements(By.TAG_NAME, "img")
        for img in img_tags:
            img_url = img.get_attribute("src")
            if img_url and (img_url.startswith("http") or img_url.startswith("https")):
                image_urls.add(img_url)

        scroll_attempts += 1

    driver.quit()
    return list(image_urls)

# Function to download images
def download_images(image_urls,label_list):
    """Downloads images from a list of URLs."""
    for i, url in enumerate(image_urls):


        try:
            # Validate URL
            # if not (url.endswith(".jpg") or url.endswith(".png") or url.endswith(".jpeg") or url.endswith(".webp")):
            #     print(f"⚠️ Skipping non-image URL: {url}")
            #     continue

            response = requests.get(url, stream=True)
            if response.status_code == 200 and "image" in response.headers["Content-Type"]:
                img_path = os.path.join("D:/MS/DL/Project/MS_DL_Project/img_webscrapp", f"{label_list[i]}_{i+1}.jpg")
                with open(img_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)

                # Verify the downloaded file is a valid image
                if not imghdr.what(img_path):
                    print(f"❌ Corrupted file detected: {img_path}, deleting...")
                    os.remove(img_path)
                else:
                    print(f"✅ Downloaded: {img_path}")

            else:
                print(f"❌ Failed to download {url} (Invalid response)")

        except Exception as e:
            print(f"⚠️ Error downloading {url}: {e}")


# Main function to scrape and download images from Google Image
def main():
    #url = input("Enter the Google Image URL: ")
    url_list = [
        #'https://www.google.com/search?q=small+number+of+birds+seen+in+the+sky&sca_esv=df054736d75a2025&hl=fr&udm=2&cs=1&rlz=1C1UEAD_frFR969FR969&biw=1536&bih=695&sxsrf=AHTn8zrqrrP-KkFipc7qQ7FG7Ah0owc4mA%3A1738770760261&ei=SImjZ_jXD5StkdUP0pqKqQQ&ved=0ahUKEwj4m4vs8ayLAxWUVqQEHVKNIkUQ4dUDCBE&uact=5&oq=small+number+of+birds+seen+in+the+sky&gs_lp=EgNpbWciJXNtYWxsIG51bWJlciBvZiBiaXJkcyBzZWVuIGluIHRoZSBza3lIgjBQ7wlY_S5wAngAkAEAmAGyAaABjw2qAQQxMi41uAEDyAEA-AEBmAIBoAIHwgIEECMYJ8ICBhAAGAgYHpgDAIgGAZIHATGgB4UG&sclient=img',
        #'https://www.google.com/search?q=plane%20seen%20in%20the%20sky&hl=fr&udm=2&tbs=rimg:Ces9imT4LwTsYQ_1lO8Dq2GKEsgIAwAIA2AIA4AIA&cs=1&rlz=1C1UEAD_frFR969FR969&sa=X&ved=0CCUQuIIBahcKEwiImJG44ZqLAxUAAAAAHQAAAAAQBw&biw=1536&bih=695&dpr=1.25',
        #'https://www.google.com/search?q=plane%20seen%20in%20the%20sky&hl=fr&tbs=rimg:CWEJ8e3tGDsUYUzTIvjcxU4LsgIAwAIA2AIA4AIA&udm=2&cs=1&rlz=1C1UEAD_frFR969FR969&sa=X&ved=0CBoQuIIBahcKEwigwcCu9qyLAxUAAAAAHQAAAAAQBw&biw=1536&bih=695&dpr=1.25',
        #'https://www.google.com/search?q=drone%20seen%20in%20the%20sky&hl=fr&udm=2&tbs=rimg:CUXfsVLzkPZjYYNECE8wa8zvsgIAwAIA2AIA4AIA&cs=1&rlz=1C1UEAD_frFR969FR969&sa=X&ved=0CBoQuIIBahcKEwjglMrm4JqLAxUAAAAAHQAAAAAQBw&biw=1536&bih=695&dpr=1.25',
        #'https://www.google.com/search?q=helicopter%20%20seen%20in%20the%20sky&hl=fr&udm=2&tbs=rimg:CQZxe_1Pja8TcYZmPv26E-lntsgIAwAIA2AIA4AIA&cs=1&rlz=1C1UEAD_frFR969FR969&sa=X&ved=0CBwQuIIBahcKEwi4tvLY4ZqLAxUAAAAAHQAAAAAQBw&biw=1536&bih=695&dpr=1.25',
        'https://www.google.com/search?q=drone%20seen&hl=fr&tbs=rimg:CSHFUPL-8cAVYU0SqzQyAGEesgIAwAIA2AIA4AIA&udm=2&cs=1&rlz=1C1UEAD_frFR969FR969&sa=X&ved=0CCQQuIIBahcKEwiQ5O2PubmLAxUAAAAAHQAAAAAQBw&biw=1536&bih=695&dpr=1.25'
    ]

    label_list = [
        # 'birds',
        # 'plane',
        # 'plane,'
        # 'drone',
        # 'helicopter'
        "drone"
    ]

    image_urls_list = []
    label = []

    for idx, url in enumerate(url_list):
        print("Fetching image URLs...")
        print(label_list[idx])
        image_urls = fetch_image_urls(url)
        print(len(image_urls))
        image_urls_list += image_urls
        label += [label_list[idx]] * len(image_urls)
        #print(label_list[idx])
    
    #image_urls_list = list(set(image_urls_list))
    
    print(f"Found {len(image_urls_list)} images. Downloading...")
    download_images(image_urls_list,label)
    print("Download completed!")

if __name__ == "__main__":
    main()
