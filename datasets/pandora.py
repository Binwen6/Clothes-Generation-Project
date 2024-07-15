import os
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 配置 ChromeOptions
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU
chrome_options.add_argument("--no-sandbox")

# 设置 ChromeDriver 路径
chromedriver_path = 'C:/Users/lenovo/.cache/selenium/chromedriver/win64/126.0.6478.126/chromedriver.exe'  # 替换为实际路径
service = Service(chromedriver_path)

# 初始化 WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(30)

# 创建 images 文件夹
images_folder = 'images_3'
os.makedirs(images_folder, exist_ok=True)

# 遍历多个 URL

start_url = f'https://hk.pandora.net/earrings/earrings/'
try:
    # 尝试加载页面
    driver.get(start_url)
except TimeoutException:
    print("Page load timed out but continuing anyway")

try:
    # 打开起始页面
    driver.get(start_url)
    print(1)

    # 等待页面加载
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#product-search-results")))
    print(1)
    # 初始化产品 URL 列表
    product_urls = []
    print(1)

    # 查找包含产品的元素并提取 data-component-url
    product_elements = driver.find_elements(By.CSS_SELECTOR, ".image-link")
    print(1)

    for element in product_elements:
        data_component_url = element.get_attribute('href')
        if data_component_url:
            product_urls.append(data_component_url)
    print(1)

    for i, product_url in enumerate(product_urls):
        full_product_url = 'https://hk.pandora.net' + product_url
        driver.get(full_product_url)

        # 文件夹命名规则
        folder_name = os.path.join(images_folder, f'pair_{i + 1}')
        os.makedirs(folder_name, exist_ok=True)

        try:
            # 等待图片元素加载
            wait = WebDriverWait(driver, 10)
            image_elements = []
            for child in [1, 2]:
                css_selector = f"# pdpCarousel-288190C01 > div:nth-child({child}) > img"

                img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
                image_elements.append(img_element)

            for index, img_element in enumerate(image_elements):
                img_url = img_element.get_attribute('src')
                if img_url:
                    print(f"Image URL for pair_{i + 1} child {index + 2}: {img_url}")

                    # 下载图片
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        img_name = os.path.join(folder_name, f'{["jewellery", "model"][index]}.jpg')
                        with open(img_name, 'wb') as f:
                            f.write(img_response.content)
                        print(f"Downloaded {img_name}")
                    else:
                        print(
                            f"Failed to download the image from {full_product_url}. Status code: {img_response.status_code}")
                else:
                    print(f"Image URL not found for pair_{i + 1} child {index + 2}.")
        except Exception as e:
            print(f"Error processing {full_product_url}: {e}")
except Exception as e:
    print(f"Error accessing start URL {start_url}: {e}")

