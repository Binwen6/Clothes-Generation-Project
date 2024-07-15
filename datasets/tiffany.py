import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_image(url, filepath):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)

def scrape_product_page(url, product_folder):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到并下载两张图片
        image_elements = soup.select('img.pdp-main-image')[:2]
        for i, img in enumerate(image_elements):
            img_url = urljoin(url, img['src'])
            img_path = os.path.join(product_folder, f'image_{i+1}.jpg')
            download_image(img_url, img_path)

def main():
    base_url = 'https://www.tiffany.com'
    main_page_url = 'https://www.tiffany.com/jewelry/shop/earrings/sort-relevance/?page=view-all'
    
    response = requests.get(main_page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有311个产品链接
        product_links = soup.select('div.browse-grid div[class^="col-"] article a')[:311]
        
        for i, link in enumerate(product_links):
            product_url = urljoin(base_url, link['href'])
            product_folder = f'product_{i+1}'
            create_directory(product_folder)
            
            print(f"Scraping product {i+1}: {product_url}")
            scrape_product_page(product_url, product_folder)

if __name__ == '__main__':
    main()