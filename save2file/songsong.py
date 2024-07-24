import requests
from bs4 import BeautifulSoup
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# URL của các mục
urls = {
    'giáo dục': 'https://vnexpress.net/giao-duc/tuyen-sinh',
    'khoa học': 'https://vnexpress.net/khoa-hoc/khoa-hoc-trong-nuoc',
    'bất động sản': 'https://vnexpress.net/bat-dong-san/thi-truong'
    # 'du lịch': 'https://vnexpress.net/du-lich/diem-den',
    # 'thể thao': 'https://vnexpress.net/bong-da',
    # 'kinh doanh': 'https://vnexpress.net/kinh-doanh/doanh-nghiep'
}

# Hàm crawl dữ liệu từ URL
def crawl_vnexpress(url, top_n=10):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='item-news item-news-common thumb-left')
    
    data = []
    for article in articles[:top_n]:
        title = article.find('h3', class_='title-news').text.strip()
        link = article.find('a')['href']
        summary = article.find('p', class_='description').text.strip()
        data.append({'title': title, 'link': link, 'summary': summary})
    
    return data

# Hàm crawl dữ liệu chi tiết từ trang bài viết
def crawl_article_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = ' '.join([p.text.strip() for p in soup.find_all('p', class_='Normal')])
    return content

# Hàm lưu dữ liệu vào file theo chủ đề
def save_to_file(topic, article, index):
    file_name = f"{topic}_ss.txt"
    with open(file_name, 'a', encoding='utf-8') as file:  # Mở file ở chế độ append
        file.write(f"Chủ đề: {topic}\n")
        file.write(f"Tiêu đề: {article['title']}\n")
        file.write(f"Link: {article['link']}\n")
        file.write(f"Tóm tắt: {article['summary']}\n")
        file.write(f"Nội dung chi tiết:\n")
        details = crawl_article_details(article['link'])
        file.write(f"{details}\n")
        file.write("------\n")

# Hàm thực hiện crawl và lưu dữ liệu cho một chủ đề
def process_topic(topic, url):
    print(f"Đang crawl dữ liệu chủ đề {topic}...")
    articles = crawl_vnexpress(url)
    
    for index, article in enumerate(articles):
        save_to_file(topic, article, index)

# Hàm chính để chạy các tác vụ song song
def main():
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:  # Tùy chỉnh số lượng worker
        futures = [executor.submit(process_topic, topic, url) for topic, url in urls.items()]
        for future in as_completed(futures):
            future.result()  # Xử lý kết quả hoặc ngoại lệ nếu cần
    
    end_time = time.time()
    print(f"Thời gian thực hiện song song: {end_time - start_time} giây")

# Chạy hàm chính
if __name__ == "__main__":
    main()
