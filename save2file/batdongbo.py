import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

# URL của mục giáo dục và bóng đá
urls = {
    'giáo dục': 'https://vnexpress.net/giao-duc/tuyen-sinh',
    'khoa học': 'https://vnexpress.net/khoa-hoc/khoa-hoc-trong-nuoc',
    'bất động sản': 'https://vnexpress.net/bat-dong-san/thi-truong'
    # 'du lịch': 'https://vnexpress.net/du-lich/diem-den',
    # 'thể thao': 'https://vnexpress.net/bong-da',
    # 'kinh doanh': 'https://vnexpress.net/kinh-doanh/doanh-nghiep'
}

# Hàm crawl dữ liệu từ URL
async def crawl_vnexpress(session, url, top_n=10):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article', class_='item-news item-news-common thumb-left')
        
        data = []
        for article in articles[:top_n]:
            title = article.find('h3', class_='title-news').text.strip()
            link = article.find('a')['href']
            summary = article.find('p', class_='description').text.strip()
            data.append({'title': title, 'link': link, 'summary': summary})
        
        return data

# Hàm crawl dữ liệu chi tiết từ trang bài viết
async def crawl_article_details(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        content = ' '.join([p.text.strip() for p in soup.find_all('p', class_='Normal')])
        return content

# Hàm lưu dữ liệu vào file
async def save_to_file(topic, articles, session):
    with open(f'{topic}_bdb.txt', 'w', encoding='utf-8') as file:
        for article in articles:
            file.write(f"Tiêu đề: {article['title']}\n")
            file.write(f"Link: {article['link']}\n")
            file.write(f"Tóm tắt: {article['summary']}\n")
            file.write(f"Nội dung chi tiết:\n")
            details = await crawl_article_details(session, article['link'])
            file.write(f"{details}\n")
            file.write("------\n")

# Hàm thực hiện crawl và lưu dữ liệu cho một chủ đề
async def process_topic(session, topic, url):
    print(f"Đang crawl dữ liệu chủ đề {topic}...")
    articles = await crawl_vnexpress(session, url)
    await save_to_file(topic, articles, session)

# Hàm chính để chạy các tác vụ bất đồng bộ
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [process_topic(session, topic, url) for topic, url in urls.items()]
        await asyncio.gather(*tasks)

# Đo thời gian thực hiện phiên bản bất đồng bộ
start_time = time.time()
asyncio.run(main())  # Sử dụng asyncio.run để chạy hàm main() bất đồng bộ
end_time = time.time()

print(f"Thời gian thực hiện bất đồng bộ: {end_time - start_time} giây")
