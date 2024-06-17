from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import random
import csv

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
    url = "https://www2.hm.com/en_in/men/shop-by-product/tshirts-tank-tops.html"
    #proxy = get_random_proxy()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url,wait_until='networkidle')
        next_page = page.locator(".button.js-load-more")
        while True:
            
            img_paths = parse_image(page.content())
            save_to_csv(img_paths)
            if next_page.is_disabled():
                break
            page.click(".button.js-load-more")
            page.wait_for_load_state('networkidle')


if __name__ == "__main__":
    main()