from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import csv
import time
import random
def save_to_csv(image_paths, filename="image_paths.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image Path"])
        for path in image_paths:
            writer.writerow([path])

def parse_image(html_page):
    result = []
    html = HTMLParser(html_page)
    ul_element = html.css_first('div.main.parsys ul.products-listing.small')
    if ul_element:
        image_containers = ul_element.css('div.image-container')
        
        for container in image_containers:
            img_tag = container.css_first('img.item-image')
            if img_tag:
                image_src = img_tag.attributes.get('src')
                if image_src:
                    result.append(image_src)
    
    return result

def main():
    url = "https://www2.hm.com/en_in/women/shop-by-product/shirts-blouses.html"
    all_image_paths = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        
        while True:
            img_paths = parse_image(page.content())
            all_image_paths.extend(img_paths)
            
            try:
                # Wait for the "Load more products" button to be visible
                next_page_button = page.locator(".button.js-load-more")
                if next_page_button.is_visible(timeout=30000):  # Adjust timeout if necessary
                    next_page_button.click()
                    page.wait_for_load_state('networkidle')
                else:
                    break
            except Exception as e:
                print(f"Error: {e}")
                break

            # Adding a short delay to avoid being flagged as a bot
            time.sleep(random.uniform(1, 3))

    # Save all collected image paths to CSV once at the end
    save_to_csv(all_image_paths)

if __name__ == "__main__":
    main()