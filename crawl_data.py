from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from modules.preprocess import preprocess_text
import csv
import re

def get_reviews_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Mở trang web
        driver.get(url)
        time.sleep(3)

        # Scroll để tải thêm nội dung
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script(f"window.scrollTo(0, {total_height * 0.5});")
        time.sleep(2)

        reviews = []

        # Biến đếm số vòng lặp
        #loop_count = 0
        # Lặp qua các trang phân trang
        while True:
            # Tăng số vòng lặp
            #loop_count += 1
            # Tìm các đánh giá trên trang hiện tại
            review_elements = driver.find_elements(By.CLASS_NAME, "review-comment__content")
            title_elements = driver.find_elements(By.CLASS_NAME, "review-comment__title")
            for review,title in zip(review_elements,title_elements):
                text = review.text.replace('\n', ' ').strip()
                title = title.text.strip()
                if text and title:  # Chỉ thêm nếu nội dung không rỗng
                    with open('output.csv', 'a', newline='', encoding='utf-8') as csvFile:
                        writer = csv.writer(csvFile)                                               
                        if len(text) < 10:
                            continue
                        if title in ['Hài lòng', 'Cực kì hài lòng']:
                            title_value = 0 # Positive
                        else:
                            title_value = 1 # Negative
                        writer.writerow([text, title_value])

            time.sleep(2)  # Tạm dừng để tránh bị phát hiện như bot

            try:
                # Tìm nút "Next" cố định
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//li/a[contains(@class, 'btn') and contains(@class, 'next')]")
                    )
                )
                
                # Nhấp vào nút của trang tiếp theo
                next_button.click()

                time.sleep(2)  # Tạm dừng để tránh bị phát hiện như bot

            except Exception as e:

                print("Không tìm thấy nút 'Trang tiếp theo' hoặc gặp lỗi:", e)
                break

        # Trả về danh sách đánh giá hoặc thông báo nếu không có 
        if not reviews:
            return {"message": "Không tìm thấy đánh giá nào"}
        return reviews
    finally:
        driver.quit()

def crawl_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()
    
    for url in urls:
        url = url.strip()
        if url:
            print(f"Processing URL: {url}")
            get_reviews_with_selenium(url)

if __name__ == '__main__':
    file_path = 'urls_tiki.txt'  # Path to the file containing the list of URLs
    crawl_data_from_file(file_path)