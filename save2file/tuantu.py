import requests
from bs4 import BeautifulSoup
import time

# URL của mục giáo dục và bóng đá
urls = {
    'giáo dục': 'https://vnexpress.net/giao-duc/tuyen-sinh',
    'khoa học': 'https://vnexpress.net/khoa-hoc/khoa-hoc-trong-nuoc',
    'bất động sản': 'https://vnexpress.net/bat-dong-san/thi-truong'
}

# Hàm crawl dữ liệu từ URL
def crawl_vnexpress(url, top_n=10):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Lấy danh sách các bài viết
    articles = soup.find_all('article', class_='item-news item-news-common thumb-left')
    
    data = []
    for article in articles[:top_n]:  # Chỉ lấy top_n bài viết đầu tiên
        title = article.find('h3', class_='title-news').text.strip()
        link = article.find('a')['href']
        summary = article.find('p', class_='description').text.strip()
        data.append({'title': title, 'link': link, 'summary': summary})
    
    return data

# Hàm crawl dữ liệu chi tiết từ trang bài viết
def crawl_article_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Giả sử chúng ta lấy nội dung bài viết từ thẻ <p> trong class 'Normal'
    content = ' '.join([p.text.strip() for p in soup.find_all('p', class_='Normal')])
    return content

# Đo thời gian thực hiện phiên bản tuần tự
start_time = time.time()
for topic, url in urls.items():
    print(f"Đang crawl dữ liệu chủ đề {topic}...")
    articles = crawl_vnexpress(url)
    with open(f"{topic}_tt.txt", "w", encoding="utf-8") as file:
        for article in articles:
            file.write(f"Tiêu đề: {article['title']}\n")
            file.write(f"Link: {article['link']}\n")
            file.write(f"Tóm tắt: {article['summary']}\n")
            file.write("------\n")
            # Crawl dữ liệu chi tiết của bài viết
            details = crawl_article_details(article['link'])
            file.write(f"Nội dung chi tiết: {details}\n")
            file.write("------\n")
end_time = time.time()

print(f"Thời gian thực hiện tuần tự: {end_time - start_time} giây")
